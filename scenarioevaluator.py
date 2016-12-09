
from deck import Cards
from collections import Counter

class Combo:

	def __init__(self):
		self.cards_involved = []

	def highest_card_rank(self):
		return max([Cards.get_rank(c) for c in self.cards_involved])

class CascadeCombo:

	def __init__(self):
		self.combos = []

	def highest_card_ranks(self):
		return tuple([combo.highest_card_rank() for combo in self.combos])

class Pair(Combo):

	def __init__(self, card_ind):
		Combo.__init__(self)
		self.cards_involved = [card_ind]

class TwoPair(CascadeCombo):

	def __init__(self, pair_cards):
		Combo.__init__(self)
		pair1 = Pair(pair_cards[0])
		pair2 = Pair(pair_cards[1])
		self.combos = [pair1, pair2]

class ThreeOfAKind(Combo):

	def __init__(self, card_ind):
		Combo.__init__(self)
		self.cards_involved = [card_ind]

class FullHouse(CascadeCombo):

	def __init__(self, pair_card, three_of_a_kind_card):
		CascadeCombo.__init__(self)
		pair = Pair(pair_card)
		toak = ThreeOfAKind(three_of_a_kind_card)
		self.combos = [toak, pair]

class FourOfAKind(Combo):

	def __init__(self, card_ind):
		Combo.__init__(self)
		self.cards_involved = [card_ind]

class Straight(Combo):
	
	def __init__(self, card_ind):
		Combo.__init__(self)
		self.cards_involved = [card_ind]

class Flush(Combo):
	pass

class StraightFlush(CascadeCombo):
	
	def __init__(self, straight_card):
		self.combos = [Straight(straight_card), Flush()]

class RoyalFlush(CascadeCombo):
	pass

