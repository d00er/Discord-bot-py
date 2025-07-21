# Descargamos Python 3 Slim
FROM python:3.12.8-alpine3.21


# Copia requirements primero
COPY requirements.txt /requirements.txt

# Con WORKDIR vamos a especificar en que carpeta vamos a guardar todo el codigo
WORKDIR /Bot

# Copiamos nuestro codigo de Python dentro de la carpeta app
# Recuerda que tienes que usar el .dockerignore para que tu imagen sea mas ligera
COPY Bot /Bot

# Instalamos las dependencias dentro de la imagen
# --no-cache-dir es un argumento para que no descarge archivos cacheables, puesto que esta imagen es inmutable, no los vamos a usar.
RUN pip install --no-cache-dir -r /requirements.txt
RUN mkdir downloads


# Esto es un poco complicado de explicar, y tiene que ver con como funciona Python, asi que te reccomiendo buscar mas en profundidad que hace.
# Basicamente Python manda todos sus mensajes en un Buffer, y si el Buffer esta lleno, esto puede hacer que cuando nuestro backend mande logs, se tarden en responder hasta que tengan espacio en el Buffer
# Un buffer te lo puedes imaginar como un Array que tiene un espacio limitado, es como cuando tu estas en una fila re larga y tienes que esperar a que llegue tu turno, es algo similar acá.
ENV PYTHONUNBUFFERED=1

# Ejecutamos la aplicacion en su archivo principal, como lo harias tu mismo en tu consola
CMD [ "python", "the_bot.py" ]