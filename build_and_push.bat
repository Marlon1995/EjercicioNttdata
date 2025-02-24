@echo off
setlocal

set DEPLOYMENT_FILE=deployment.yaml

:: Comando para aplicar el deployment
echo Aplicando deployment...
kubectl apply -f %DEPLOYMENT_FILE%

:: Verificar si el comando fue exitoso
if %errorlevel% neq 0 (
    echo Error al aplicar el deployment. Saliendo...
    exit /b 1
)


echo Despliegue completado correctamente.

endlocal
