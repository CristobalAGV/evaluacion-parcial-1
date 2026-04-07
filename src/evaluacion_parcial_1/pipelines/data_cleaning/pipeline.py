"""
This is a boilerplate pipeline 'data_cleaning'
generated using Kedro 1.2.0
"""
"""
Pipeline de limpieza de datos.

Este pipeline se encarga de limpiar los datos validados:
- Eliminar valores nulos
- Eliminar duplicados
- Preparar datos para transformación
"""

from kedro.pipeline import node, Pipeline

# Importamos las funciones de limpieza desde nodes.py
from .nodes import (
    limpiar_clientes,
    limpiar_productos,
    limpiar_ventas,
    limpiar_devoluciones,
)


def create_pipeline(**kwargs) -> Pipeline:
    """
    Definición del pipeline de limpieza.
    Cada node representa la limpieza de un dataset.
    """
    return Pipeline(
        [
            # Limpieza dataset clientes
            node(
                func=limpiar_clientes,
                inputs="clientes_validated",
                outputs="clientes_clean",
                name="limpiar_clientes_node",
            ),

            # Limpieza dataset productos
            node(
                func=limpiar_productos,
                inputs="productos_validated",
                outputs="productos_clean",
                name="limpiar_productos_node",
            ),

            # Limpieza dataset ventas
            node(
                func=limpiar_ventas,
                inputs="ventas_validated",
                outputs="ventas_clean",
                name="limpiar_ventas_node",
            ),

            # Limpieza dataset devoluciones
            node(
                func=limpiar_devoluciones,
                inputs="devoluciones_validated",
                outputs="devoluciones_clean",
                name="limpiar_devoluciones_node",
            ),
        ]
    )