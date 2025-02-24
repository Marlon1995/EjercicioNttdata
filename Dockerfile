# Usar la imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de requisitos al contenedor
COPY requirements.txt .

# Actualizar pip y luego instalar las dependencias
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente al contenedor
COPY . .

# Establecer la variable de entorno para el entorno (dev, qa, prod)
ENV ENV=dev

# Exponer el puerto en el que Flask escucha
EXPOSE 8080

# Comando para iniciar la aplicación con Gunicorn (recomendado en producción)
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
