"""
Script para limpiar locks huérfanos de Redis cuando un flujo falla
y no se libera correctamente el lock.

Uso:
    docker-compose exec shared_redis redis-cli DEL "flow_lock:magazine:1"

O usar este script Python dentro del contenedor de la API:
    docker-compose exec intecmar_api python scripts/clear_flow_locks.py
"""

import os
import sys

# Añadir el directorio backend al path para poder importar
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.services.magazine.redis_service import get_redis

def list_all_flow_locks():
    """Lista todos los flow locks activos en Redis"""
    r = get_redis()
    if not r:
        print("❌ No se pudo conectar a Redis")
        return []
    
    # Buscar todas las claves que empiecen con "flow_lock:"
    keys = r.keys("flow_lock:*")
    
    if not keys:
        print("✅ No hay flow locks activos")
        return []
    
    print(f"📋 Flow locks activos ({len(keys)}):")
    locks = []
    for key in keys:
        key_str = key.decode() if isinstance(key, bytes) else key
        ttl = r.ttl(key)
        print(f"  - {key_str} (TTL: {ttl}s)")
        locks.append(key_str)
    
    return locks

def clear_flow_lock(lock_key: str):
    """Elimina un flow lock específico"""
    r = get_redis()
    if not r:
        print("❌ No se pudo conectar a Redis")
        return False
    
    result = r.delete(lock_key)
    if result:
        print(f"✅ Lock eliminado: {lock_key}")
        return True
    else:
        print(f"⚠️  Lock no encontrado: {lock_key}")
        return False

def clear_all_flow_locks():
    """Elimina TODOS los flow locks (usar con precaución)"""
    r = get_redis()
    if not r:
        print("❌ No se pudo conectar a Redis")
        return 0
    
    keys = r.keys("flow_lock:*")
    if not keys:
        print("✅ No hay flow locks para limpiar")
        return 0
    
    count = 0
    for key in keys:
        if r.delete(key):
            count += 1
            key_str = key.decode() if isinstance(key, bytes) else key
            print(f"  ✅ Eliminado: {key_str}")
    
    print(f"\n✅ Total locks eliminados: {count}")
    return count

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Gestionar flow locks de Redis")
    parser.add_argument(
        "action",
        choices=["list", "clear", "clear-all"],
        help="Acción a realizar"
    )
    parser.add_argument(
        "--lock",
        help="Nombre del lock a eliminar (ej: flow_lock:magazine:1)",
        default=None
    )
    
    args = parser.parse_args()
    
    if args.action == "list":
        list_all_flow_locks()
    
    elif args.action == "clear":
        if not args.lock:
            print("❌ Error: Se requiere --lock para la acción 'clear'")
            print("   Ejemplo: python clear_flow_locks.py clear --lock flow_lock:magazine:1")
            sys.exit(1)
        clear_flow_lock(args.lock)
    
    elif args.action == "clear-all":
        confirm = input("⚠️  ¿Estás seguro de eliminar TODOS los flow locks? (y/N): ")
        if confirm.lower() == "y":
            clear_all_flow_locks()
        else:
            print("Operación cancelada")
