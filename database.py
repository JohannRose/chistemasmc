"""
Database Layer - Serverless Optimized (NO CONNECTION POOL)
Direct connections + In-memory cache for Vercel
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
from db import DATABASE_URL

# Simple in-memory cache
_cache = {}
_cache_timeout = {}

def cache_get(key):
    """Get from cache if not expired"""
    if key in _cache:
        if datetime.now() < _cache_timeout.get(key, datetime.min):
            return _cache[key]
        else:
            del _cache[key]
            if key in _cache_timeout:
                del _cache_timeout[key]
    return None

def cache_set(key, value, seconds=30):
    """Set cache with expiration"""
    _cache[key] = value
    _cache_timeout[key] = datetime.now() + timedelta(seconds=seconds)

def cache_clear():
    """Clear all cache"""
    _cache.clear()
    _cache_timeout.clear()

def get_connection():
    """Create a new connection (serverless-friendly)"""
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def execute_query(query, params=None, fetch=True, cache_key=None, cache_seconds=30):
    """Ejecutar query con cache opcional - DIRECT CONNECTION"""
    # Check cache first
    if cache_key and fetch:
        cached = cache_get(cache_key)
        if cached is not None:
            return cached
    
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            if fetch:
                result = cursor.fetchall()
                if cache_key:
                    cache_set(cache_key, result, cache_seconds)
                return result
            conn.commit()
            cache_clear()  # Clear cache on write
            return cursor.rowcount
    finally:
        conn.close()

def execute_one(query, params=None, cache_key=None, cache_seconds=30):
    """Ejecutar query y retornar un solo resultado - DIRECT CONNECTION"""
    if cache_key:
        cached = cache_get(cache_key)
        if cached is not None:
            return cached
    
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            if cache_key:
                cache_set(cache_key, result, cache_seconds)
            return result
    finally:
        conn.close()

# ============================================================================
# USER FUNCTIONS
# ============================================================================

def get_user_by_username(username):
    """Obtener usuario por username - cached"""
    query = "SELECT * FROM users WHERE username = %s"
    return execute_one(query, (username,), cache_key=f"user:{username}")

def verify_password(user, password):
    """Verificar contraseña de usuario"""
    if user and 'password_hash' in user:
        return check_password_hash(user['password_hash'], password)
    return False

# ============================================================================
# PLAYER FUNCTIONS - OPTIMIZED
# ============================================================================

def get_all_players():
    """Obtener todos los jugadores con su total pagado - CACHED"""
    query = """
        SELECT 
            p.id, p.name, p.minecraft_username,
            COALESCE(SUM(pay.amount), 0) as total_paid
        FROM players p
        LEFT JOIN payments pay ON p.id = pay.player_id
        GROUP BY p.id
        ORDER BY p.name
    """
    return execute_query(query, cache_key="all_players", cache_seconds=20)

def get_player_by_id(player_id):
    """Obtener jugador por ID"""
    query = "SELECT * FROM players WHERE id = %s"
    return execute_one(query, (player_id,))

def create_player(name, minecraft_username):
    """Crear nuevo jugador"""
    query = "INSERT INTO players (name, minecraft_username) VALUES (%s, %s) RETURNING id"
    result = execute_one(query, (name, minecraft_username))
    return result['id'] if result else None

def update_player(player_id, name, minecraft_username):
    """Actualizar jugador"""
    query = "UPDATE players SET name = %s, minecraft_username = %s WHERE id = %s"
    return execute_query(query, (name, minecraft_username, player_id), fetch=False)

def delete_player(player_id):
    """Eliminar jugador"""
    query = "DELETE FROM players WHERE id = %s"
    return execute_query(query, (player_id,), fetch=False)

# ============================================================================
# PAYMENT FUNCTIONS - OPTIMIZED
# ============================================================================

def get_all_payments():
    """Obtener todos los pagos - CACHED"""
    query = """
        SELECT 
            pay.id, pay.amount, pay.date, pay.description,
            pay.player_id, p.name as player_name, p.minecraft_username
        FROM payments pay
        JOIN players p ON pay.player_id = p.id
        ORDER BY pay.date DESC
    """
    return execute_query(query, cache_key="all_payments", cache_seconds=20)

def get_recent_payments(limit=5):
    """Obtener pagos recientes - CACHED"""
    query = """
        SELECT pay.id, pay.amount, pay.date, pay.description,
               pay.player_id, p.name as player_name
        FROM payments pay
        JOIN players p ON pay.player_id = p.id
        ORDER BY pay.date DESC LIMIT %s
    """
    return execute_query(query, (limit,), cache_key=f"recent_payments:{limit}", cache_seconds=15)

def get_payment_by_id(payment_id):
    """Obtener pago por ID"""
    query = "SELECT pay.*, p.name as player_name FROM payments pay JOIN players p ON pay.player_id = p.id WHERE pay.id = %s"
    return execute_one(query, (payment_id,))

def create_payment(player_id, amount, date, description=None):
    """Crear nuevo pago"""
    query = "INSERT INTO payments (player_id, amount, date, description) VALUES (%s, %s, %s, %s) RETURNING id"
    result = execute_one(query, (player_id, amount, date, description))
    return result['id'] if result else None

def update_payment(payment_id, player_id, amount, date, description=None):
    """Actualizar pago"""
    query = "UPDATE payments SET player_id = %s, amount = %s, date = %s, description = %s WHERE id = %s"
    return execute_query(query, (player_id, amount, date, description, payment_id), fetch=False)

def delete_payment(payment_id):
    """Eliminar pago"""
    query = "DELETE FROM payments WHERE id = %s"
    return execute_query(query, (payment_id,), fetch=False)

# ============================================================================
# EXPENSE FUNCTIONS - OPTIMIZED
# ============================================================================

def get_all_expenses():
    """Obtener todos los gastos - CACHED"""
    query = "SELECT * FROM expenses ORDER BY date DESC"
    return execute_query(query, cache_key="all_expenses", cache_seconds=20)

def get_recent_expenses(limit=5):
    """Obtener gastos recientes - CACHED"""
    query = "SELECT * FROM expenses ORDER BY date DESC LIMIT %s"
    return execute_query(query, (limit,), cache_key=f"recent_expenses:{limit}", cache_seconds=15)

def get_expense_by_id(expense_id):
    """Obtener gasto por ID"""
    query = "SELECT * FROM expenses WHERE id = %s"
    return execute_one(query, (expense_id,))

def create_expense(amount, date, description):
    """Crear nuevo gasto"""
    query = "INSERT INTO expenses (amount, date, description) VALUES (%s, %s, %s) RETURNING id"
    result = execute_one(query, (amount, date, description))
    return result['id'] if result else None

def update_expense(expense_id, amount, date, description):
    """Actualizar gasto"""
    query = "UPDATE expenses SET amount = %s, date = %s, description = %s WHERE id = %s"
    return execute_query(query, (amount, date, description, expense_id), fetch=False)

def delete_expense(expense_id):
    """Eliminar gasto"""
    query = "DELETE FROM expenses WHERE id = %s"
    return execute_query(query, (expense_id,), fetch=False)

# ============================================================================
# STATISTICS - ULTRA OPTIMIZED
# ============================================================================

def get_statistics():
    """Obtener estadísticas - SINGLE QUERY + CACHED"""
    query = """
        SELECT 
            (SELECT COUNT(*) FROM players) as total_players,
            (SELECT COALESCE(SUM(amount), 0) FROM payments) as total_collected,
            (SELECT COALESCE(SUM(amount), 0) FROM expenses) as total_expenses
    """
    result = execute_one(query, cache_key="statistics", cache_seconds=15)
    if result:
        # Convert all to float for consistency
        result['total_collected'] = float(result['total_collected'])
        result['total_expenses'] = float(result['total_expenses'])
        result['overall_balance'] = result['total_collected'] - result['total_expenses']
        player_count = result['total_players']
        result['expense_per_player'] = result['total_expenses'] / player_count if player_count > 0 else 0.0
    return result
