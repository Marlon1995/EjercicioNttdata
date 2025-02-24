# Usar la imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de requisitos y la aplicación
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

# Establecer la variable de entorno para el entorno (dev, qa, prod)
ENV ENV=prod

# Exponer el puerto en el que Flask escucha
EXPOSE 8080

# Comando para iniciar la aplicación
CMD ["python", "app.py"]
