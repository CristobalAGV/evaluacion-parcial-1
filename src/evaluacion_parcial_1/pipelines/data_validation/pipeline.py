"""
This is a boilerplate pipeline 'data_validation'
generated using Kedro 1.2.0
"""
"""
Pipeline de validación de datos.

Este pipeline se encarga de verificar la calidad de los datos
provenientes de data_ingestion antes de pasar a limpieza.
"""

from kedro.pipeline import node, Pipeline

# Importamos las funciones de validación creadas en nodes.py
from .nodes import (
    validar_clientes,
    validar_productos,
    validar_ventas,
    validar_devoluciones,
)


def create_pipeline(**kwargs) -> Pipeline:
    """
    Definición del pipeline de validación.
    Cada node representa una validación de dataset.
    """
    return Pipeline(
        [
            # Validación dataset clientes
            node(
                func=validar_clientes,
                inputs="clientes_raw",
                outputs="clientes_validated",
                name="validar_clientes_node",
            ),

            # Validación dataset productos
            node(
                func=validar_productos,
                inputs="productos_raw",
                outputs="productos_validated",
                name="validar_productos_node",
            ),

            # Validación dataset ventas
            node(
                func=validar_ventas,
                inputs="ventas_raw",
                outputs="ventas_validated",
                name="validar_ventas_node",
            ),

            # Validación dataset devoluciones
            node(
                func=validar_devoluciones,
                inputs="devoluciones_raw",
                outputs="devoluciones_validated",
                name="validar_devoluciones_node",
            ),
        ]
    )