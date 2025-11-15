# Usa una imagen base de Python que tenga un sistema operativo completo (no slim)
# para instalar fácilmente otras dependencias como Node.js
FROM python:3.11

# 1. --- INSTALACIÓN DE NODE.JS Y DEPENDENCIAS DE NPM ---
# Actualiza los paquetes e instala curl
RUN apt-get update && apt-get install -y curl

# Añade el repositorio de NodeSource para instalar una versión reciente de Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash -

# Instala Node.js y npm
RUN apt-get install -y nodejs

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de configuración de Node.js y el schema de Prisma
# Esto se hace primero para aprovechar el cache de Docker si no cambian
COPY package*.json ./
COPY prisma ./prisma/

# Instala las dependencias de Node (Prisma Client)
RUN npm install

# 2. --- INSTALACIÓN DE DEPENDENCIAS DE PYTHON ---
# Copia el archivo de requerimientos de Python
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# 3. --- COPIA DEL CÓDIGO DE LA APLICACIÓN Y SCRIPT DE ARRANQUE ---
# Copia el resto del código de la aplicación
COPY . .

# Otorga permisos de ejecución al script de arranque
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# 4. --- CONFIGURACIÓN FINAL ---
# Expone el puerto que usará Chainlit
EXPOSE 8000

# Usa el script de arranque como punto de entrada
ENTRYPOINT ["entrypoint.sh"]

# El comando por defecto que ejecutará el entrypoint.sh después de la migración
CMD ["chainlit", "run", "app/app.py", "--host", "0.0.0.0", "--port", "8000"]