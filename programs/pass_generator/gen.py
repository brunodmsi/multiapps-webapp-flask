import string
from random import *

def generate():
  chars = string.ascii_letters + string.punctuation + string.digits
  password = "".join(choice(chars) for x in range(randint(8, 16)))

  return password
