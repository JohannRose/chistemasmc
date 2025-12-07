import psycopg2
from werkzeug.security import generate_password_hash

# URL de conexión a PostgreSQL en Aiven
DATABASE_URL = "postgresql://avnadmin:AVNS_Ip7pf989aOcdP6_SaZx@minecraftjohann-usat-fc50.e.aivencloud.com:17580/defaultdb?sslmode=require"

def init_database():
    """Inicializar base de datos PostgreSQL para Vercel"""
    print("=" * 80)
    print("INICIALIZANDO BASE DE DATOS POSTGRESQL PARA VERCEL")
    print("=" * 80)
    
    try:
        print("\n1. Conectando a PostgreSQL...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        print("   ✓ Conexión exitosa!")
        
        print("\n2. Eliminando tablas existentes...")
        cursor.execute("DROP TABLE IF EXISTS payments CASCADE")
        cursor.execute("DROP TABLE IF EXISTS expenses CASCADE")
        cursor.execute("DROP TABLE IF EXISTS players CASCADE")
        cursor.execute("DROP TABLE IF EXISTS users CASCADE")
        print("   ✓ Tablas antiguas eliminadas")
        
        print("\n3. Creando tablas...")
        
        # Tabla users
        cursor.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(80) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("CREATE INDEX idx_username ON users(username)")
        print("   ✓ Tabla 'users' creada")
        
        # Tabla players
        cursor.execute("""
            CREATE TABLE players (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                minecraft_username VARCHAR(100) NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("CREATE INDEX idx_minecraft_username ON players(minecraft_username)")
        cursor.execute("CREATE INDEX idx_name ON players(name)")
        print("   ✓ Tabla 'players' creada")
        
        # Tabla payments
        cursor.execute("""
            CREATE TABLE payments (
                id SERIAL PRIMARY KEY,
                player_id INTEGER NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                description VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE
            )
        """)
        cursor.execute("CREATE INDEX idx_player_id ON payments(player_id)")
        cursor.execute("CREATE INDEX idx_date ON payments(date)")
        print("   ✓ Tabla 'payments' creada")
        
        # Tabla expenses
        cursor.execute("""
            CREATE TABLE expenses (
                id SERIAL PRIMARY KEY,
                amount DECIMAL(10, 2) NOT NULL,
                date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                description VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("CREATE INDEX idx_expense_date ON expenses(date)")
        print("   ✓ Tabla 'expenses' creada")
        
        # Crear usuario admin
        print("\n4. Creando usuario administrador...")
        password_hash = generate_password_hash('admin123')
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            ('admin', password_hash)
        )
        print("   ✓ Usuario 'admin' creado")
        print("   Username: admin")
        print("   Password: admin123")
        
        conn.commit()
        
        # Verificar
        print("\n5. Verificando tablas...")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        for table in tables:
            print(f"   ✓ {table[0]}")
        
        print("\n" + "=" * 80)
        print("✓ BASE DE DATOS POSTGRESQL INICIALIZADA CORRECTAMENTE")
        print("=" * 80)
        print("\nAhora puedes desplegar en Vercel con confianza.")
        print("Asegúrate de configurar DATABASE_URL en las variables de entorno de Vercel.")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    import sys
    
    print("\n⚠️  IMPORTANTE:")
    print("Este script inicializará la base de datos PostgreSQL en Aiven.")
    print("Todas las tablas existentes serán eliminadas y recreadas.")
    print()
    
    respuesta = input("¿Deseas continuar? (s/n): ")
    
    if respuesta.lower() == 's':
        success = init_database()
        sys.exit(0 if success else 1)
    else:
        print("Operación cancelada.")
        sys.exit(0)
