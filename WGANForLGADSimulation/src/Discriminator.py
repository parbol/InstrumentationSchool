import torch



class Discriminator(torch.nn.Module):

	def __init__(self):
		super().__init__()
	
		self.encoder = torch.nn.Sequential(
			torch.nn.Linear(5, 10),
	        torch.nn.BatchNorm1d(10),
            torch.nn.ReLU(),
			torch.nn.Linear(10, 5),
	        torch.nn.BatchNorm1d(5),
			torch.nn.ReLU(),
			torch.nn.Linear(5, 1),
            torch.nn.Sigmoid()
		)
		

	def forward(self, x):
		encoded = self.encoder(x)
		return encoded
	
    
