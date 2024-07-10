import time
import sys
from btc2balance import btc2balance

tmp = btc2balance(
    conf_mysql={
        'host': "localhost",
        'user': "sal",
        'password': "25042504",
        'database': "balance"
    },
    dir_bitcoin='~/.bitcoin'
)


tmp.loadFileBlocks()
tmp.loadFileindex()

while True:
    tmp.loopsBlocks()
    try:
        #time.sleep(15)
        pass
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
    except Exception as e:
        print('Error:', e)
        pass
