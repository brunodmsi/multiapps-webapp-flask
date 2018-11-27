import programs.blockchain.block.genesis as gsis 
import programs.blockchain.block.new_block as nb 

class Chain():
  def generate_chain(self, num_of_blocks):
    blockchain = [gsis.create_genesis_block()]
    previous_block = blockchain[0]

    for i in range(0, num_of_blocks):
      block_to_add = nb.next_block(previous_block)
      blockchain.append(block_to_add)
      previous_block = block_to_add
      
    return blockchain

