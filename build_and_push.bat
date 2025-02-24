@echo off

:: Variables
set IMAGE_NAME=kfcregistry.azurecr.io/devops-microservice
set TAG=latest
set DOCKERFILE_PATH=.
set REGISTRY=kfcregistry.azurecr.io

:: Iniciar sesión en ACR
echo Iniciando sesión en Azure Container Registry...
az acr login --name %REGISTRY%

:: Construir la imagen Docker
echo Construyendo la imagen Docker...
docker build -t %IMAGE_NAME%:%TAG% %DOCKERFILE_PATH%

:: Subir la imagen a ACR
echo Subiendo la imagen a ACR...
docker push %IMAGE_NAME%:%TAG%

echo Imagen %IMAGE_NAME%:%TAG% subida correctamente.
