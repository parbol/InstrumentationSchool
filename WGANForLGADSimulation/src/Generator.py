import torch



class Generator(torch.nn.Module):

	def __init__(self):
		super().__init__()
	
		self.encoder = torch.nn.Sequential(
			torch.nn.Linear(27, 100),
	        torch.nn.BatchNorm1d(100),
            torch.nn.ReLU(),
			torch.nn.Linear(100, 50),
	        torch.nn.BatchNorm1d(50),
			torch.nn.ReLU(),
			torch.nn.Linear(50, 12),
			torch.nn.ReLU()
		)
		

	def forward(self, x):
		encoded = self.encoder(x)
		return encoded
	
