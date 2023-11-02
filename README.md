### Como funciona?

- Server.py y config.py (Requiere tener instalado socat) espera a que el cliente envíe la url generada por ngrok para exponerlo vía socat, por defecto reenvía el puerto 2222 del servidor donde se ejecuta a la url obtenida desde client.sh

- client.sh ejecuta ngrok y expone el puerto definido, después lo obtiene y lo manda vía webhock al servidor server.py, este requiere jq y ngrok instalado.

### Requisitos Cliente
##### jq, ngrok, supervisor

### Requisitos Servidor
##### python3, socat
