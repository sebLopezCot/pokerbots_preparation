
class Player:

	names = set(['Cayla','Roxie','Anya','Kindra','Kittie','Kitty','Sonya','Mora',
		'Amada','Shawnee','Shizue','Shanti','Sherry','Miles','Martha','Marisela',
		'Reena','Edwin','Demetria','Lorrine','Jacques','Michele','Maryanna','Carson',
		'Nilsa','Tawnya','Vince','Heather','Necole','Mozelle','Sheilah','Rhoda','Rolf',
		'Eugene','Kizzie','Elinore','Bruno','Suk','Yoshiko','Sharie','Monique','Jasmine',
		'Meghan','Glennis','Vertie','Francesco','Isidro','Calvin','Elvia','Candie'])


	def __init__(self):
		self.name = Player.names.pop()
		self.hand = None
		self.is_dealer = False

	def give_hand(self, hand):
		self.hand = hand

	def get_move(self, situation):
		pass
