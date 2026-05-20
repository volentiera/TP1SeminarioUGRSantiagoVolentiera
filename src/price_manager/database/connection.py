import os
from sqlalchemy import create_engine

class ConexionDB:
    """Clase responsable de inicializar y gestionar el motor de base de datos SQLite."""
    
    def __init__(self):
        # Creamos el directorio base tal como lo indica el profesor en su ejemplo
        self.data_base_directory = '/content/base_de_datos/'
        os.makedirs(self.data_base_directory, exist_ok=True)
        
        # Definimos el nombre del archivo de nuestra base de datos relacional
        self.data_base_name = 'price_manager.db'
        
        # Creamos el engine (motor). echo=False evita que la consola se llene de logs en cada query.
        self.engine = create_engine(
            f'sqlite:///{self.data_base_directory}{self.data_base_name}', 
            echo=False
        )

    def connect(self):
        """Retorna el objeto de conexión activo para poder ejecutar sentencias."""
        return self.engine.connect()
