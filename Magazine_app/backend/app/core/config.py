import os
from dotenv import load_dotenv

# Load environment variables from the root .env file
# assuming this file is at backend/app/core/config.py, so root is ../../../.env
# Adjust path as necessary based on where main.py runs or use default loading
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), '.env')
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME: str = "Magazine Generator API"
    VERSION: str = "1.0.0"
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Security / Workers
    WORKER_TOKEN: str = os.getenv("WORKER_TOKEN", "")
    
    # Paths
    OUTPUTS_DIR: str = "outputs"
    EMAIL_SETTINGS_FILE: str = os.path.join(OUTPUTS_DIR, "email_settings.json")
    SOURCES_FILE: str = os.path.join(OUTPUTS_DIR, "sources.json")
    CONVOCATORIAS_FILE: str = os.path.join(OUTPUTS_DIR, "convocatorias.json")
    UPLOADS_DIR: str = os.path.join(OUTPUTS_DIR, "uploads")
    
    # Email Defaults
    DEFAULT_SENDER_EMAIL: str = os.getenv("DEFAULT_SENDER_EMAIL", "harithodevoz@gmail.com")
    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASS: str = os.getenv("SMTP_PASS", "")
    SMTP_TLS: bool = os.getenv("SMTP_TLS", "true").lower() in ("1", "true", "yes")
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "false").lower() in ("1", "true", "yes")

    # API Keys & External Services (Ensure they are loaded in env)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DEFAULT_TOPIC: str = os.getenv(
            "DEFAULT_TOPIC",
            "convocatorias de financiación nacionales e internacionales y eventos en ciencia, tecnología e inteligencia artificial para startups"
        )

settings = Settings()
