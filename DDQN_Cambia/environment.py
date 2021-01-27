import numpy as np 


class Environment():
	def __init__ (self):
		self.deck = [i for i in range(1,13)] * 4 + [-1, -1, 0, 0, 13, 13]
		self.index = 0
		self.board = [-2 for i in range(8)]
		self.oppo_board = [-2 for i in range(8)]
		self.masterBoard = [-2 for i in range(8)]
		self.card = -2
		# self.state = np.array(self.board + [self.expectedValue(-2), -2, 0, 0])
		self.state = np.array(self.board + [self.expectedValue(-2), -2, 0])
		self.win_history = []
		self.win_percentage = []
		self.move_counter = 0
		self.episode_lengths = []

	def reshuffle(self):
		self.deck = [i for i in range(1,13)] * 4 + [-1, -1, 0, 0, 13, 13]
		np.random.shuffle(self.deck)
		self.index = 0
		removed_cards = []
		# print("Master board is ", self.masterBoard)
		for card in self.masterBoard:
			if card >= -1 and card in self.deck:
				# print("A removed card is ", card)
				self.deck.remove(card)	
				removed_cards.append(card)
		self.index = len(removed_cards)
		self.deck = removed_cards + self.deck			
	def eValHelper(self, x):
		avg = 0
		counter = 0
		for i in range(self.index, len(self.deck)):
			if (self.deck[i] <= x + 18):
				avg += self.deck[i]
				counter += 1 
		for i in range(8): 
			if ((self.board[i] <= -2) and self.masterBoard[i] != -4 and self.masterBoard[i] <= x + 18):
				avg += self.masterBoard[i]
				counter += 1
		avg = avg/counter if counter != 0 else 0
		return avg

	def expectedValue(self, x):
		if (x == -4):
			return 0
		if (-1 <= x <= 13):
			return x
		elif (-18 <= x <= -2):
			return (self.eValHelper(x) * 0.25 + self.eValHelper(-2) * 0.75) 
		else:
			print("State error, {} is included".format(x))
			return 14
	
	def validCard(self, val):
		return val >= -1 and val <= 13

	def find_worst_card(self, cards):
		worst_card_val = -2
		worst_card_index = -2
		for i in range(len(cards)):
			card_val = self.expectedValue(cards[i])
			card_val += 1 if cards[i] == -2 else 0
			card_val += 2 - (cards[i] + 3)/15 if cards[i] <= -3 else 0
			if cards[i] != -4 and card_val > worst_card_val: 
				worst_card_index = i
				worst_card_val = card_val
		return worst_card_index

	def find_best_card(self, cards):
		best_card_val = 18
		best_card_index = -1
		for i in range(len(cards)):
			card_val = self.expectedValue(cards[i])
			card_val += 1 if cards[i] == -2 else 0
			card_val += 2 - (cards[i] + 3)/15 if cards[i] <= -3 else 0
			if cards[i] != -4 and card_val < best_card_val: 
				best_card_index = i
				best_card_val = card_val
		return best_card_index

	def step1(self, action):
		reward = 0
		done = False 
		if action <= 0 or self.masterBoard[:4] == [-4, -4, -4, -4]: 
			if action == 0:
				# self.oppo_step()
				self.your_action(True)
				self.move_counter += 1
			your_cards = [(self.masterBoard[i] if self.masterBoard[i] != -4 else 0) for i in range(4)]
			oppo_cards = [(self.masterBoard[i] if self.masterBoard[i] != -4 else 0) for i in range(4, 8)]

			if sum(your_cards) <= sum(oppo_cards):
				reward += 50
				done = True
				self.win_history.append(1)
			else:
				reward += -50
				done = True
				self.win_history.append(0)
			self.episode_lengths.append(self.move_counter)

			self.win_percentage.append((sum(self.win_history)/len(self.win_history)) if len(self.win_history) != 0 else 0)
			# state_ = np.array(self.board + [self.expectedValue(-2), -2, 0, 0])
			state_ = np.array(self.board + [self.expectedValue(-2), -2, 0])
			self.state = state_
		else: 
			if self.index >= len(self.deck):
				self.reshuffle()
			self.card = self.deck[self.index]
			# print("Now self.card is ", self.card)
			self.index += 1
			# state_ = np.array(self.board + [self.expectedValue(-2), self.card, 0, 0])
			state_ = np.array(self.board + [self.expectedValue(-2), self.card, 0])
			self.state = state_
		return state_, reward, done

	def setIndexEmpty(self, index):
		self.board[index] = -4
		self.oppo_board[index] = -4
		self.masterBoard[index] = -4

	def swap(self, index1, index2):
		tmp = self.board[index1]
		self.board[index1] = self.board[index2]
		self.board[index2] = tmp
		tmp = self.oppo_board[index1]
		self.oppo_board[index1] = self.oppo_board[index2]
		self.oppo_board[index2] = tmp
		tmp = self.masterBoard[index1]
		self.masterBoard[index1] = self.masterBoard[index2]
		self.masterBoard[index2] = tmp

	def your_flip_card(self, played_card):
		if not self.validCard(played_card):
			print("Error you flipped card {}".format(played_card))
			return
		for i in range(4):
			if played_card == self.masterBoard[i]:	
				if self.board[i] == played_card:
					if played_card > 0 or self.oppo_board[i] == played_card:
						# print("You put {} down first on your side!".format(played_card))
						print("The opponent is flipping the card {} in slot {}".format(self.masterBoard[i], i))
						self.setIndexEmpty(i)
				elif self.oppo_board[i] == played_card:
					print("You are flipping the card {} on your opponent's board in slot {}".format(self.masterBoard[i], i))
					# print("Oppo put {} down first on your side!".format(played_card))
					oppo_worst_index = self.find_worst_card(self.oppo_board[4:]) + 4
					if oppo_worst_index != -2 and self.oppo_board[oppo_worst_index] != -1: 
						print("You are giving your opponent your card in slot {} to fill in their slot {}".format(oppo_worst_index, i))
						self.oppo_board[i] = self.oppo_board[oppo_worst_index]
						self.board[i] = self.board[oppo_worst_index]
						self.masterBoard[i] = self.masterBoard[oppo_worst_index]
						self.setIndexEmpty(oppo_worst_index)
		for i in range(4, 8):
			if played_card == self.masterBoard[i]:
				if self.board[i] == played_card and (self.oppo_board[i] != played_card or np.random.random() <= 0.5):
					print("The opponent is flipping the card {} on your board in slot {}".format(self.masterBoard[i], i))
					# print("You put {} down first on oppo side!".format(played_card))
					your_worst_index = self.find_worst_card(self.board[:4])
					if your_worst_index != -2 and self.board[your_worst_index] != -1:
						print("The opponent is giving you their card in slot {} to fill in the slot {}".format(your_worst_index, i))
						self.board[i] = self.board[your_worst_index]
						self.oppo_board[i] = self.oppo_board[your_worst_index]
						self.masterBoard[i] = self.masterBoard[your_worst_index]
						self.setIndexEmpty(your_worst_index)
				elif self.oppo_board[i] == played_card:
					# print("Oppo put {} down first on oppo side!".format(played_card))
					print("You are flipping the card {} in slot {}".format(self.masterBoard[i], i))
					self.setIndexEmpty(i)

	def highest_priority(self, cards):
		highest_priority = self.find_worst_card(cards)
		worst_unknown_expected = -2
		for i in range(len(cards)):
			if cards[i] == -2 and self.expectedValue(cards[i]) > worst_unknown_expected:
				highest_priority = i
				worst_unknown_expected = self.expectedValue(cards[i])
		worst_unknown_expected = -2
		for i in range(len(cards)):
			if cards[i] < -3 and self.expectedValue(cards[i]) > worst_unknown_expected:
				highest_priority = i
				worst_unknown_expected = self.expectedValue(cards[i])
		worst_unknown_expected = -2
		for i in range(len(cards)):
			if cards[i] == -3 and self.expectedValue(cards[i]) > worst_unknown_expected:
				highest_priority = i
				worst_unknown_expected = self.expectedValue(cards[i])
		return highest_priority

	def highest_priority_take(self, cards):
		highest_priority = self.find_best_card(cards)
		best_unknown_expected = 18
		for i in range(len(cards)):
			if cards[i] == -3 and self.expectedValue(cards[i]) < best_unknown_expected:
				highest_priority = i
				best_unknown_expected = self.expectedValue(cards[i])
		best_unknown_expected = 18
		for i in range(len(cards)):
			if cards[i] < -3 and self.expectedValue(cards[i]) < best_unknown_expected:
				highest_priority = i
				best_unknown_expected = self.expectedValue(cards[i])
		best_unknown_expected = 18
		for i in range(len(cards)):
			if cards[i] == -2 and self.expectedValue(cards[i]) < best_unknown_expected:
				highest_priority = i
				best_unknown_expected = self.expectedValue(cards[i])
		return highest_priority

	def your_card_ability(self, played_card):
		if not self.validCard(played_card):
			print("Error you played card {}".format(played_card))
			return
		if played_card <= 6 and played_card >= 0:
			return
		print_board = [i if self.oppo_board[i] != -4 else "_" for i in range(8)]
		print("The board currently is: ", print_board)
		if played_card == 7 or played_card == 8:
			highest_priority = self.highest_priority(self.board[:4])
			self.board[highest_priority] = self.masterBoard[highest_priority]
			self.oppo_board[highest_priority] = -3 if self.oppo_board[highest_priority] == -2 else self.oppo_board[highest_priority]
			print("Your opponent looked at the card in the {} slot on their own board".format(highest_priority))
		if played_card == 9 or played_card == 10:
			highest_priority = self.highest_priority_take(self.board[4:]) + 4
			self.board[highest_priority] = self.masterBoard[highest_priority]
			self.oppo_board[highest_priority] = -3 if self.oppo_board[highest_priority] == -2 else self.oppo_board[highest_priority]
			print("Your opponent looked at the card in the {} slot on your board".format(highest_priority))

		if played_card == 11 or played_card == 12:
			your_worst_index = self.find_worst_card(self.board[:4])
			oppo_best_index = self.find_best_card(self.board[4:]) + 4

			your_val = self.expectedValue(self.board[your_worst_index]) 
			your_val += 1 if self.board[your_worst_index] == -2 else 0
			your_val += 2 + (self.board[your_worst_index] + 3)/15 if self.board[your_worst_index] <= -3 else 0
			oppo_val = self.expectedValue(self.board[oppo_best_index]) 
			oppo_val += 1 if self.board[oppo_best_index] == -2 else 0
			oppo_val += 2 - (self.board[oppo_best_index] + 3)/15 if self.board[oppo_best_index] <= -3 else 0

			if your_val > oppo_val and self.board[your_worst_index] != -4 and self.board[oppo_best_index] != -4: 
				self.swap(your_worst_index, oppo_best_index)
				print("Your opponent is swapping the indices {} and {}".format(your_worst_index, oppo_best_index))
				print_board[your_worst_index] = oppo_best_index
				print_board[oppo_best_index] = your_worst_index
			print("Now the board now is: ", print_board)
		if played_card == 13 or played_card == -1:
			your_worst_index = self.find_worst_card(self.board[:4])
			your_highest_priority = self.highest_priority(self.board[:4])
			if self.expectedValue(self.board[your_worst_index]) <= self.expectedValue(self.board[your_highest_priority]) + 4:
				your_worst_index = your_highest_priority
			oppo_best_index = self.find_best_card(self.board[4:]) + 4
			oppo_highest_priority = self.highest_priority_take(self.board[4:]) + 4
			if self.expectedValue(self.board[oppo_best_index]) >= self.expectedValue(self.board[oppo_highest_priority]) - 4:
				oppo_best_index = oppo_highest_priority
			self.board[your_worst_index] = self.masterBoard[your_worst_index]
			self.oppo_board[your_worst_index] = -3 if self.oppo_board[your_worst_index] == -2 else self.oppo_board[your_worst_index]
			print("Your opponent looked at the card in the {} slot on their own board".format(your_worst_index))

			self.board[oppo_best_index] = self.masterBoard[oppo_best_index]
			self.oppo_board[oppo_best_index] = -3 if self.oppo_board[oppo_best_index] == -2 else self.oppo_board[oppo_best_index]
			print("Your opponent looked at the card in the {} slot on your board".format(oppo_best_index))

			if (self.board[your_worst_index] > self.board[oppo_best_index]):
				self.swap(your_worst_index, oppo_best_index)
				print("Your opponent is swapping the indices {} and {}".format(your_worst_index, oppo_best_index))
				print_board[your_worst_index] = oppo_best_index
				print_board[oppo_best_index] = your_worst_index
			print("Now the board now is: ", print_board)

	def board_reward(self, old_board):
		reward = 0
		for i in range(4):
			if old_board[i] != self.board[i]:
				if not self.validCard(self.board[i]):
					reward -= 1 if self.board[i] == -2 else 0
					reward -= 2 - (self.board[i] + 3)/15 if self.board[i] <= -3 and self.board[i] != -4 else 0
				if not self.validCard(old_board[i]):
					reward += 1 if old_board[i] == -2 else 0
					reward += 2 - (old_board[i] + 3)/15 if old_board[i] <= -3 and old_board[i] != -4 else 0
				reward += self.expectedValue(old_board[i]) - self.expectedValue(self.board[i]) 
		oppo_improvement = 0
		for i in range(4, 8):
			if old_board[i] != self.board[i]:
				if not self.validCard(self.board[i]):
					oppo_improvement -= 1 if self.board[i] == -2 else 0
					oppo_improvement -= 2 - (self.board[i] + 3)/15 if self.board[i] <= -3 and self.board[i] != -4 else 0
				if not self.validCard(old_board[i]):
					oppo_improvement += 1 if old_board[i] == -2 else 0
					oppo_improvement += 2 - (old_board[i] + 3)/15 if old_board[i] <= -3 and old_board[i] != -4 else 0
				oppo_improvement += min(self.expectedValue(old_board[i]) - self.expectedValue(self.board[i]), 0)

		reward -= oppo_improvement/2
		return reward

	def step2(self, action):
		done = bool(self.state[-1])
		old_board = self.board.copy()
		print_board = [i if self.oppo_board[i] != -4 else "_" for i in range(8)]
		print("The board before your opponent plays their card is: ", print_board)
		# print("We pulled the card ", self.card)
		if action < 4 and self.masterBoard[action] != -4: 
			played_card = self.masterBoard[action]
			self.board[action] = self.card 
			self.oppo_board[action] = -3 # if self.oppo_board[action] == -2 else self.oppo_board[action]
			self.masterBoard[action] = self.card
			print("Your opponent is playing the card in slot {} on their board".format(action))
		else:
			played_card = self.card
			print("Your opponent is playing the card in their hand.")
		# print("We are playing the card ", played_card)
		print("Your opponent is playing the card: ", played_card)
		self.your_flip_card(played_card)
		self.your_card_ability(played_card)
		# card_has_ability = self.validCard(played_card) and (played_card >= 7 or played_card <= -1)
		# done = (not card_has_ability) and done 
		# oppo_cambia = False
		# if not done and not card_has_ability:
		# oppo_cambia = self.oppo_step()
		oppo_cambia = self.your_action(done)
			# oppo_cambia = self.your_action()
		self.move_counter += 1


		reward = self.board_reward(old_board)
		# state_ = np.array(self.board + [self.expectedValue(-2), played_card if card_has_ability else -2, int(card_has_ability), int(oppo_cambia)])
		state_ = np.array(self.board + [self.expectedValue(-2), -2, int(oppo_cambia)])
		if done:
			_, new_reward, _ = self.step1(-1)
			reward += new_reward
		self.state = state_
		# print("The reward is ", reward)

		return state_, reward, done

	def step3(self, action):
		done = bool(self.state[-1])
		old_board = self.board.copy()
		# print("We pulled the card ", self.card)
		# played_card = self.state[-3]
		played_card = self.state[-2]
		if played_card == 7 or played_card == 8:
			index = action % 4
			if self.validCard(self.board[index]) or self.board[index] == -4:
				for i in range(4):
					if not self.validCard(self.board[i]) and self.board[i] != -4:
						index = i
						break
				self.board[index] = self.masterBoard[index]
				self.oppo_board[index] = -3 if self.oppo_board[index] == -2 else self.oppo_board[index]
		if played_card == 9 or played_card == 10:
			index = (action % 4) + 4
			if self.validCard(self.board[index]) or self.board[index] == -4:
				for i in range(4, 8):
					if not self.validCard(self.board[i]) and self.board[i] != -4:
						index = i
						break
				self.board[index] = self.masterBoard[index]
				self.oppo_board[index] = -3 if self.oppo_board[index] == -2 else self.oppo_board[index]

		if played_card == 11 or played_card == 12:
			your_index = action % 4
			oppo_index = int(action/4)
			self.swap(your_index, oppo_index)

		if played_card == 13 or played_card == -1:
			your_index = action % 4 
			oppo_index = int(action/4)
			self.board[your_index] = self.masterBoard[your_index]
			self.oppo_board[your_index] = -3 if self.oppo_board[your_index] == -2 else self.oppo_board[your_index]
			self.board[oppo_index] = self.masterBoard[oppo_index]
			self.oppo_board[oppo_index] = -3 if self.oppo_board[oppo_index] == -2 else self.oppo_board[oppo_index]

		oppo_cambia = done
		if not done:
			oppo_cambia = self.oppo_step()
			self.move_counter += 1

		reward = self.board_reward(old_board)	
		# state_ = np.array(self.board + [self.expectedValue(-2), -2, 0, oppo_cambia])
		state_ = np.array(self.board + [self.expectedValue(-2), -2, oppo_cambia])

		if done:
			_, new_reward, _ = self.step1(-1)
			reward += new_reward
		self.state = state_
		# print("The reward is ", reward)

		return state_, reward, done

	def step(self, action):
		if self.state[-1] and not self.validCard(self.state[-2]): # and not self.state[-2]:
			if self.index >= len(self.deck):
				self.reshuffle()
			self.card = self.deck[self.index]
			self.index += 1
			# self.state[-3] = self.card
			self.state[-2] = self.card

		if self.state[-2] == -2: #self.state[-3] == -2:
			self.move_counter += 1
			return self.step1(action)
		else:
			return self.step2(action)
		# elif not self.state[-2]:
		# 	return self.step2(action)
		# else:
		# 	return self.step3(action)

	def reset(self):
		np.random.shuffle(self.deck)
		self.board = [self.deck[0], self.deck[1], -2, -2, -2, -2, -3, -3] # -2 indicates neither player knows, -3 indicates opponent knows but you do not 
		self.oppo_board = [-3, -3, -2, -2, -2, -2, self.deck[6], self.deck[7]]
		self.masterBoard = [self.deck[i] for i in range(8)]
		self.index = 8
		# self.state = np.array(self.board + [self.expectedValue(-2), -2, 0, 0])
		self.state = np.array(self.board + [self.expectedValue(-2), -2, 0])
		self.move_counter = 0
		return self.state 

	def oppo_flip_card(self, played_card):	
		if not self.validCard(played_card):
			print("Error oppo played card {}".format(played_card))
			return
		for i in range(4, 8):
			if played_card == self.masterBoard[i]:	
				if self.oppo_board[i] == played_card:
					if played_card > 0 or self.board[i] == played_card:
						# print("Oppo put {} down first on oppo side!".format(played_card))
						print("You are flipping the card {} in slot {}".format(self.masterBoard[i], i))
						self.setIndexEmpty(i)
				elif self.board[i] == played_card:
					# print("You put {} down first on oppo side!".format(played_card))
					print("Your opponent is flipping the card {} on your board in slot {}".format(self.masterBoard[i], i))
					your_worst_index = self.find_worst_card(self.board[:4])
					if your_worst_index != -2 and self.board[your_worst_index] != -1:
						print("Your opponent is giving you the card in slot {} to fill in your slot {}".format(your_worst_index, i))
						self.board[i] = self.board[your_worst_index]
						self.oppo_board[i] = self.oppo_board[your_worst_index]
						self.masterBoard[i] = self.masterBoard[your_worst_index]
						self.setIndexEmpty(your_worst_index)

		for i in range(4):
			if played_card == self.masterBoard[i]:
				if self.oppo_board[i] == played_card and (self.board[i] != played_card or np.random.random() <= 0.5):
					# print("Oppo put {} down first on your side!".format(played_card))
					print("You are flipping the card {} on your opponent's board in slot {}".format(self.masterBoard[i], i))
					oppo_worst_index = self.find_worst_card(self.oppo_board[4:]) + 4
					if oppo_worst_index != -2 and self.oppo_board[oppo_worst_index] != -1:
						print("You are giving your opponent the card in slot {} to fill in their slot {}".format(oppo_worst_index, i))
						self.board[i] = self.board[oppo_worst_index]
						self.oppo_board[i] = self.oppo_board[oppo_worst_index]
						self.masterBoard[i] = self.masterBoard[oppo_worst_index]
						self.setIndexEmpty(oppo_worst_index)
				elif self.board[i] == played_card:
					# print("You put {} down first on your side!".format(played_card))
					print("The opponent is flipping the card {} in slot {}".format(self.masterBoard[i], i))
					self.setIndexEmpty(i)

		# if not self.validCard(played_card):
		# 	print("Error you played card {}".format(played_card))
		# 	return
		# for i in range(4, 8):
		# 	if played_card == self.oppo_board[i]:
		# 		self.setIndexEmpty(i)
		# for i in range(4):
		# 	if played_card == self.oppo_board[i] and self.validCard(self.board[i]):
		# 		oppo_win_flip = np.random.random() <= 0.5
		# 		print(oppo_win_flip)

		# 	if played_card == self.oppo_board[i]:
		# 		if not self.validCard(self.board[i]) or oppo_win_flip:
		# 			oppo_worst_index = self.find_worst_card(self.oppo_board[:4])
		# 			self.oppo_board[i] = self.oppo_board[oppo_worst_index]
		# 			self.board[i] = self.board[oppo_worst_index]
		# 			self.masterBoard[i] = self.masterBoard[oppo_worst_index]
		# 			self.setIndexEmpty(oppo_worst_index)

		# 		else:
		# 			self.setIndexEmpty(i)

	def oppo_step1(self):
		oppo_sum = sum([self.expectedValue(self.oppo_board[i]) for i in range(4, 8)])
		your_sum = sum([self.expectedValue(self.oppo_board[i]) for i in range(4)])
		your_sum -= (13 - (self.expectedValue(-2))) * min(2, sum([(1 if self.oppo_board[i] != -4 else 0) for i in range(4)]))
		if oppo_sum < your_sum or self.oppo_board[4:] == [-4, -4, -4, -4]: 
			# print("Oppo is calling cambia ", self.oppo_board, oppo_sum, your_sum)
			return -2
		else:
			self.index += 1
			if (self.index > len(self.deck)):
				self.reshuffle()
			return self.deck[self.index-1]

	def oppo_card_ability(self, played_card):
		if not self.validCard(played_card):
			# print("Error you played card {}".format(played_card))
			return
		if played_card <= 6 and played_card >= 0:
			return
		if played_card == 7 or played_card == 8:
			oppo_highest_priority = self.highest_priority(self.oppo_board[4:]) + 4
			self.oppo_board[oppo_highest_priority] = self.masterBoard[oppo_highest_priority]
			self.board[oppo_highest_priority] = -3 if self.board[oppo_highest_priority] == -2 else self.board[oppo_highest_priority]

		if played_card == 9 or played_card == 10:
			oppo_highest_priority = self.highest_priority_take(self.board[:4])
			self.oppo_board[oppo_highest_priority] = self.masterBoard[oppo_highest_priority]
			self.board[oppo_highest_priority] = -3 if self.board[oppo_highest_priority] == -2 else self.board[oppo_highest_priority]

		if played_card == 11 or played_card == 12:
			your_best_index = self.find_best_card(self.oppo_board[:4])
			oppo_worst_index = self.find_worst_card(self.oppo_board[4:]) + 4

			your_val = self.expectedValue(self.oppo_board[your_best_index]) 
			your_val += 1 if self.oppo_board[your_best_index] == -2 else 0
			your_val += 2 + (self.oppo_board[your_best_index] + 3)/15 if self.oppo_board[your_best_index] <= -3 else 0
			oppo_val = self.expectedValue(self.oppo_board[oppo_worst_index]) 
			oppo_val += 1 if self.oppo_board[oppo_worst_index] == -2 else 0
			oppo_val += 2 - (self.oppo_board[oppo_worst_index] + 3)/15 if self.oppo_board[oppo_worst_index] <= -3 else 0

			if your_val < oppo_val and self.oppo_board[your_best_index] != -4 and self.oppo_board[oppo_worst_index] != -4:
				self.swap(your_best_index, oppo_worst_index)

		if played_card == 13 or played_card == -1:
			oppo_worst_index = self.find_worst_card(self.oppo_board[4:]) + 4
			oppo_highest_priority = self.highest_priority(self.oppo_board[4:]) + 4
			if self.expectedValue(self.oppo_board[oppo_worst_index]) <= self.expectedValue(self.oppo_board[oppo_highest_priority]) + 4:
				oppo_worst_index = oppo_highest_priority
			your_best_index = self.find_best_card(self.oppo_board[:4])
			your_highest_priority = self.highest_priority_take(self.oppo_board[:4])
			if self.expectedValue(self.oppo_board[your_best_index]) >= self.expectedValue(self.oppo_board[your_highest_priority]) - 4:
				your_best_index = your_highest_priority
			self.oppo_board[oppo_worst_index] = self.masterBoard[oppo_worst_index]
			self.board[oppo_worst_index] = -3 if self.board[oppo_worst_index] == -2 else self.board[oppo_worst_index]
			self.oppo_board[your_best_index] = self.masterBoard[your_best_index]
			self.board[your_best_index] = -3 if self.board[your_best_index] == -2 else self.board[your_best_index]
			
			if (self.oppo_board[oppo_worst_index] > self.oppo_board[your_best_index]):
				# if not self.validCard(self.board[your_best_index]) and self.validCard(self.board[oppo_worst_index]):
				# 	if self.board[oppo_worst_index] <= 12:
				# 		self.board[your_best_index] = self.board[oppo_worst_index] - 17
				self.swap(oppo_worst_index, your_best_index)
			# else:
			# 	if self.validCard(self.board[your_best_index]) and not self.validCard(self.board[oppo_worst_index]):
			# 		if self.board[your_best_index] <= 12:
			# 			self.board[oppo_worst_index] = self.board[your_best_index] - 17


	def oppo_step2(self, oppo_card):
		# print("Oppo pulled the card ", oppo_card)
		oppo_worst_index = self.find_worst_card(self.oppo_board[4:]) + 4
		if oppo_card < self.expectedValue(self.oppo_board[oppo_worst_index]) + (1 if self.oppo_board[oppo_worst_index] <= -2 else 0):
			played_card = self.masterBoard[oppo_worst_index]
			# if self.board[oppo_worst_index] == -3:
			# 	self.board[oppo_worst_index] = played_card - 17
				# print("Now the board is ", self.board)
			self.oppo_board[oppo_worst_index] = oppo_card
			self.board[oppo_worst_index] = -3 # if self.board[oppo_worst_index] == -2 else self.board[oppo_worst_index]
			self.masterBoard[oppo_worst_index] = oppo_card

		else:
			played_card = oppo_card
		# print("Oppo is playing the card ", played_card)
		self.oppo_flip_card(played_card)
		self.oppo_card_ability(played_card)

	def oppo_step(self):
		oppo_card = self.oppo_step1()
		if oppo_card != -2:
			self.oppo_step2(oppo_card)
			return False
		return True

	def your_action(self, oppo_cambia):
		print("\n\n\n\n\n\n\n\n\n\n------------------------------------------------------------------------\n")
		if oppo_cambia:
			print("The opponent called cambia. You have one turn left.")
		else:
			cambia = input("Do you want to call cambia? (yes/no): ")
			if cambia == "yes" or cambia == 1 or cambia == "Yes" or cambia == "Y" or cambia == "y":
				return True
		if self.index >= len(self.deck):
			self.reshuffle()
		self.card = self.deck[self.index]
		self.index += 1
		print_board = [i if self.oppo_board[i] != -4 else "_" for i in range(8)]
		print("The board is originally: ", print_board)
		print("Your card is: ", self.card)
		print("Your board is: \n {}                   {} \n {}                   {} \n where _ represents an empty slot".format(0 if self.oppo_board[4] != -4 else "_", 1 if self.oppo_board[5] != -4 else "_", 2 if self.oppo_board[6] != -4 else "_", 3 if self.oppo_board[7] != -4 else "_"))
		card_index = input("If you want to play your card press enter. Otherwise enter the number of the card you on your board that you want to flip. Input your action: ")
		card_index = int(card_index) if card_index != "" else -1
		while(card_index >= 0 and card_index < 4 and self.masterBoard[card_index+4] == -4):
			card_index = input("Your input was not valid. If you want to play your card enter 5. Otherwise enter the number of the card you on your board that you want to flip. Input your action: ")
			card_index = int(card_index) if card_index != "" else -1
		card_index += 4
		if card_index < 8 and card_index >= 5: 
			played_card = self.masterBoard[card_index]
			self.board[card_index] = -3
			self.oppo_board[card_index] = self.card
			self.masterBoard[card_index] = self.card 
		else:
			played_card = self.card
		print("Now you are flipping the card: ", played_card)
		print_board = [i if self.oppo_board[i] != -4 else "_" for i in range(8)]
		print("The board before you play your card is: ", print_board)
		self.oppo_flip_card(played_card)
		if played_card == 7 or played_card == 8:
			print("Your board is: \n {}                   {} \n {}                   {} \n where _ represents an empty slot".format(0 if self.oppo_board[4] != -4 else "_", 1 if self.oppo_board[5] != -4 else "_", 2 if self.oppo_board[6] != -4 else "_", 3 if self.oppo_board[7] != -4 else "_"))
			card_index = input("You can look at one of your own cards. Please enter the number of the card you on your board that you want to flip. Input your action: ")
			card_index = int(card_index) if card_index != "" else -1
			while(card_index >= 0 and card_index < 4 and self.masterBoard[card_index+4] == -4):
				card_index = input("Your input was not valid. Please enter the number of the card you on your board that you want to flip. Input your action: ")
				card_index = int(card_index) if card_index != "" else -1
			card_index += 4
			print("Your card is: {}".format(self.masterBoard[card_index]))
			if card_index >= 4 and card_index < 8:
				self.oppo_board[card_index] = self.masterBoard[card_index]
				self.board[card_index] = -3 if self.board[card_index] == -2 else self.board[card_index]

		if played_card == 9 or played_card == 10:
			print("Your opponent's board is: \n {}                   {} \n {}                   {} \n where _ represents an empty slot".format(0 if self.oppo_board[1] != -4 else "_", 1 if self.oppo_board[2] != -4 else "_", 2 if self.oppo_board[3] != -4 else "_", 3 if self.oppo_board[4] != -4 else "_"))
			card_index = input("You can look at one of your opponent's cards. Please enter the number of the card you on the opponent's board that you want to flip. Input your action: ")
			card_index = int(card_index) if card_index != "" else -1
			while(card_index >= 0 and card_index < 4 and self.masterBoard[card_index] == -4):
				card_index = input("Your input was not valid. Please enter the number of the card you on the opponent's board that you want to flip. Input your action: ")
				card_index = int(card_index) if card_index != "" else -1
			print("The opponent's card is: {}".format(self.masterBoard[card_index]))
			if card_index >= 0 and card_index < 4:
				self.oppo_board[card_index] = self.masterBoard[card_index]
				self.board[card_index] = -3 if self.board[card_index] == -2 else self.board[card_index]

		if played_card == 11 or played_card == 12:
			print("Your board is: \n {}                   {} \n {}                   {} \n where _ represents an empty slot".format(0 if self.oppo_board[4] != -4 else "_", 1 if self.oppo_board[5] != -4 else "_", 2 if self.oppo_board[6] != -4 else "_", 3 if self.oppo_board[7] != -4 else "_"))
			card_index = input("You can choose one of your cards (0-3) to swap or your can press enter to not swap. Please enter the number of the card you on your board that you want to flip. Input your action: ")
			card_index = int(card_index) if card_index != "" else -1
			while(card_index >= 0 and card_index < 4 and self.masterBoard[card_index+4] == -4):
				card_index = input("Your input was not valid. Please enter the number of the card you on your board that you want to flip. Input your action: ")
				card_index = int(card_index) if card_index != "" else -1
			card_index += 4
			if card_index >= 4 and card_index < 8:
				print("Your opponent's board is: \n {}                   {} \n {}                   {} \n where _ represents an empty slot".format(0 if self.oppo_board[1] != -4 else "_", 1 if self.oppo_board[2] != -4 else "_", 2 if self.oppo_board[3] != -4 else "_", 3 if self.oppo_board[4] != -4 else "_"))
				comp_card_index = input("You can look at one of your opponent's cards. Please enter the number of the card you on the opponent's board that you want to flip. Input your action: ")
				comp_card_index = int(comp_card_index) if comp_card_index != "" else -1
				while(comp_card_index >= 0 and comp_card_index < 4 and self.masterBoard[comp_card_index] == -4):
					comp_card_index = input("Your input was not valid. Please enter the number of the card you on the opponent's board that you want to flip. Input your action: ")
					comp_card_index = int(comp_card_index) if comp_card_index != "" else -1
				if comp_card_index >= 0 and comp_card_index < 4:
					self.swap(card_index, comp_card_index)

		if played_card == 13 or played_card == -1:
			print("Your board is: \n {}                   {} \n {}                   {} \n where _ represents an empty slot".format(0 if self.oppo_board[4] != -4 else "_", 1 if self.oppo_board[5] != -4 else "_", 2 if self.oppo_board[6] != -4 else "_", 3 if self.oppo_board[7] != -4 else "_"))
			card_index = input("You can look at one of your own cards. Please enter the number of the card you on your board that you want to flip. Input your action: ")
			card_index = int(card_index) if card_index != "" else -1
			while(card_index >= 0 and card_index < 4 and self.masterBoard[card_index+4] == -4):
				card_index = input("Your input was not valid. Please enter the number of the card you on your board that you want to flip. Input your action: ")
				card_index = int(card_index) if card_index != "" else -1
			card_index += 4
			if card_index >= 4 and card_index < 8:
				print("Your card is: {}".format(self.masterBoard[card_index]))
				self.oppo_board[card_index] = self.masterBoard[card_index]
				self.board[card_index] = -3 if self.board[card_index] == -2 else self.board[card_index]

				print("Your opponent's board is: \n {}                   {} \n {}                   {} \n where _ represents an empty slot".format(0 if self.oppo_board[1] != -4 else "_", 1 if self.oppo_board[2] != -4 else "_", 2 if self.oppo_board[3] != -4 else "_", 3 if self.oppo_board[4] != -4 else "_"))
				comp_card_index = input("You can look at one of your opponent's cards. Please enter the number of the card you on the opponent's board that you want to flip. Input your action: ")
				comp_card_index = int(comp_card_index) if comp_card_index != "" else -1
				while(comp_card_index >= 0 and comp_card_index < 4 and self.masterBoard[comp_card_index+4] == -4):
					comp_card_index = input("Your input was not valid. Please enter the number of the card you on the opponent's board that you want to flip. Input your action: ")
					comp_card_index = int(comp_card_index) if comp_card_index != "" else -1
				if comp_card_index >= 0 and comp_card_index < 4:
					print("The opponent's card is: {}".format(self.masterBoard[comp_card_index]))
					self.oppo_board[comp_card_index] = self.masterBoard[comp_card_index]
					self.board[comp_card_index] = -3 if self.board[comp_card_index] == -2 else self.board[comp_card_index]
					decision = input("Do you want to swap the cards? (yes/no): ")
					if decision == "yes" or decision == 1 or decision == "Yes" or decision == "Y" or decision == "y":
						self.swap(card_index, comp_card_index)
		print("\n------------------------------------------------------------------------\n\n\n\n\n\n\n\n\n\n")
		return False



