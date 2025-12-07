import psycopg2
from db import DATABASE_URL

# Eliminar usuario admin
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

cursor.execute("DELETE FROM users WHERE username = 'admin'")
rows_deleted = cursor.rowcount

conn.commit()
cursor.close()
conn.close()

print(f"✓ Usuario 'admin' eliminado ({rows_deleted} registro(s))")
print("Solo queda el usuario 'johann' activo")
