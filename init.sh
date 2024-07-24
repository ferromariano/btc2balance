#!/bin/bash

# Verificar si la base de datos ya ha sido inicializada
# if [ ! -f /data/.db_initialized ]; then
    echo "Inicializando la base de datos..."
    sleep 10s;
    mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME < /usr/src/app/bd.sql

    # Marcar como inicializado
    # touch /data/.db_initialized
# fi

# Ejecutar la aplicación
python ./__main__.py
