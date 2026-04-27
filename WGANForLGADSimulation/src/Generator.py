import torch



class Generator(torch.nn.Module):

	def __init__(self):
		super().__init__()
	
		self.encoder = torch.nn.Sequential(
			torch.nn.Linear(8, 25),
	        torch.nn.BatchNorm1d(25),
            torch.nn.ReLU(),
			torch.nn.Linear(25, 50),
	        torch.nn.BatchNorm1d(50),
			torch.nn.ReLU(),
			torch.nn.Linear(50, 20),
	        torch.nn.BatchNorm1d(20),
			torch.nn.ReLU(),
			torch.nn.Linear(20, 2),
			torch.nn.ReLU()
		)
		

	def forward(self, x):
		encoded = self.encoder(x)
		return encoded
	
