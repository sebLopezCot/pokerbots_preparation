
from handevaluator import HandEvaluator
from numpy.random import choice
import numpy.e

class Player:

	names = set(['Cayla','Roxie','Anya','Kindra','Kittie','Kitty','Sonya','Mora',
		'Amada','Shawnee','Shizue','Shanti','Sherry','Miles','Martha','Marisela',
		'Reena','Edwin','Demetria','Lorrine','Jacques','Michele','Maryanna','Carson',
		'Nilsa','Tawnya','Vince','Heather','Necole','Mozelle','Sheilah','Rhoda','Rolf',
		'Eugene','Kizzie','Elinore','Bruno','Suk','Yoshiko','Sharie','Monique','Jasmine',
		'Meghan','Glennis','Vertie','Francesco','Isidro','Calvin','Elvia','Candie'])

	start_stack_sizes = {5: 20, 10: 10, 20: 5, 50: 4, 100: 1}

	def __init__(self):
		m_name = choice(list(Player.names))
		Player.names.remove(m_name)
		self.name = m_name
		self.hand = []
		self.chips = Player.start_stack_sizes.copy()
		self.is_dealer = False

	def new_hand(self, hand):
		self.hand = hand

	def deposit_chips(self, pot):
		for chip_type in pot:
			num_new_chips = pot[chip_type]
			self.chips[chip_type] += num_new_chips

	def can_commit(self, total):
		pass

	def max_bet(self):
		pass

	def withdraw_chips(self, denoms):
		pass

	# when prompted to make a move: imperative is when you must do something such as ('call', 50) or ('check', 0)
	# round_num: pre-flop, flop, turn, river
	def make_move(self, bets, round_num, num_other_players, table_cards, min_imperative):
		
		# TODO: move this logic to strategy class
		# Also should have a situation evaluator to aid strategy class
		hand_ranking = HandEvaluator.rank_hand(self.hand, table_cards)

		min_bet_size = min_imperative[1]

		if self.can_commit(min_bet_size):
			if round_num > 0 and hand_ranking >= 5:
				# bet
				x = hand_ranking
				risk_factor = 20.0 * (0.37 - 0.5 * (x+1) * numpy.e**(-0.5*(x+1)))
				risk_coeff = risk_factor / 10.5 # max value of rf is 6.95, so at most you throw away 2/3 of your chips in one move
				ideal_bet = self.max_bet() * risk_coeff / 9.0 # divide by 9 so you can keep going for 3 rounds
				actual_bet = int(5.0 * round(ideal_bet / 5.0)) # round to 5's place

				return ('raise', actual_bet)
			else:
				# such as 'check', note that we could change our strategy, but for now we will just check
				return min_imperative
		else:
			return ('fold', 0)
