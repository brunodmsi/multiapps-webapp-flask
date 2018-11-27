import hashlib as hasher
import datetime as date

class Block:
  def __init__(self, index, timestamp, data, prev_hash):
    self.index = index
    self.timestamp = timestamp
    self.data = data 
    self.prev_hash = prev_hash
    self.hash = self.hash_block()

  def hash_block(self) :
    sha = hasher.sha256()
    sha.update((str(self.index).encode('utf-8')) +
                str(self.timestamp).encode('utf-8') +
                str(self.data).encode('utf-8') +
                str(self.prev_hash).encode('utf-8'))
    return sha.hexdigest()