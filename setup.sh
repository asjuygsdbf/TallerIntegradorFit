# Crear el directorio de configuración de Streamlit si no existe
mkdir -p ~/.streamlit/

# Crear el archivo de configuración config.toml con los parámetros necesarios
echo "[server]
headless = true                 # Ejecutar en modo sin interfaz gráfica (modo servidor)
enableCORS = false              # Desactivar la protección CORS (permite acceso externo)
enableXsrfProtection = false    # Desactivar la protección contra ataques XSRF (útil en despliegues simples)
port = 8080                     # Puerto donde se ejecutará la aplicación Streamlit
" > ~/.streamlit/config.toml