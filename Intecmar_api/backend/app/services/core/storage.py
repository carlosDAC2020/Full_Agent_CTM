import os
import boto3
import io
import mimetypes
from botocore.exceptions import NoCredentialsError, ClientError
from backend.app.core.config import settings

class UnifiedStorageService:
    def __init__(self):
        # Configuración desde entorno o settings
        self.endpoint = os.getenv("MINIO_ENDPOINT", "http://shared-minio:9000")
        self.access_key = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
        self.secret_key = os.getenv("MINIO_SECRET_KEY", "minioadmin")
        self.bucket_name = settings.MINIO_BUCKET_NAME
        self.public_endpoint = os.getenv("MINIO_PUBLIC_ENDPOINT", "http://localhost:9000")

        # Cliente boto3 (S3 compatible)
        self.s3_client = boto3.client(
            's3',
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            use_ssl=False
        )
        
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except ClientError:
            print(f"🪣 Unified Bucket '{self.bucket_name}' no encontrado. Creando...")
            try:
                self.s3_client.create_bucket(Bucket=self.bucket_name)
            except Exception as e:
                print(f"❌ Error creando bucket: {e}")

    def upload_file(self, file_path_or_data, object_key: str, content_type: str = None, remove_after_upload: bool = False) -> str:
        """
        Sube un archivo (ruta local o bytes) a MinIO.
        Retorna la object_key si tiene éxito.
        """
        if not content_type:
            mime_type, _ = mimetypes.guess_type(object_key)
            content_type = mime_type or "application/octet-stream"

        success = False
        try:
            if isinstance(file_path_or_data, (bytes, io.BytesIO)):
                # Subir desde bytes
                data = file_path_or_data if isinstance(file_path_or_data, bytes) else file_path_or_data.read()
                self.s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_key,
                    Body=data,
                    ContentType=content_type
                )
                success = True
            else:
                # Subir desde ruta local
                if not os.path.exists(file_path_or_data):
                    print(f"⚠️ Archivo no encontrado: {file_path_or_data}")
                    return None
                self.s3_client.upload_file(
                    file_path_or_data, 
                    self.bucket_name, 
                    object_key,
                    ExtraArgs={'ContentType': content_type}
                )
                success = True
            
            if success:
                print(f"✅ Archivo subido: {self.bucket_name}/{object_key}")
                
                # Cleanup if requested
                if remove_after_upload and not isinstance(file_path_or_data, (bytes, io.BytesIO)):
                    try:
                        os.remove(file_path_or_data)
                        print(f"🗑️ Archivo local eliminado: {file_path_or_data}")
                    except Exception as e:
                        print(f"⚠️ No se pudo eliminar el archivo local {file_path_or_data}: {e}")
                
                return object_key
        except Exception as e:
            print(f"❌ Error subiendo a MinIO: {e}")
            return None

    def download_file(self, object_key: str) -> bytes:
        """Descarga un archivo y retorna sus bytes."""
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=object_key)
            return response['Body'].read()
        except Exception as e:
            print(f"❌ Error descargando de MinIO: {e}")
            return None

    def get_presigned_url(self, object_key: str, expiration=3600) -> str:
        """Genera URL temporal para acceso desde el navegador."""
        if not object_key: return None
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_key},
                ExpiresIn=expiration
            )
            # Fix para Docker (reemplazar endpoint interno por externo si es necesario)
            if self.endpoint in url and self.public_endpoint:
                url = url.replace(self.endpoint, self.public_endpoint)
            return url
        except Exception as e:
            print(f"❌ Error generando URL: {e}")
            return None

# Instancia única para toda la app
storage_service = UnifiedStorageService()
