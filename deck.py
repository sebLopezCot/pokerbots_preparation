
from heapq import *
from random import random
import numpy as np

class Cards:

	indeces = set(['2','3','4','5','6','7','8','9','J','Q','K','A'])
	ranks = {'2': 0,'3': 1,'4': 2,'5': 3,'6': 4,'7': 5,'8': 6,'9': 7,'J': 8,'Q': 9,'K': 10,'A': 11}
	suits = set(['H','D','C','S'])
	kinds = set([('2', 'H'), ('2', 'D'), ('2', 'C'), ('2', 'S'), ('3', 'H'), ('3', 'D'), 
	('3', 'C'), ('3', 'S'), ('4', 'H'), ('4', 'D'), ('4', 'C'), ('4', 'S'), ('5', 'H'), 
	('5', 'D'), ('5', 'C'), ('5', 'S'), ('6', 'H'), ('6', 'D'), ('6', 'C'), ('6', 'S'), 
	('7', 'H'), ('7', 'D'), ('7', 'C'), ('7', 'S'), ('8', 'H'), ('8', 'D'), ('8', 'C'), 
	('8', 'S'), ('9', 'H'), ('9', 'D'), ('9', 'C'), ('9', 'S'), ('J', 'H'), ('J', 'D'), 
	('J', 'C'), ('J', 'S'), ('Q', 'H'), ('Q', 'D'), ('Q', 'C'), ('Q', 'S'), ('K', 'H'), 
	('K', 'D'), ('K', 'C'), ('K', 'S'), ('A', 'H'), ('A', 'D'), ('A', 'C'), ('A', 'S')])

	@staticmethod
	def get_all_cards():
		return list(Cards.kinds)

	@staticmethod
	def get_rank(card):
		return Cards.ranks[card[0]]


class Deck:

	def __init__(self):
		self.cards = []
		self.shuffle()

	def get_top_card(self):
		return self.cards.pop()

	def shuffle(self):
		temp = []
		for card in Cards.get_all_cards():
			heappush(temp, (int(random() * 1000), card))

		self.cards = []
		while len(temp) > 0:
			self.cards.append(heappop(temp)[1])

	@staticmethod
	def levenshtein(source, target):
	    if len(source) < len(target):
	        return levenshtein(target, source)

	    # So now we have len(source) >= len(target).
	    if len(target) == 0:
	        return len(source)

	    # We call tuple() to force strings to be used as sequences
	    # ('c', 'a', 't', 's') - numpy uses them as values by default.
	    source = np.array(tuple(source))
	    target = np.array(tuple(target))

	    # We use a dynamic programming algorithm, but with the
	    # added optimization that we only need the last two rows
	    # of the matrix.
	    previous_row = np.arange(target.size + 1)
	    for s in source:
	        # Insertion (target grows longer than source):
	        current_row = previous_row + 1

	        # Substitution or matching:
	        # Target and source items are aligned, and either
	        # are different (cost of 1), or are the same (cost of 0).
	        current_row[1:] = np.minimum(
	                current_row[1:],
	                np.add(previous_row[:-1], target != s))

	        # Deletion (target grows shorter than source):
	        current_row[1:] = np.minimum(
	                current_row[1:],
	                current_row[0:-1] + 1)

	        previous_row = current_row

	    return previous_row[-1]

	def distance(self, other):
		temp = list(Cards.get_all_cards())
		mapping = {}
		for i in range(len(temp)):
			card = temp[i]
			mapping[card] = chr(65 + i)

		deckstr1 = ''
		deckstr2 = ''
		for card in self.cards:
			deckstr1 += mapping[card]

		for card in other.cards:
			deckstr2 += mapping[card]

		return Deck.levenshtein(deckstr1, deckstr2)


	def __str__(self):
		return '\n'.join(map(str, list(reversed(self.cards))))

	def __len__(self):
		return len(self.cards)
