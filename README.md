# btc2balance

Extrae las wallet que tuvieron alguna ves movimiento en la blockchain de BTC y la guarda en MySql

## Install 

Whether installing using Pip or from source, plyvel requires leveldb development libraries for LevelDB >1.2.X.

On Linux, install libleveldb-dev

```
sudo apt-get install libleveldb-dev
```
### Using pip
```
python3 -m pip install -r /path/to/requirements.txt
```
### Mysql
```
mysql < db.sql
```

## Config

En __main__.py configurar:
- conf_mysql: accesos de la base de datos
- dir_bitcoin: directorio donde esta la blockchain. Por defecto en la instalacion bitcoin-core esta en '~/.bitcoin'

## Ejecucion
```
python3 __main__.py
```

## Notas

[blockchain_parser](https://github.com/alecalve/python-bitcoin-blockchain-parser)