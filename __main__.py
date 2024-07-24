import os
import time
import sys
from btc2balance import btc2balance

tmp = btc2balance(
    conf_mysql={
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'sal'),
        'password': os.getenv('DB_PASSWORD', '25042504'),
        'database': os.getenv('DB_DATABASE', 'balance')
    },
    dir_bitcoin=os.getenv('BITCOIN_DIR', '~/.bitcoin')
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
