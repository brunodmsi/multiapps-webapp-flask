import programs.random_gen.generator.generate as gen

class List():
  def __init__(self):
    self.__word = gen.Word()
  
  def generate_wordlist(self, lines):
    words = []
    for i in range(lines):
      words.append(self.__word.generate_word())
    return words