import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

class ConexionDB:
    """Clase responsable de inicializar y gestionar el motor de base de datos SQLite y transacciones."""
    
    def __init__(self):
        # Creamos el directorio base tal como lo indica el profesor en su ejemplo
        self.data_base_directory = '/content/base_de_datos/'
        os.makedirs(self.data_base_directory, exist_ok=True)
        
        # Definimos el nombre del archivo de nuestra base de datos relacional
        self.data_base_name = 'price_manager.db'
        
        # Creamos el engine (motor). echo=False evita que la consola se llene de logs.
        self.engine = create_engine(
            f'sqlite:///{self.data_base_directory}{self.data_base_name}', 
            echo=False
        )

    def connect(self):
        """Retorna el objeto de conexión activo."""
        return self.engine.connect()

    @contextmanager
    def transaccion(self):
        """
        Context manager para manejar transacciones de forma segura.
        Realiza commit si no hay excepciones, y rollback si ocurre algún error.
        """
        connection = self.connect()
        transaction = connection.begin()
        try:
            # Cedemos el control de la conexión al bloque 'with'
            yield connection
            # Si el bloque termina sin errores, guardamos los cambios
            transaction.commit()
        except Exception as e:
            # Si ocurre un error, deshacemos todos los cambios
            transaction.rollback()
            print(f"Error en la transacción. Rollback ejecutado. Detalle: {e}")
            raise
        finally:
            # Siempre cerramos la conexión y la transacción al finalizar
            transaction.close()
            connection.close()
