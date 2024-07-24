# Usar una imagen base de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /usr/src/app

# Instalar libleveldb-dev y el cliente de MariaDB
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    mariadb-client  \
    libleveldb-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copiar los archivos de la aplicación al contenedor
COPY ./requirements.txt ./

# Instalar las dependencias de la aplicación
RUN pip install -r requirements.txt

COPY ./bd.sql ./

COPY ./init.sh ./

RUN chmod +x init.sh
# # RUN mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME < db.sql
# CMD ["mysql", "-h", "$DB_HOST", "-u", "$DB_USER", "-p$DB_PASSWORD", "$DB_NAME", "<", "db.sql"]

COPY . ./

# Ejecutar la aplicación
# CMD ["python", "./__main__.py"]
CMD ["./init_db.sh"]