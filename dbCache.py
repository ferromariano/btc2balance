import mysql.connector

class dbCache:
    def __init__(self, conf):
        self.mydb = mysql.connector.connect(
            host=conf['host'],
            user=conf['user'],
            password=conf['password'],
            database=conf['database']
        )
        self.mycursor = self.mydb.cursor()

        self.sql_block_has    = "SELECT COUNT(blocks.id) as 'c' FROM blocks WHERE n = \"%s\";"
        self.sql_block_insert = "INSERT INTO blocks (n) VALUES (%s);"
        self.sql_addrs_insert = "INSERT INTO btc_wallet (btc_wallet.public, btc_wallet.val) VALUES (%s, %s) ON DUPLICATE KEY UPDATE btc_wallet.val = btc_wallet.val + %s;"

    def addAddrs(self, addrs):
        for addr in addrs:
            val = (addr.address, 1, 1)
            self.mycursor.execute(self.sql_addrs_insert, val)
        pass

    def insertBlock(self, hash):
        v = [hash]
        self.mycursor.execute(self.sql_block_insert, v)

    def hasBlock(self, hash):
        v = [hash]
        self.mycursor.execute(self.sql_block_has, v)
        result = self.mycursor.fetchone()
        
        if result[0] == 0:
            return False
        return True

    def save(self):
        self.mydb.commit()