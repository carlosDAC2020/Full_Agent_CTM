import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

class MinioService:
    def __init__(self):
        self.endpoint = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
        self.access_key = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
        self.secret_key = os.getenv("MINIO_SECRET_KEY", "minioadmin")
        self.bucket_name = os.getenv("MINIO_BUCKET", "agent-results")
        self.public_endpoint = os.getenv("MINIO_PUBLIC_ENDPOINT", "http://localhost:9000")

        # Cliente interno (para subir archivos desde Docker)
        self.s3_client = boto3.client(
            's3',
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
        )
        
        # Asegurar que el bucket existe
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except ClientError:
            print(f"🪣 Bucket '{self.bucket_name}' no encontrado. Creando...")
            self.s3_client.create_bucket(Bucket=self.bucket_name)

    def upload_file(self, file_path: str, session_id: str, subfolder: str = None) -> str:
        """
        Sube un archivo y retorna el 'object_key' (ruta en S3).
        Organiza por carpeta usando session_id.
        """
        if not file_path or not os.path.exists(file_path):
            print(f"⚠️ Archivo no encontrado para subir: {file_path}")
            return None

        filename = os.path.basename(file_path)
        # Estructura: session_id/[subfolder/]filename
        if subfolder:
            object_name = f"{session_id}/{subfolder}/{filename}"
        else:
            object_name = f"{session_id}/{filename}"

        try:
            print(f"⬆️ Subiendo {filename} a MinIO ({self.bucket_name})...")
            self.s3_client.upload_file(file_path, self.bucket_name, object_name)
            return object_name
        except FileNotFoundError:
            print("❌ El archivo no fue encontrado")
            return None
        except NoCredentialsError:
            print("❌ Credenciales incorrectas")
            return None

    def get_presigned_url(self, object_name: str, expiration=3600) -> str:
        """
        Genera una URL temporal para descargar el archivo.
        REEMPLAZA el endpoint interno (minio:9000) por el público (localhost:9000)
        para que funcione en el navegador del usuario.
        """
        if not object_name:
            return None
            
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_name},
                ExpiresIn=expiration
            )
            # Truco clave: boto3 genera la URL con 'http://minio:9000...', 
            # pero el navegador del usuario necesita 'http://localhost:9000...'
            if self.endpoint in url and self.public_endpoint:
                url = url.replace(self.endpoint, self.public_endpoint)
            return url
        except ClientError as e:
            print(f"Error generando URL: {e}")
            return None