#!/bin/sh

set -e

# --- BUCLE DE ESPERA PARA LA BASE DE DATOS (MÉTODO SEGURO) ---
attempts=0
max_attempts=15
# Usamos 'prisma db execute' para verificar la conexión sin alterar el esquema.
# Este comando solo tendrá éxito si la base de datos está lista para aceptar consultas.
until npx prisma db execute --schema=./prisma/schema.prisma --file ./prisma/check_db.sql > /dev/null 2>&1; do
  attempts=$((attempts+1))
  if [ $attempts -ge $max_attempts ]; then
    echo "Error: No se pudo conectar a la base de datos después de $max_attempts intentos."
    exit 1
  fi
  echo "Esperando a que la base de datos esté lista... (intento $attempts/$max_attempts)"
  sleep 3
done
echo "¡Conexión con la base de datos exitosa!"
# --- FIN DEL BUCLE DE ESPERA ---

# --- LÓGICA DE MIGRACIÓN ---
echo "--> Aplicando migraciones pendientes..."

# El comando 'deploy' es el adecuado para entornos de producción/CI/CD.
# Aplica todas las migraciones pendientes que no se han ejecutado.
npx prisma migrate deploy

# --- FIN DE LA LÓGICA DE MIGRACIÓN ---

echo "--> Migraciones completadas."
echo "--> Iniciando la aplicación Chainlit..."

# Ejecuta el comando principal pasado al contenedor (el CMD del Dockerfile)
exec "$@"