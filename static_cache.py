"""
Static Cache Manager - Para página index ultra rápida
Los datos se actualizan solo cada 5 minutos
"""
from datetime import datetime, timedelta
import database as db

# Cache global para index
_index_cache = {
    'data': None,
    'last_update': None,
    'cache_duration': 600  # 5 minutos en segundos
}

def get_index_data():
    """
    Obtener datos para index con caché de 5 minutos
    Solo consulta BD cada 5 minutos, el resto sirve datos estáticos
    """
    now = datetime.now()
    
    # Verificar si necesitamos actualizar el caché
    needs_update = (
        _index_cache['data'] is None or
        _index_cache['last_update'] is None or
        (now - _index_cache['last_update']).total_seconds() > _index_cache['cache_duration']
    )
    
    if needs_update:
        print(f"[CACHE] Actualizando datos del index - {now.strftime('%H:%M:%S')}")
        
        # Consultar BD
        players = db.get_all_players()
        payments = db.get_all_payments()
        expenses = db.get_all_expenses()
        stats = db.get_statistics()
        
        # Calcular balances por jugador
        player_data = []
        for player in players:
            player_balance = float(player['total_paid']) - stats['expense_per_player']
            player_data.append({
                'player': player,
                'total_paid': float(player['total_paid']),
                'balance': player_balance
            })
        
        # Guardar en caché
        _index_cache['data'] = {
            'player_data': player_data,
            'payments': payments,
            'expenses': expenses,
            'total_collected': float(stats['total_collected']),
            'total_expenses': float(stats['total_expenses']),
            'overall_balance': float(stats['overall_balance']),
            'expense_per_player': float(stats['expense_per_player']),
            'last_update': now.strftime('%d/%m/%Y %H:%M:%S')
        }
        _index_cache['last_update'] = now
        
        print(f"[CACHE] Datos actualizados. Próxima actualización en 5 minutos")
    else:
        seconds_until_next = _index_cache['cache_duration'] - (now - _index_cache['last_update']).total_seconds()
        print(f"[CACHE] Sirviendo datos cacheados. Próxima actualización en {int(seconds_until_next)}s")
    
    return _index_cache['data']

def force_refresh_index():
    """Forzar actualización del caché (llamar después de crear/editar/eliminar)"""
    _index_cache['data'] = None
    _index_cache['last_update'] = None
    print("[CACHE] Caché forzado a refrescar en próxima petición")

def get_cache_info():
    """Obtener información del estado del caché"""
    if _index_cache['last_update'] is None:
        return {
            'cached': False,
            'last_update': None,
            'next_update': None
        }
    
    now = datetime.now()
    elapsed = (now - _index_cache['last_update']).total_seconds()
    remaining = max(0, _index_cache['cache_duration'] - elapsed)
    next_update = _index_cache['last_update'] + timedelta(seconds=_index_cache['cache_duration'])
    
    return {
        'cached': True,
        'last_update': _index_cache['last_update'].strftime('%d/%m/%Y %H:%M:%S'),
        'next_update': next_update.strftime('%d/%m/%Y %H:%M:%S'),
        'seconds_remaining': int(remaining)
    }

