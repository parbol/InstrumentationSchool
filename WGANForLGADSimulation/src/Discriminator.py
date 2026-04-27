import torch



class Discriminator(torch.nn.Module):

	def __init__(self):
		super().__init__()
	
		self.encoder = torch.nn.Sequential(
			torch.nn.Linear(5, 5),
	        torch.nn.BatchNorm1d(5),
            torch.nn.ReLU(),
			torch.nn.Linear(5, 3),
	        torch.nn.BatchNorm1d(3),
			torch.nn.ReLU(),
			torch.nn.Linear(3, 1),
			torch.nn.Sigmoid()
		)
		

	def forward(self, x):
		encoded = self.encoder(x)
		return encoded
	
    
