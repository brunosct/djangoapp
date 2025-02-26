FROM python:3.11



# Establece el directorio de trabajo dentro del contenedor
WORKDIR /code

# Copia el archivo de requisitos al contenedor
COPY . /code/ 

RUN pip install uwsgi
# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt



RUN a2enmod wsgi
RUN a2enmod ssl

# CMD tail -f /dev/null
CMD ["uwsgi", "--ini", "/code/app/uwsgi.ini"]

