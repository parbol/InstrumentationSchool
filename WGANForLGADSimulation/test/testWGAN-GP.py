import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import backend
from tensorflow.keras import layers
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.callbacks import LearningRateScheduler
from keras.models import Model
from keras.layers import Input
from keras.layers import Dense
from keras.layers import Reshape
from keras.layers import Flatten
from keras.layers import Conv2D
from keras.layers import Conv2DTranspose
from keras.layers import LeakyReLU
from keras.layers import Dropout
from keras.layers import Embedding
from keras.layers import Concatenate
from keras.layers import Activation
from keras.layers import BatchNormalization
from keras.initializers import RandomNormal
from keras.constraints import Constraint
import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

from WGANForLGADSimulation.src.WGAN import WGAN
from WGANForLGADSimulation.src.WGAN import GANMonitor
from WGANForLGADSimulation.src.WGAN import PlotLosses
from WGANForLGADSimulation.src.WGAN import StepDecay

import sys



def load(inputfile):

    data = pd.read_parquet(inputfile).to_numpy()
    print(data)
    sys.exit()
    variables = data[:,:8]
    labels = data[:,8]

    scaler = StandardScaler()
    weights = 1/np.sqrt(data[:,4]**2 + data[:,5]**2)
    scaler.fit(variables, sample_weight=weights)
    variables = scaler.transform(variables)

    return [variables, labels], scaler


def get_discriminator_model(in_shape):
    # first detector and label input
    in_first_det_data = Input(shape=in_shape)
    # second detector input
    in_second_detector = Input(shape=in_shape)
    # concat label as a channel
    merge = Concatenate()([in_second_detector, in_first_det_data])

    fe = Dense(64)(merge)
    fe = LeakyReLU(alpha=0.2)(fe)
    fe = Dense(32)(fe)
    fe = LeakyReLU(alpha=0.2)(fe)
    fe = Dense(16)(fe)
    fe = LeakyReLU(alpha=0.2)(fe)

    # output
    out_layer = Dense(1, activation='linear')(fe)
    # define model
    d_model = Model([in_second_detector, in_first_det_data], out_layer)
    return d_model
                   

def get_generator_model(in_shape, latent_dim):
    # data and label input
    in_first_detector = Input(shape=in_shape)
    # noise input
    in_lat = Input(shape=latent_dim)

    merge = Concatenate()([in_lat, in_first_detector])

    gen = Dense(16)(merge)
    gen = Activation('relu')(gen)
    gen = Dense(32)(gen)
    gen = Activation('relu')(gen)
    gen = Dense(64)(gen)
    gen = Activation('relu')(gen)

    # output
    out_layer = Dense(4, activation='linear')(gen)
    # define model
    g_model = Model([in_lat, in_first_detector], out_layer)
    return g_model




if __name__ == "__main__":

    # GPU memory usage configuration
    #config = tf.compat.v1.ConfigProto()
    #config.gpu_options.allow_growth = True
    #sess = tf.compat.v1.Session(config=config)
    #backend.set_session(sess)

    BATCH_SIZE = 5000
    LATENT_DIM = 16
    EPOCHS = 1000
    LEARNING_RATE = 0.0001
    K = 5

    inputfile = "../data/output.parquet"

    print('_' * 100)
    print('OPTIONS WGAN-GP')
    print('_' * 100)
    print(' Training data file: {:<50}'.format(inputfile))
    print('     Training epochs: {:<50}'.format(EPOCHS))
    print('     Dimension of latent space: {:<50}'.format(LATENT_DIM))
    print('     Batch size: {:<50}'.format(BATCH_SIZE))
    print('     k hyperparameter: {:<50}'.format(K))
    print('_' * 100)

    print('Loading data: '+inputfile)
    [train_samples, labels], scaler = load(inputfile)
    # Take only samples with one pipe radius value
    train_samples = train_samples[labels==16]
    print(f"Data shape: {train_samples.shape}")

    d_model = get_discriminator_model(in_shape=4)
    d_model.summary()
    g_model = get_generator_model(in_shape=4, latent_dim=LATENT_DIM)
    g_model.summary()

    # Instantiate the optimizer for both networks
    # (learning_rate=0.0002, beta_1=0.5 are recommended)
    generator_optimizer = keras.optimizers.Adam(
        learning_rate=LEARNING_RATE, beta_1=0.5, beta_2=0.9
    )
    discriminator_optimizer = keras.optimizers.Adam(
        learning_rate=LEARNING_RATE, beta_1=0.5, beta_2=0.9
    )

    # Define the loss functions for the discriminator,
    # which should be (fake_loss - real_loss).
    # We will add the gradient penalty later to this loss function.
    def discriminator_loss(real_img, fake_img):
        real_loss = tf.reduce_mean(real_img)
        fake_loss = tf.reduce_mean(fake_img)
        return fake_loss - real_loss

    # Define the loss functions for the generator.
    def generator_loss(fake_img):
        return -tf.reduce_mean(fake_img)

    # Instantiate the custom Keras callbacks.
    cbk = GANMonitor(saveEvery=25)
    pltloss = PlotLosses()
    lrs = LearningRateScheduler(StepDecay(initLearningRate=LEARNING_RATE, factor=1, dropEvery=1000), verbose=0)


    # Instantiate the WGAN model.
    wgan = WGAN(
        discriminator=d_model,
        generator=g_model,
        total_n_samples=train_samples.shape[0],
        latent_dim=LATENT_DIM,
        discriminator_extra_steps=K,
    )

    # Compile the WGAN model.
    wgan.compile(
        d_optimizer=discriminator_optimizer,
        g_optimizer=generator_optimizer,
        g_loss_fn=generator_loss,
        d_loss_fn=discriminator_loss,
    )

    # Start training the model.
    wgan.fit(train_samples, batch_size=BATCH_SIZE, epochs=EPOCHS, callbacks=[cbk, pltloss, lrs])
