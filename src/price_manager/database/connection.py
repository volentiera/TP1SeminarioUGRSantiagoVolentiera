import os
import sys
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Connection
from typing import Generator

class ConexionDB:
    """Clase responsable de inicializar y gestionar el motor de base de datos SQLite y transacciones."""

    def __init__(self) -> None:
        # Detección automática del entorno
        if 'google.colab' in sys.modules or os.path.exists('/content'):
            # Estamos en Google Colab
            self.data_base_directory = '/content/base_de_datos/'
        else:
            # Estamos en local (VS Code / Windows)
            self.data_base_directory = 'base_de_datos/'
            
        os.makedirs(self.data_base_directory, exist_ok=True)
        self.data_base_name = 'price_manager.db'
        
        self.engine = create_engine(
            f'sqlite:///{self.data_base_directory}{self.data_base_name}',
            echo=False
        )

    def connect(self) -> Connection:
        """Retorna el objeto de conexión activo."""
        return self.engine.connect()

    @contextmanager
    def transaccion(self) -> Generator[Connection, None, None]:
        """
        Context manager para manejar transacciones de forma segura.
        Realiza commit si no hay excepciones, y rollback si ocurre algún error.
        """
        connection = self.connect()
        transaction = connection.begin()
        try:
            yield connection
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            print(f"Error en la transacción. Rollback ejecutado. Detalle: {e}")
            raise
        finally:
            transaction.close()
            connection.close()