
class Player:

	names = set(['Cayla','Roxie','Anya','Kindra','Kittie','Kitty','Sonya','Mora',
		'Amada','Shawnee','Shizue','Shanti','Sherry','Miles','Martha','Marisela',
		'Reena','Edwin','Demetria','Lorrine','Jacques','Michele','Maryanna','Carson',
		'Nilsa','Tawnya','Vince','Heather','Necole','Mozelle','Sheilah','Rhoda','Rolf',
		'Eugene','Kizzie','Elinore','Bruno','Suk','Yoshiko','Sharie','Monique','Jasmine',
		'Meghan','Glennis','Vertie','Francesco','Isidro','Calvin','Elvia','Candie'])

	start_stack_sizes = {5: 20, 10: 10, 20: 5, 50: 4, 100: 1}

	def __init__(self):
		self.name = Player.names.pop()
		self.hand = []
		self.chips = Player.start_stack_sizes.copy()
		self.is_dealer = False

	def new_hand(self, hand):
		self.hand = hand

	def collect_pot(self, pot):
		for chip_type in pot:
			num_new_chips = pot[chip_type]
			self.chips[chip_type] += num_new_chips

	# when prompted to make a move: imperative is when you must do something
	def make_move(self, bets, table_cards, imperative):
		return 'fold'

	# returns best combination of hand and table cards found so far (flush, straight-flush, etc.)
	def get_hand_ranking(self):
		pass
