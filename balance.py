import os
from blockchain_parser.blockchain import Blockchain
from blockchain_parser.transaction import Transaction
from blockchain_parser.utils import decode_varint
import mysql.connector
import time

class DBTransactionIndex:
    cache = {}
    def __init__(self):
        pass
    def add(txhash, raw):
        DBTransactionIndex.cache[txhash] = raw
        
    def get(txhash, i):
        if txhash not in DBTransactionIndex.cache:
            return []
        if i not in DBTransactionIndex.cache[txhash]:
            return []
        return DBTransactionIndex.cache[txhash][i]


class dbCache:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="sal",
            password="25042504",
            database="balance"
        )
        self.mycursor = self.mydb.cursor()
        self.sql_insert_transacion = "INSERT INTO btc_wallet (btc_wallet.public, btc_wallet.val) VALUES (%s, %s) ON DUPLICATE KEY UPDATE btc_wallet.val = btc_wallet.val + %s;"

    def addAddrs(self, addrs):
        for addr in addrs:
            val = (addr.address, 1, 1)
            self.mycursor.execute(self.sql_insert_transacion, val)
        pass
    def save(self):
        self.mydb.commit()
        
class btc2balance:
    
    def __init__(self):
        self.dbCache = dbCache()
        self.cacheBlock = []
        # self.loaddBlocks()
    def loadFileBlocks(self):
        self.blockchain = Blockchain(os.path.expanduser('~/.bitcoin/blocks'))
    def loadFileindex(self):
        self.blockchain_index = os.path.expanduser('~/.bitcoin/blocks/index')

    def loopBlocks(self):
        print("\n\n loopBlocks")
        for block in self.blockchain.get_unordered_blocks():
            if block.hash in self.cacheBlock:
                print("height=%s block=%s REPETIDO" % (block.height, block.hash))
                continue
            self.cacheBlock.append(block.hash)
            print("height=%s block=%s" % (block.height, block.hash))
            #block._transactions = list(get_block_transactions(block.hex))
            for transactions in block.transactions:
                self.loopTransactions(transactions)
            self.dbCache.save()

        self.blockchain = Blockchain(os.path.expanduser('~/.bitcoin/blocks'))
        

    def loopBlocksOrder(self, start, end=0):
        print("\n\n loopBlockss start=%d end=%d" % (start, end))
        for block in self.blockchain.get_ordered_blocks(self.blockchain_index, start=start, end=end):
            #block._transactions = list(get_block_transactions(block.hex))
            if block.hash in self.cacheBlock:
                print('repetido')
                print("\nheight=%d block=%s repetido" % (block.height, block.hash))
                continue
            print("\nheight=%d block=%s" % (block.height, block.hash))
            self.cacheBlock.append(block.hash)



            for transactions in block.transactions:
                self.loopTransactions(transactions)
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


tmp = btc2balance()
# tmp.loadFileBlocks()
# tmp.loadFileindex()
# tmp.loopBlocksOrder(1, 2)
# tmp.loopBlocksOrder(1, 2)



while True:
    time.sleep(15)
    tmp.loadFileBlocks()
    tmp.loopBlocks()
