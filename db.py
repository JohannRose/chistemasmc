# Database Configuration
# Configuración de la base de datos PostgreSQL en Aiven

# PostgreSQL Connection String
DATABASE_URL = "postgresql://avnadmin:AVNS_Ip7pf989aOcdP6_SaZx@minecraftjohann-usat-fc50.e.aivencloud.com:17580/svminecraft?sslmode=require"

# Flask Secret Key
SECRET_KEY = "minecraft-payment-tracker-johann-2025-secret-key-production"

# Database Engine Options
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'pool_size': 10,
    'max_overflow': 20
}

# SQLAlchemy Configuration
SQLALCHEMY_TRACK_MODIFICATIONS = False