if __name__ == '__main__':
	env = Environment()
	env.reset()
	print("\n ******************** TEST 1 ******************** \n")
	print(env.deck)
	print(env.board, env.masterBoard)
	print(env.expectedValue(2), env.expectedValue(10))
	print(env.expectedValue(-4), env.expectedValue(-2))
	print(env.expectedValue(-18), env.expectedValue(14))

	print("\n ******************** TEST 2 ******************** \n")
	print(env.board, env.oppo_board, env.masterBoard)
	print([env.expectedValue(env.board[i]) for i in range(4)])
	print([env.expectedValue(env.board[i]) for i in range(4, 8)])
	print("My worst card is: ", env.find_worst_card(env.board[:4]))
	print("Oppo worst card is: ", env.find_worst_card(env.board[4:]))
	print("My best card is: ", env.find_best_card(env.board[:4]))
	print("Oppo best card is: ", env.find_best_card(env.board[4:]))
	print(env.board, env.oppo_board, env.masterBoard)
	env.reshuffle()
	print(env.deck, env.index)
	print("\n ******************** TEST 3 ******************** \n")
	print("Initial setup: ", env.board, env.oppo_board, env.masterBoard, env.state, env.card)
	print(env.step1(0))
	print("Boards and card after action 0: ", env.board, env.oppo_board, env.masterBoard, env.card)
	env.swap(5, 2)
	print(env.step1(0))
	print("Boards and card after action 0: ", env.board, env.oppo_board, env.masterBoard, env.card)
	env.setIndexEmpty(1)
	env.setIndexEmpty(6)
	print(env.step1(2))
	print("Boards and card after action 1: ", env.board, env.oppo_board, env.masterBoard, env.card)
	env.reshuffle()
	print(env.deck, env.index)
	print("\n ******************** TEST 4 ******************** \n")
	env.reset()
	print(env.deck)
	print(env.board, env.masterBoard)
	env.your_flip_card(-3)
	print("Boards: ", env.board, env.oppo_board, env.masterBoard)
	env.your_flip_card(5)
	print("Boards: ", env.board, env.oppo_board, env.masterBoard) 
	env.your_flip_card(env.board[0])
	print("Boards: ", env.board, env.oppo_board, env.masterBoard)
	env.board[6] = env.masterBoard[6]
	env.oppo_board[6] = -3
	env.your_flip_card(env.board[6])
	print("Boards: ", env.board, env.oppo_board, env.masterBoard)
	env.board[3] = -3
	env.oppo_board[3] = env.masterBoard[3]
	env.your_flip_card(env.oppo_board[3])
	print("Boards: ", env.board, env.oppo_board, env.masterBoard)

	env.reset()
	print(env.deck)
	print(env.board, env.masterBoard)
	env.oppo_flip_card(-3)
	print("Boards after playing -3: ", env.board, env.oppo_board, env.masterBoard)
	env.oppo_flip_card(5)
	print("Boards after playing 5: ", env.board, env.oppo_board, env.masterBoard)
	env.oppo_flip_card(env.board[0])
	print("Boards after playing {}: ".format(env.board[0]), env.board, env.oppo_board, env.masterBoard)
	env.board[6] = env.masterBoard[6]
	env.oppo_board[6] = -3
	env.oppo_flip_card(env.board[6])
	print("Boards after playing {}: ".format(env.board[6]), env.board, env.oppo_board, env.masterBoard)
	env.board[3] = -3
	env.oppo_board[3] = env.masterBoard[3]
	env.your_flip_card(env.oppo_board[3])
	print("Boards after playing {}: ".format(env.oppo_board[3]), env.board, env.oppo_board, env.masterBoard)

	print("\n ******************** TEST 5 ******************** \n")
	env.reset()
	print(env.deck)
	print(env.board, env.masterBoard)
	print(env.highest_priority(env.board[:4]), env.highest_priority(env.board[4:]) + 4)
	env.board[3] = -3
	env.oppo_board[3] = env.masterBoard[3]
	print(env.highest_priority(env.board[:4]), env.highest_priority(env.board[4:]) + 4)
	print(env.board, env.masterBoard)

	env.your_card_ability(-2)
	print("After playing -2 the board is now: ", env.board, env.oppo_board, env.masterBoard)
	env.your_card_ability(3)
	print("After playing 3 the board is now: ", env.board, env.oppo_board, env.masterBoard)
	for j in range(1):
		for i in range(7, 14):
			env.your_card_ability(i)
			print("After playing {} the board is now: ".format(i), env.board, env.oppo_board, env.masterBoard)
	env.reshuffle()
	print(env.deck, env.index)
	print("\n ******************** TEST 6 ******************** \n")
	env.reset()
	print(env.deck)
	print(env.board, env.masterBoard)
	print("Move 1 step 1 returns \n", env.step1(0))
	print("Move 1 step 2 returns \n", env.step2(3))
	print("The oppo cambia is ", env.state[-1])
	if env.state[-1] == 1:
		print("Now if we try to step we get ", env.step(4))
	print("After move 1 the boards are now, ", env.board, env.oppo_board, env.masterBoard)
	print("--------------------------")

	print("Move 2 step 1 returns \n", env.step1(0))
	print("Move 2 step 2 returns \n", env.step2(4))
	print("The oppo cambia is ", env.state[-1])
	if env.state[-1] == 1:
		print("Now if we try to step we get ", env.step(4))
	print("After move 2 the boards are now, ", env.board, env.oppo_board, env.masterBoard)
	print("--------------------------")

	print("Move 3 step 1 returns \n", env.step1(0))
	print("Move 3 step 2 returns \n", env.step2(1))
	print("The oppo cambia is ", env.state[-1])
	if env.state[-1] == 1:
		print("Now if we try to step we get ", env.step(4))
	print("After move 3 the boards are now, ", env.board, env.oppo_board, env.masterBoard)
	print("--------------------------")

	print("Move 4 step 1 returns \n", env.step1(3))
	print("Move 4 step 2 returns \n", env.step2(2))
	print("The oppo cambia is ", env.state[-1])

	if env.state[-1] == 1:
		print("Now if we try to step we get ", env.step(4))
	print("After move 4 the boards are now, ", env.board, env.oppo_board, env.masterBoard)














	






