FROM python:3.11



# Establece el directorio de trabajo dentro del contenedor
WORKDIR /code

# Copia el archivo de requisitos al contenedor
COPY . /code/ 

RUN pip install uwsgi gunicorn
# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /var/log/uwsgi/
RUN chmod 777 /var/log/uwsgi/


# CMD ["uwsgi", "--ini", "/code/app/app.ini"]
CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:9000", "stocksProjectApp.wsgi:application"]

