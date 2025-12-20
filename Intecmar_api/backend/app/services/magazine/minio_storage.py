from minio import Minio
from minio.error import S3Error
import os
import io


class MinioStorage:
    def __init__(self) -> None:
        endpoint = os.getenv("MINIO_ENDPOINT", "shared_minio:9000")
        if endpoint.startswith("http://"):
            endpoint = endpoint[7:]
        elif endpoint.startswith("https://"):
            endpoint = endpoint[8:]

        self.client = Minio(
            endpoint,
            access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
            secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
            secure=os.getenv("MINIO_SECURE", "False").lower() == "true",
        )
        self.bucket_name = os.getenv("MINIO_BUCKET_USERS", "users")
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self) -> None:
        """Crea el bucket si no existe (idempotente)."""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                print(f"Bucket '{self.bucket_name}' creado exitosamente.")
        except S3Error as err:
            print(f"Error verificando bucket MinIO: {err}")

    def upload_file(
        self,
        file_data: bytes,
        folder: str,
        filename: str,
        content_type: str = "application/pdf",
    ) -> bool:
        """Sube un archivo a MinIO en la ruta {folder}/{filename}."""
        try:
            data_stream = io.BytesIO(file_data)
            object_name = f"{folder}/{filename}"

            self.client.put_object(
                self.bucket_name,
                object_name,
                data_stream,
                length=len(file_data),
                content_type=content_type,
            )
            print(f"Archivo subido a MinIO: {self.bucket_name}/{object_name}")
            return True
        except S3Error as e:
            print(f"Error subiendo a MinIO: {e}")
            return False


minio_storage = MinioStorage()
