#!/bin/bash

# Usa la variable de entorno BUCKET_NAME. Si no está definida, usa "chainlit-bucket" por defecto.
BUCKET_NAME=${BUCKET_NAME:-chainlit-bucket}
AWS_REGION=${APP_AWS_REGION:-eu-central-1}

echo "Configurando LocalStack... Creando bucket: ${BUCKET_NAME} en la región ${AWS_REGION}"

awslocal s3api create-bucket \
    --bucket ${BUCKET_NAME} \
    --region ${AWS_REGION} \
    --create-bucket-configuration LocationConstraint=${AWS_REGION}

echo "Configurando políticas CORS para el bucket ${BUCKET_NAME}..."
awslocal s3api put-bucket-cors \
    --bucket ${BUCKET_NAME} \
    --cors-configuration '{
        "CORSRules": [
            {
                "AllowedHeaders": ["*"],
                "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
                "AllowedOrigins": ["*"],
                "ExposeHeaders": ["ETag"]
            }
        ]
    }'

echo "Configuración de LocalStack completada."