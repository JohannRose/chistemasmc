import re

# Leer app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Agregar import
content = content.replace('import database as db', 'import database as db\nimport static_cache')

# 2. Reemplazar función index
old_index = r'@app\.route\(\'/\'\)\ndef index\(\):.*?expense_per_player=float\(stats\[\'expense_per_player\'\]\)\)'
new_index = '''@app.route('/')
def index():
    """Public page - STATIC CACHE (actualiza cada 5 minutos)"""
    data = static_cache.get_index_data()
    return render_template('index.html',
                         player_data=data['player_data'],
                         payments=data['payments'],
                         expenses=data['expenses'],
                         total_collected=data['total_collected'],
                         total_expenses=data['total_expenses'],
                         overall_balance=data['overall_balance'],
                         expense_per_player=data['expense_per_player'])'''

content = re.sub(old_index, new_index, content, flags=re.DOTALL)

# 3. Agregar force_refresh después de cada operación
replacements = [
    (r'(db\.create_player\([^)]+\))', r'\1\n        static_cache.force_refresh_index()'),
    (r'(db\.update_player\([^)]+\))', r'\1\n        static_cache.force_refresh_index()'),
    (r'(db\.delete_player\([^)]+\))', r'\1\n        static_cache.force_refresh_index()'),
    (r'(db\.create_payment\([^)]+\))', r'\1\n        static_cache.force_refresh_index()'),
    (r'(db\.update_payment\([^)]+\))', r'\1\n        static_cache.force_refresh_index()'),
    (r'(db\.delete_payment\([^)]+\))', r'\1\n        static_cache.force_refresh_index()'),
    (r'(db\.create_expense\([^)]+\))', r'\1\n        static_cache.force_refresh_index()'),
    (r'(db\.update_expense\([^)]+\))', r'\1\n        static_cache.force_refresh_index()'),
    (r'(db\.delete_expense\([^)]+\))', r'\1\n        static_cache.force_refresh_index()'),
]

for pattern, replacement in replacements:
    content = re.sub(pattern, replacement, content)

# Guardar
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ app.py actualizado con caché estático de 5 minutos")
