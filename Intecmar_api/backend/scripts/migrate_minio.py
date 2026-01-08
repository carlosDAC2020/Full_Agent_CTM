import os
import boto3
from botocore.exceptions import ClientError
from backend.app.core.config import settings

def migrate_minio_buckets():
    """
    Migra archivos de los buckets antiguos ('users' y 'agent-results') 
    al nuevo bucket unificado ('intecmar-data').
    """
    endpoint = os.getenv("MINIO_ENDPOINT", "http://shared-minio:9000")
    access_key = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    secret_key = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    dest_bucket = settings.MINIO_BUCKET_NAME
    
    source_buckets = ["users", "agent-results"]

    s3 = boto3.client(
        's3',
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        use_ssl=False
    )

    print(f"🚀 Iniciando migración de MinIO a bucket: {dest_bucket}")

    # Asegurar bucket destino
    try:
        s3.head_bucket(Bucket=dest_bucket)
    except ClientError:
        print(f"📦 Creando bucket destino: {dest_bucket}")
        s3.create_bucket(Bucket=dest_bucket)

    for src in source_buckets:
        try:
            # Verificar si el bucket origen existe
            s3.head_bucket(Bucket=src)
            print(f"📂 Migrando contenido de bucket: {src}...")
            
            # Listar objetos
            paginator = s3.get_paginator('list_objects_v2')
            for page in paginator.paginate(Bucket=src):
                if 'Contents' in page:
                    for obj in page['Contents']:
                        key = obj['Key']
                        # Copiar objeto
                        copy_source = {'Bucket': src, 'Key': key}
                        
                        # Verificar si ya existe en destino para no repetir trabajo innecesario
                        try:
                            s3.head_object(Bucket=dest_bucket, Key=key)
                            # print(f"  ⏭️ {key} ya existe en destino, omitiendo.")
                        except ClientError:
                            # No existe, copiar
                            print(f"  ✅ Copiando: {key}")
                            s3.copy_object(CopySource=copy_source, Bucket=dest_bucket, Key=key)
                            
            print(f"✨ Migración de '{src}' finalizada.")
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                print(f"⚠️ Bucket origen '{src}' no encontrado, omitiendo.")
            else:
                print(f"❌ Error migrando bucket '{src}': {e}")
        except Exception as e:
            print(f"❌ Error inesperado en migración de '{src}': {e}")

    print("🏁 Migración de MinIO completada.")

if __name__ == "__main__":
    migrate_minio_buckets()
