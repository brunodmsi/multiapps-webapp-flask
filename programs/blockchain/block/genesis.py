import datetime as date
import programs.blockchain.block.block as block 

def create_genesis_block():
  return block.Block(0, date.datetime.now(), "Genesis Block", "0")