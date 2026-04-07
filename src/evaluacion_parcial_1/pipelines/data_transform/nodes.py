"""
This is a boilerplate pipeline 'data_transform'
generated using Kedro 1.2.0
"""
"""
Pipeline de transformación de datos.

Este archivo contiene funciones que transforman los datos
para análisis y generación de métricas.
"""

import pandas as pd


def transformar_ventas(ventas):
    """
    Transformación del dataset de ventas:
    - Convierte columnas a formato numérico
    - Calcula el total de venta
    - Deja el dataset listo para análisis
    """

    print("Transformando ventas...")

    # Convertimos cantidad a número.
    # errors="coerce" transforma valores inválidos en NaN.
    ventas["cantidad"] = pd.to_numeric(ventas["cantidad"], errors="coerce")

    # Convertimos precio_unitario a número.
    # Esto evita errores cuando la columna viene como texto.
    ventas["precio_unitario"] = pd.to_numeric(ventas["precio_unitario"], errors="coerce")

    # Calculamos el total de venta por fila.
    ventas["total_venta"] = ventas["cantidad"] * ventas["precio_unitario"]

    return ventas


def transformar_devoluciones(devoluciones):
    """
    Transformación dataset devoluciones:
    - Preparación para análisis
    """
    print("Transformando devoluciones...")
    return devoluciones


def transformar_productos(productos):
    """
    Transformación dataset productos:
    - Preparación para análisis
    """
    print("Transformando productos...")
    return productos


def transformar_clientes(clientes):
    """
    Transformación dataset clientes:
    - Preparación para análisis
    """
    print("Transformando clientes...")
    return clientes