class ScenarioEvaluator:

	# input: a list of hands of 2 cards
	# output: a set of the indeces of the winners
	@staticfunction
	def test_high_card(hands):
		max_card_rank = -1
		winner_indices = set()

		for i in range(len(hands)):
			hand = hands[i]
			rank = max(Cards.get_rank(hand[0]), Cards.get_rank(hand[1]))
			if rank == max_card_rank:
				winner_indices.add(i)
			elif rank > max_card_rank:
				winner_indices = set([i])
				max_card_rank = rank

		return winner_indices

	# tests for pair, 2 pair, 3 of a kind, full house, and 4 of a kind
	# input: hand of cards, cards on table
	# output: dictionary of 2,3,and 4 pairs example (output[2] = ['J','2'] or output[3] = ['K'])
	# 		  s.t. each list of n pairs is descending in the card rank of the index such as 'J'
	@staticfunction
	def get_pairs(hand, table_cards):
		freqs = Counter()

		for card in hand:
			freqs[card[0]] += 1

		for card in table_cards:
			freqs[card[0]] += 1

		pairs = [tup for tup in freqs.items() if tup[1] > 1]
		pairs_in_order = sorted(pairs, key=lambda t: (t[1], Cards.get_rank(t[0])), reverse=True)

		pair_dict = {2:[],3:[],4:[]}
		for pair in pairs_in_order:
			card_ind, pair_size = pair
			pair_dict[pair_size].append(card_ind)

		return pair_dict

	# input: pairs
	# output: pair card index or None if no pair
	@staticfunction
	def test_pair(pairs):
		if len(pairs[2]) == 1:
			return pairs[2][0]
		else:
			return None

	# input: pairs
	# output: highest 2 pairs of card index or None if less than 2 pairs
	@staticfunction
	def test_two_pair(pairs):
		if len(pairs[2]) > 1:
			return (pairs[2][0], pairs[2][1])
		else
			return None

	# input: pairs
	# output: highest 3 of a kind of card index or None if no 3 of a kind
	@staticfunction
	def test_three_of_a_kind(pairs):
		if len(pairs[3]) > 0:
			return pairs[3][0]
		else:
			return None

	# input: pairs
	# outpu: 4 of a kind of card index or None if no 4 of a kind
	@staticfunction
	def test_four_of_a_kind(pairs):
		if len(pairs[4]) == 1:
			return pairs[4][0]
		else:
			return None

	@staticfunction
	def test_straight(hand, table_cards):
		freq = Counter()

		for card in hand:
			freq[card[0]] += 1

		for card in table_cards:
			freq[card[0]] += 1

		lcs_index = -1
		lcs_length = 0
		for i in range(len(freq)-1, -1, -1):
			if lcs_length == 0:
				lcs_index = i
			else:
				if Cards.get_rank(freq.keys()[i]) == Cards.get_rank(freq.keys()[i+1]) - 1:
					lcs_length += 1

					if lcs_length == 5:
						break
				else:
					lcs_length = 0
					lcs_index = -1

		if lcs_length == 5:
			return freq.keys()[lcs_index]
		elif lcs_length == 4 and freq.keys()[lcs_index] == '5' and freq['A'] > 0:
			return freq.keys()[lcs_index]
		else:
			return None


	@staticfunction
	def test_flush(hand, table_cards):
		freq = Counter()

		for card in hand:
			suit = card[1]
			freq[suit] += 1

		for card in table_cards:
			suit = card[1]
			freq[suit] += 1

		flush = False
		for suit in freq:
			if freq[suit] == 5:
				flush = True
				break

		return flush

	@staticfunction
	def test_royal(hand, table_cards):
		royals = Cards.royals.copy()
		h = set([c[0] for c in hand])
		t = set([c[0] for c in table_cards])

		comb = h.union(t)

		return len(royals.intersection(comb)) == len(royals)

	# input: hands and table cards
	# output: tuple of indices of winning hands
	@staticfunction
	def rank_hands(hands, table_cards):
		max_card_rank = 1
		winner_indices = set()

		ranks = [ScenarioEvaluator.rank_hand(hand, table_cards) for hand in hands]

		for i in range(len(hands)):
			hand = hands[i]
			rank = ranks[i][0]
			if rank == max_card_rank:
				winner_indices.add(i)
			elif rank > max_card_rank:
				winner_indices = set([i])
				max_card_rank = rank

		if len(winner_indices) > 1:
			# break ties
			l_winner_indices = list(winner_indices)
			# check if combos is empty, if so, check high card
			combos = ranks[l_winner_indices[0]][1]
			if len(combos) < 1:
				winner_indices = set([l_winner_indices[j] for j in ScenarioEvaluator.test_high_card([hands[i] for i in l_winner_indices])])
			# if not, check whether cascade combo or regular combo
			elif len(combos) == 1:
				if isinstance(combos[0], Combo):
					# if regular combo, check only combo for higher combo
					second_rank = sorted([ranks[l_winner_indices[i]][1][0] for i in range(len(l_winner_indices))], key=lambda comb: comb.highest_card_rank(), reverse=True)
					max_val_second_rank = second_rank[0].highest_card_rank()
					winner_indices = set()
					for i in l_winner_indices:
						if ranks[i][1][0].highest_card_rank() == max_val_second_rank:
							winner_indices.add(i)

				elif isinstance(combos[0], CascadeCombo):
					# if cascade, check in order which has higher combo
					second_rank = sorted([ranks[l_winner_indices[i]][1][0] for i in range(len(l_winner_indices))], key=lambda comb: comb.highest_card_ranks(), reverse=True)
					max_val_second_rank = second_rank[0].highest_card_ranks()
					winner_indices = set()
					for i in l_winner_indices:
						is_a_winner = True
						for j in range(len(max_val_second_rank)):
							if rank[i][1][0][j] != max_val_second_rank[j]:
								is_a_winner = False
						if is_a_winner:
							winner_indices.add(i)

			# if still room left in 5 card best hand, check high card (CHECK THIS RULE FIRST, NOT SURE / HAVEN'T IMPLEMENTED)
			# if still a tie, split the pot among players

		return winner_indices

	@staticfunction
	def rank_hand(hand, table_cards):
		rank = 1 # 1 is worst
		combos = []

		s = ScenarioEvaluator.test_straight(hand, table_cards)
		f = ScenarioEvaluator.test_flush(hand, table_cards)

		if s is not None and f:
			if ScenarioEvaluator.test_royal(hand, table_cards):
				rank = max(rank, 10)
				combos.append(RoyalFlush())
			else:
				rank = max(rank, 9)
				combos.append(StraightFlush(s))
		else:
			if f:
				rank = max(rank, 6)
				combos.append(Flush())
			if s is not None:
				rank = max(rank, 5)
				combos.append(Straight(s))

		pairs = ScenarioEvaluator.get_pairs(hand, table_cards)

		one = ScenarioEvaluator.test_pair(pairs)
		two = ScenarioEvaluator.test_two_pair(pairs)
		three = ScenarioEvaluator.test_three_of_a_kind(pairs)
		four = ScenarioEvaluator.test_four_of_a_kind(pairs)

		full_house = (one is not None and three is not None)

		if two is not None:
			rank = max(rank, 3)
			combos.append(TwoPair(two))

		if full_house:
			rank = max(rank, 7)
			combos.append(FullHouse(one, three))
		else:
			if one is not None:
				rank = max(rank, 2)
				combos.append(Pair(one))

			if three is not None:
				rank = max(rank, 4)
				combos.append(ThreeOfAKind(three))

		if four is not None:
			rank = max(rank, 8)
			combos.append(FourOfAKind(four))


		return (rank, combos)




		
