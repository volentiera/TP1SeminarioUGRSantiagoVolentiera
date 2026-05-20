from sqlalchemy.sql import text
from price_manager.database.connection import ConexionDB

def crear_tablas():
    """Crea todas las tablas del sistema en la base de datos SQLite usando SQL crudo."""
    db = ConexionDB()
    
    # Utilizamos el context manager para asegurar la transacción
    with db.transaccion() as conn:
        
        # Tabla Categorías
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY,
            nombre VARCHAR NOT NULL
        );
        """))
        
        # Tabla Proveedores
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY,
            nombre VARCHAR NOT NULL,
            contacto VARCHAR
        );
        """))
        
        # Tabla Monedas
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS monedas (
            id INTEGER PRIMARY KEY,
            nombre VARCHAR NOT NULL
        );
        """))
        
        # Tabla Tipos de Cotización
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS tipos_cotizacion (
            id INTEGER PRIMARY KEY,
            nombre VARCHAR NOT NULL
        );
        """))
        
        # Tabla Productos (con sus claves foráneas)
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY,
            nombre VARCHAR NOT NULL,
            descripcion VARCHAR,
            precio_valor REAL NOT NULL,
            moneda_id INTEGER NOT NULL,
            fecha_precio DATE NOT NULL,
            categoria_id INTEGER NOT NULL,
            proveedor_id INTEGER NOT NULL,
            FOREIGN KEY (moneda_id) REFERENCES monedas(id),
            FOREIGN KEY (categoria_id) REFERENCES categorias(id),
            FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
        );
        """))
        
        # Tabla Stock (producto_id actúa como PK y FK al mismo tiempo)
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS stock (
            producto_id INTEGER PRIMARY KEY,
            cantidad INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        );
        """))
        
        # Tabla Cotizaciones Dólar
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS cotizaciones_dolar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor REAL NOT NULL,
            fecha DATE NOT NULL,
            tipo_id INTEGER NOT NULL,
            FOREIGN KEY (tipo_id) REFERENCES tipos_cotizacion(id)
        );
        """))

# Dejamos un bloque de ejecución directa por si se quiere correr solo este archivo
if __name__ == "__main__":
    crear_tablas()
    print("Tablas creadas exitosamente en la base de datos.")
