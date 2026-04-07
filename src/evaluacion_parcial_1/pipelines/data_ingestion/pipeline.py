"""
This is a boilerplate pipeline 'data_ingestion'
generated using Kedro 1.2.0
"""

from kedro.pipeline import node, Pipeline
from .nodes import (
    explore_clientes,
    explore_productos,
    explore_ventas,
    explore_devoluciones,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=explore_clientes,
                inputs="clientes",
                outputs="clientes_raw",
                name="explore_clientes_node",
            ),
            node(
                func=explore_productos,
                inputs="productos",
                outputs="productos_raw",
                name="explore_productos_node",
            ),
            node(
                func=explore_ventas,
                inputs="ventas",
                outputs="ventas_raw",
                name="explore_ventas_node",
            ),
            node(
                func=explore_devoluciones,
                inputs="devoluciones",
                outputs="devoluciones_raw",
                name="explore_devoluciones_node",
            ),
        ]
    )

