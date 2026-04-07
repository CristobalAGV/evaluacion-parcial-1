"""
This is a boilerplate pipeline 'data_transform'
generated using Kedro 1.2.0
"""

"""
Pipeline de transformación de datos.

Este pipeline aplica transformaciones sobre los datos limpios
para prepararlos para análisis y reporte.
"""

from kedro.pipeline import node, Pipeline

# Importamos las funciones de transformación desde nodes.py
from .nodes import (
    transformar_clientes,
    transformar_productos,
    transformar_ventas,
    transformar_devoluciones,
)


def create_pipeline(**kwargs) -> Pipeline:
    """
    Definición del pipeline de transformación.
    Cada node transforma un dataset limpio.
    """
    return Pipeline(
        [
            # Transformación dataset clientes
            node(
                func=transformar_clientes,
                inputs="clientes_clean",
                outputs="clientes_transform",
                name="transformar_clientes_node",
            ),

            # Transformación dataset productos
            node(
                func=transformar_productos,
                inputs="productos_clean",
                outputs="productos_transform",
                name="transformar_productos_node",
            ),

            # Transformación dataset ventas
            node(
                func=transformar_ventas,
                inputs="ventas_clean",
                outputs="ventas_transform",
                name="transformar_ventas_node",
            ),

            # Transformación dataset devoluciones
            node(
                func=transformar_devoluciones,
                inputs="devoluciones_clean",
                outputs="devoluciones_transform",
                name="transformar_devoluciones_node",
            ),
        ]
    )