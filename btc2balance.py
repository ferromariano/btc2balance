import os
from blockchain_parser.blockchain import Blockchain
from dbCache import dbCache

class btc2balance:
    
    def __init__(self, 
            conf_mysql,
            dir_bitcoin='~/.bitcoin'
        ):
        self.dbCache = dbCache(conf_mysql)
        self.cacheBlock = []
        self.config = {
            'dir_bitcoin': dir_bitcoin
        }
        
    def loadFileBlocks(self):
        self.blockchain = Blockchain(os.path.expanduser(self.config['dir_bitcoin'] + '/blocks'))

    def loadFileindex(self):
        self.blockchain_index = os.path.expanduser(self.config['dir_bitcoin'] + '/blocks/index')

    def loopsBlocks(self):
        print("\n\n loopBlocks")
        for block in self.blockchain.get_unordered_blocks():
            self.loopsAnyBlocks(block)

    def loopsBlocksOrder(self, start, end=0):
        print("\n\n loopBlockss start=%d end=%d" % (start, end))
        for block in self.blockchain.get_ordered_blocks(self.blockchain_index, start=start, end=end):
            self.loopsAnyBlocks(block)

    def loopsAnyBlocks(self, block):
        if self.dbCache.hasBlock(block.hash):
            print("height=%s block=%s REPETIDO" % (block.height, block.hash))
            return
        print("height=%s block=%s" % (block.height, block.hash))

        for transactions in block.transactions:
            self.loopTransactions(transactions)

        self.dbCache.insertBlock(block.hash)
        self.dbCache.save()

    def loopTransactions(self, transactions):
        print("    tx=%s" % transactions.txid)
        # for input in transactions.inputs:
        #     self.loopTransactionInput(input)
        for output in transactions.outputs:
            self.loopTransactionOutput(output)


    def loopTransactionOutput(self, output):
            print("        OUT address=%s value=%s" % (output.addresses, output.value))
            self.dbCache.addAddrs(output.addresses)
            # val = (output.addresses, output.value, output.value)
            # self.mycursor.execute(sql, val)
            # self.mydb.commit()

    def loopTransactionInput(self, input):
        if input.transaction_hash == '0000000000000000000000000000000000000000000000000000000000000000':
            print('        IN coinbase')
            return
        
        print('        IN=', input.transaction_hash,' #', input.transaction_index)
