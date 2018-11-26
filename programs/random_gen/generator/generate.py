import random

class Word():
	def __init__(self):
		self.__vogals = ['a','e','i','o','u']
		self.__consonants = ['B','C','D','F','G','J','K','L','M','N','P','Q','R','S','T','V','W','X','Z']
		self.__word = []

	def generate_word(self):
		self.__word.append(random.choice(self.__vogals))
		self.__word.append(random.choice(self.__consonants))
		self.__word.append(random.choice(self.__vogals))
		self.__word.append(random.choice(self.__consonants))
		self.__word.append(random.choice(self.__vogals))
		self.__word.append(random.choice(self.__consonants))
		self.__word.append(random.choice(self.__vogals))
		self.__word.append(random.choice(self.__consonants))
		
		word = "".join(self.__word)
		self.__word = []
		return word.lower()