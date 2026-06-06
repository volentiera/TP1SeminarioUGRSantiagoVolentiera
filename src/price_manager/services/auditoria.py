import functools
from datetime import datetime
from price_manager.database.connection import ConexionDB
from sqlalchemy import text

def auditar(accion: str):
    """Decorador para registrar auditoría de operaciones en la BD."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            db = ConexionDB()
            # Aseguramos que la tabla de auditoría exista
            with db.transaccion() as conn:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS auditoria (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        accion TEXT,
                        fecha TEXT,
                        detalles TEXT
                    )
                """))
            
            # Ejecutamos la función original
            try:
                resultado = func(*args, **kwargs)
                estado = "Ejecución exitosa"
            except Exception as e:
                estado = f"Error: {str(e)}"
                raise
            finally:
                # Guardamos el registro de lo que pasó
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                detalles = f"Módulo: '{func.__name__}'. Resultado: {estado}"
                with db.transaccion() as conn:
                    conn.execute(text(
                        "INSERT INTO auditoria (accion, fecha, detalles) VALUES (:a, :f, :d)"
                    ), {"a": accion, "f": fecha, "d": detalles})
            
            return resultado
        return wrapper
    return decorator

def obtener_historial_auditoria():
    """Recupera los registros de auditoría para el Ejercicio 07."""
    db = ConexionDB()
    historial = []
    try:
        with db.transaccion() as conn:
            # Validamos si la tabla existe primero
            res = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='auditoria'")).fetchone()
            if not res: return []
            
            resultado = conn.execute(text("SELECT accion, fecha, detalles FROM auditoria ORDER BY id DESC"))
            historial = [{"accion": r[0], "fecha": r[1], "detalles": r[2]} for r in resultado]
    except Exception as e:
        print(f"Error al leer auditoría: {e}")
    return historial
