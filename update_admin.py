import psycopg2
from werkzeug.security import generate_password_hash

# Importar configuración de db.py
from db import DATABASE_URL

def update_admin_password():
    """Actualizar contraseña del usuario johann"""
    print("=" * 80)
    print("ACTUALIZANDO CONTRASEÑA DE JOHANN")
    print("=" * 80)
    
    try:
        print("\n1. Conectando a PostgreSQL...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        print("   ✓ Conexión exitosa!")
        
        # Nuevo password
        username = "johann"
        new_password = "%Aguinaga10%"
        
        print(f"\n2. Actualizando contraseña del usuario '{username}'...")
        password_hash = generate_password_hash(new_password)
        
        # Actualizar solo la contraseña
        cursor.execute(
            "UPDATE users SET password_hash = %s WHERE username = %s",
            (password_hash, username)
        )
        
        rows_updated = cursor.rowcount
        
        if rows_updated > 0:
            conn.commit()
            print(f"   ✓ Contraseña actualizada correctamente")
            print(f"\n   Credenciales actuales:")
            print(f"   Username: {username}")
            print(f"   Password: {new_password}")
        else:
            print(f"   ⚠ No se encontró el usuario '{username}'")
            print("   Creando nuevo usuario...")
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                (username, password_hash)
            )
            conn.commit()
            print(f"   ✓ Usuario '{username}' creado correctamente")
        
        print("\n" + "=" * 80)
        print("✓ CONTRASEÑA ACTUALIZADA CORRECTAMENTE")
        print("=" * 80)
        print(f"\nPuedes iniciar sesión con:")
        print(f"Username: {username}")
        print(f"Password: {new_password}")
        
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
    success = update_admin_password()
    sys.exit(0 if success else 1)
