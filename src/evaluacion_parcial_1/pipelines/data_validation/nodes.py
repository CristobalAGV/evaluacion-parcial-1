"""
This is a boilerplate pipeline 'data_validation'
generated using Kedro 1.2.0
"""
"""
Pipeline de validación de datos.

Este módulo valida la calidad de los datos:
- Detecta valores nulos
- Revisa duplicados
- Limpia caracteres problemáticos
"""

import pandas as pd


def limpiar_texto(df):
    """
    Limpia caracteres problemáticos en columnas de texto
    """
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(r"[\x00-\x1F\x7F-\x9F]", "", regex=True)
            .str.strip()
        )
    return df


def validar_clientes(clientes):
    print("Validando clientes...")

    print(clientes.isnull().sum())

    clientes = limpiar_texto(clientes)

    return clientes


def validar_productos(productos):
    print("Validando productos...")

    print(productos.isnull().sum())

    productos = limpiar_texto(productos)

    return productos


def validar_ventas(ventas):
    print("Validando ventas...")

    print(ventas.isnull().sum())

    ventas = limpiar_texto(ventas)

    return ventas


def validar_devoluciones(devoluciones):
    print("Validando devoluciones...")

    print(devoluciones.isnull().sum())

    devoluciones = limpiar_texto(devoluciones)

    return devoluciones