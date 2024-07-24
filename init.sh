#!/bin/bash

# Verificar si la base de datos ya ha sido inicializada
if [ ! -f /data/.db_initialized ]; then
    echo "Inicializando la base de datos..."
    mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME < /usr/src/app/db.sql

    # Marcar como inicializado
    touch /data/.db_initialized
fi

# Ejecutar la aplicación
exec python ./__main__.py
