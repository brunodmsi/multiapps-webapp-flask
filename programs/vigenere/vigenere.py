from programs.vigenere.cipher.cipher import Cipher

class Vigenere(Cipher):
  def __init__(self):
    self.plain = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

  def repeat_password(self, password, text):
    if len(password) < len(text):
      new_pass = password * int((len(text) / len(password)))
      if len(new_pass):
        new_pass += password[:len(new_pass)]
      return new_pass.upper()
    return password.upper()

  def encrypt(self, plaintext, password, decrypt=False):
    password = self.repeat_password(password, plaintext)
    plaintext = self.format_str(plaintext)
    textout = ''

    for idx, char in enumerate(plaintext.upper()):
      index_key = self.plain.find(password[idx])
      c_alphabet = self.shift_alphabet(self.plain, index_key)

      if decrypt:
        index_pos = c_alphabet.find(char)
        textout += self.plain[index_pos]
      else:
        index_pos = self.plain.find(char)
        textout += c_alphabet[index_pos]
    return textout

  def decrypt(self, ciphertext, password):
    return self.encrypt(ciphertext, password, True)