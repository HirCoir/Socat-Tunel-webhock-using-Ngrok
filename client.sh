pkill ngrok
pkill ngrok
pkill ngrok
ngrok_token="your_ngrok_token_here"
# Definir el puerto para el túnel
ngrok_port=22

# URL de servidor flask (server.py)
WEBHOOCK_URL="123.456.789"
WEBHOOCK_PORT=5000
# Definir el token secreto de la aplicación Flask
flask_token="crearurlsecreta"

# Configurar ngrok con el token
ngrok authtoken $ngrok_token

# Iniciar el servidor ngrok en modo TCP en el puerto definido en segundo plano
ngrok tcp $ngrok_port > /dev/null &

# Esperar un momento para asegurarse de que ngrok esté listo
sleep 5

# Obtener la URL TCP directamente del resultado del comando ngrok
ngrok_url=$(curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url' | sed 's|tcp://||')

# Mostrar la URL en la consola
echo $ngrok_url

# Enviar la URL al servidor webhock con el token secreto usando cURL
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Token $flask_token" \
  -d '{"url": "'$ngrok_url'"}' \
  http://$WEBHOOCK_URL:$WEBHOOCK_PORT=/webhook

# Mostrar información adicional
echo "URL TCP enviada al servidor webhock"
echo "Puedes acceder a la interfaz web de ngrok en http://127.0.0.1:4040"
