FROM python:3.11



RUN apt update &&  apt -y install wget curl sudo \
    lsb-release git apt-transport-https ca-certificates \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt update && apt install -y apache2 libapache2-mod-wsgi-py3 \
&& apt clean \
&& rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /code

# Copia el archivo de requisitos al contenedor
COPY . /code/ 

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt



RUN a2enmod wsgi
RUN a2enmod ssl

# CMD tail -f /dev/null
CMD ["apache2ctl", "-D","FOREGROUND"]

