# Price Manager

## Sprint Finalizado: Sprint 1

## Objetivo
Desarrollar una aplicación de consola (CLI) en Python para gestionar el
inventario de un local de hardware, cotizar productos en tiempo real según
el valor del dólar y comparar precios con la competencia web.

## Introducción y Contexto
Una empresa distribuidora de productos electrónicos necesita modernizar su
sistema de gestión de inventarios. Debido a la volatilidad económica, el
sistema debe gestionar precios en diferentes monedas y hacer seguimiento de
la cotización del dólar para actualizar sus valores en tiempo real.
El desarrollo sigue una metodología incremental y colaborativa, simulando
un entorno real de trabajo en equipo con control de versiones Git.

## Sprint Actual: Sprint 2

## Objetivo
El objetivo principal de este proyecto es consolidar los conocimientos de programación orientada a objetos y evolucionar el sistema hacia el almacenamiento persistente utilizando una base de datos relacional (SQLite mediante el ORM SQLAlchemy).

## Introducción y Contexto
Una empresa distribuidora de productos electrónicos necesita modernizar su sistema de gestión de inventarios. Debido a la volatilidad económica, el sistema debe gestionar precios en diferentes monedas y hacer seguimiento de la cotización del dólar para actualizar sus valores.

En este segundo sprint, hemos migrado el almacenamiento de datos inicial hacia tablas relacionales. Además, integramos el consumo de una API externa (DolarAPI) para obtener las cotizaciones en tiempo real de forma automática, garantizando transacciones seguras y persistencia a largo plazo.

## Características Principales
* **Gestión de Inventario y Stock:** Control preciso de cantidades y productos.
* **Soporte CRUD Completo:** Creación, lectura, actualización y eliminación de Categorías, Proveedores, Monedas y Tipos de Cotización.
* **Integración con DolarAPI:** Descarga y registro automático de cotizaciones históricas y actuales.
* **Reportes Bimonetarios:** Visualización cruzada de precios (ARS/USD) al instante.
* **Exportación de Datos:** Generación de listas de precios actualizadas en formato CSV.

## Requisitos Previos
El proyecto requiere Python y las siguientes librerías de terceros:
* `sqlalchemy` (Manejo de base de datos y ORM)
* `requests` (Consumo de la API externa)
* `python-dotenv` (Gestión de variables de entorno)

Puedes instalarlas ejecutando:
`pip install sqlalchemy requests python-dotenv`

## Configuración Inicial
Crea un archivo llamado `.env` en la raíz del proyecto (al mismo nivel que la carpeta `src`) con el siguiente contenido:
`API_URL=https://dolarapi.com/v1/dolares`

## Instrucciones de Ejecución
El proyecto utiliza una estructura de paquetes dentro de la carpeta `src`. Sigue estos pasos para ejecutarlo correctamente:

1. Abre una terminal y posiciónate dentro de la carpeta `src`:
   `cd src`

2. Ejecuta el sistema tratando a `main.py` como un módulo de Python:
   `python -m price_manager.main`

> **Nota:** La primera vez que se ejecute el sistema, se creará automáticamente la base de datos `price_manager.db` y sus tablas correspondientes, además de precargar los datos iniciales necesarios para su funcionamiento.

## Autores
* Grupo 13 - Santiago Volentiera# Price Manager - Sprint 3

## Sprint actual
Sprint 3 - Web Scraping y comparación de precios con la competencia.

## Objetivo
Aplicar los conocimientos de programación orientada a objetos y
persistencia de datos, incorporando la obtención de datos desde la web
(scraping) para comparar los precios internos con los de la competencia
(Star Computación) y generar alertas y reportes.

## Introducción y contexto
Una empresa distribuidora de productos electrónicos necesita competir
con los precios del mercado. En este tercer sprint se obtienen los
precios de la competencia mediante scraping, se comparan con los precios
internos almacenados en la base de datos relacional, y se generan alertas
(CSV) y reportes (Excel) para la toma de decisiones. El sistema registra
además una auditoría de cada operación realizada.

## Funcionalidades principales
- Gestión de inventario, stock y entidades (CRUD completo).
- Cotización del dólar en tiempo real (DolarAPI).
- Reporte bimonetario y exportación a CSV.
- Scraping de precios de la competencia con Scrapy.
- Generación de alertas por diferencia de precios.
- Reporte Excel comparativo.
- Auditoría de operaciones del sistema.
