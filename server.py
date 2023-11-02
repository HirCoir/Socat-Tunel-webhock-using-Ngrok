from flask import Flask, request
import subprocess

app = Flask(__name__)

# Leer la configuración desde el archivo config.conf
with open('config.conf', 'r') as config_file:
    config_lines = config_file.readlines()

# Definir valores por defecto
SSL_EXPOSE_PORT = 443
SSL_EXPOSE_CERT = 'cert.pem'
SSH_EXPOSE_PORT = 2222
PORT = 5000
SECRET_TOKEN = None  # Cambio aquí

for line in config_lines:
    if 'SSL_EXPOSE_PORT' in line:
        SSL_EXPOSE_PORT = int(line.split('=')[1].strip())
    elif 'SSL_EXPOSE_CERT' in line:
        SSL_EXPOSE_CERT = line.split('=')[1].strip()
    elif 'SSH_EXPOSE_PORT' in line:
        SSH_EXPOSE_PORT = int(line.split('=')[1].strip())
    elif 'PORT' in line:
        PORT = int(line.split('=')[1].strip())
    elif 'SECRET_TOKEN' in line:  # Cambio aquí
        SECRET_TOKEN = line.split('=')[1].strip()  # Cambio aquí

# Si no se especifica SECRET_TOKEN en config.conf, se usará el valor por defecto
SECRET_TOKEN = SECRET_TOKEN or 'default_secret_token'  # Cambio aquí

def validate_input(data):
    # Verifica si los campos 'url' están presentes
    return 'url' in data

def authenticate(request):
    # Verifica si la solicitud contiene el encabezado 'Authorization'
    auth_header = request.headers.get('Authorization')
    return auth_header == f'Token {SECRET_TOKEN}'

@app.route('/webhook', methods=['POST'])
def webhook():
    # Verifica la autenticación
    if not authenticate(request):
        return 'Autenticación fallida', 401

    try:
        data = request.json

        # Valida el formato de entrada
        if not validate_input(data):
            return 'Datos incorrectos o incompletos', 400

        url = data['url']

        # Mostrar la URL en la consola
        print(f'Received URL: {url}')

        # Actualizar la configuración de stunnel usando sed
        update_stunnel_config(url)

        return 'Configuración actualizada con éxito', 200
    except Exception as e:
        print(f'Error: {e}')
        return 'Error interno del servidor', 500

def update_stunnel_config(url):
    command = ["socat", f"TCP-LISTEN:{SSH_EXPOSE_PORT},fork", f"TCP:{url}"]
    
    try:
        # Intenta iniciar el subproceso
        subprocess.Popen(["socat", f"OPENSSL-LISTEN:{SSL_EXPOSE_PORT},cert={SSL_EXPOSE_CERT},fork,reuseaddr,verify=0", f"TCP:{url}"])
        # Iniciar el subproceso en segundo plano
        subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, close_fds=True)
    except socket.error as e:
        # Si el error es "Address already in use", imprime un mensaje y continúa
        if e.errno == errno.EADDRINUSE:
            print(f'Error: {e}. Forzando la ejecución del comando.')
        else:
            # Si es otro tipo de error, lanza una excepción
            raise e

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
