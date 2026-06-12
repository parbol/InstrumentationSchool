import torch



class Discriminator(torch.nn.Module):

	def __init__(self, conditional_dim, output_dim):
		super().__init__()
	
		self.encoder = torch.nn.Sequential(
			torch.nn.Linear(conditional_dim + output_dim , 64),
	        torch.nn.BatchNorm1d(64),
            #torch.nn.LeakyReLU(negative_slope=0.2),
            torch.nn.ReLU(),
			torch.nn.Linear(64, 32),
	        torch.nn.BatchNorm1d(32),
			#torch.nn.LeakyReLU(negative_slope=0.2),
            torch.nn.ReLU(),
			torch.nn.Linear(32, 16),
	        torch.nn.BatchNorm1d(16),
			#torch.nn.LeakyReLU(negative_slope=0.2),
            torch.nn.ReLU(),
			torch.nn.Linear(16, 1)
		)
		

	def forward(self, x):
		encoded = self.encoder(x)
		return encoded
	
    
