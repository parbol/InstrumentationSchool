import torch



class Generator(torch.nn.Module):

	def __init__(self, latent_dim, conditional_dim, output_dim):
		super().__init__()
	
		self.encoder = torch.nn.Sequential(
			torch.nn.Linear(latent_dim + conditional_dim, 16),
	        torch.nn.BatchNorm1d(16),
            torch.nn.ReLU(),
			torch.nn.Linear(16, 32),
	        torch.nn.BatchNorm1d(32),
			torch.nn.ReLU(),
			torch.nn.Linear(32, 64),
	        torch.nn.BatchNorm1d(64),
			torch.nn.ReLU(),
			torch.nn.Linear(64, output_dim)
		)
		

	def forward(self, x):
		encoded = self.encoder(x)
		return encoded
	
