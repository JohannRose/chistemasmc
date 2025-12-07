"""
Script para aplicar caché estático correctamente
"""
import re

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontrar línea de import database
for i, line in enumerate(lines):
    if 'import database as db' in line and 'import static_cache' not in line:
        lines[i] = line.rstrip() + '\nimport static_cache\n'
        break

# Escribir de vuelta
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✓ Import agregado")

# Ahora reemplazar la función index
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Buscar y reemplazar index
old_pattern = r"@app\.route\('/'\)\ndef index\(\):.*?return render_template\('index\.html',.*?expense_per_player=float\(stats\['expense_per_player'\]\)\)"

new_index = """@app.route('/')
def index():
    \"\"\"Public page - STATIC CACHE (actualiza cada 5 minutos)\"\"\"
    data = static_cache.get_index_data()
    return render_template('index.html',
                         player_data=data['player_data'],
                         payments=data['payments'],
                         expenses=data['expenses'],
                         total_collected=data['total_collected'],
                         total_expenses=data['total_expenses'],
                         overall_balance=data['overall_balance'],
                         expense_per_player=data['expense_per_player'])"""

content = re.sub(old_pattern, new_index, content, flags=re.DOTALL)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Función index actualizada")

# Agregar force_refresh en lugares correctos
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

output = []
i = 0
while i < len(lines):
    line = lines[i]
    output.append(line)
    
    # Detectar llamadas a db que necesitan force_refresh
    if any(call in line for call in [
        'db.create_player(',
        'db.update_player(',
        'db.delete_player(',
        'db.create_payment(',
        'db.update_payment(',
        'db.delete_payment(',
        'db.create_expense(',
        'db.update_expense(',
        'db.delete_expense('
    ]):
        # Agregar force_refresh en la siguiente línea con la misma indentación
        indent = len(line) - len(line.lstrip())
        output.append(' ' * indent + 'static_cache.force_refresh_index()\n')
    
    i += 1

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(output)

print("✓ force_refresh_index() agregado después de operaciones de escritura")
print("✓ app.py completamente actualizado")
