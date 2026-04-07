"""
This is a boilerplate pipeline 'data_cleaning'
generated using Kedro 1.2.0
"""
"""
Pipeline de limpieza de datos.

Este archivo contiene funciones que limpian los datos:
- Eliminación de valores nulos
- Eliminación de duplicados
- Limpieza de caracteres extraños en columnas de texto
- Preparación para transformación
"""

import pandas as pd


def limpiar_texto(df):
    """
    Limpia caracteres problemáticos en columnas de texto.
    Recorre todas las columnas tipo object/string y elimina
    caracteres especiales que pueden causar errores de codificación.
    """
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(r"[\x00-\x1F\x7F-\x9F]", "", regex=True)
            .str.strip()
        )
    return df


def limpiar_clientes(clientes):
    """
    Limpieza del dataset de clientes:
    - Elimina valores nulos
    - Elimina duplicados
    - Limpia caracteres problemáticos
    """
    print("Limpiando clientes...")

    clientes = clientes.dropna()
    clientes = clientes.drop_duplicates()
    clientes = limpiar_texto(clientes)

    return clientes


def limpiar_productos(productos):
    """
    Limpieza del dataset de productos:
    - Elimina valores nulos
    - Elimina duplicados
    - Limpia caracteres problemáticos
    """
    print("Limpiando productos...")

    productos = productos.dropna()
    productos = productos.drop_duplicates()
    productos = limpiar_texto(productos)

    return productos


def limpiar_ventas(ventas):
    """
    Limpieza del dataset de ventas:
    - Elimina valores nulos
    - Elimina duplicados
    - Limpia caracteres problemáticos
    """
    print("Limpiando ventas...")

    ventas = ventas.dropna()
    ventas = ventas.drop_duplicates()
    ventas = limpiar_texto(ventas)

    return ventas


def limpiar_devoluciones(devoluciones):
    """
    Limpieza del dataset de devoluciones:
    - Elimina valores nulos
    - Elimina duplicados
    - Limpia caracteres problemáticos
    """
    print("Limpiando devoluciones...")

    devoluciones = devoluciones.dropna()
    devoluciones = devoluciones.drop_duplicates()
    devoluciones = limpiar_texto(devoluciones)

    return devoluciones