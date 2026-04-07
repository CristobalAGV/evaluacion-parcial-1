"""
This is a boilerplate pipeline 'data_ingestion'
generated using Kedro 1.2.0
"""
import pandas as pd


def explore_clientes(clientes):
    print("Clientes Shape:", clientes.shape)
    print(clientes.info())
    return clientes


def explore_productos(productos):
    print("Productos Shape:", productos.shape)
    print(productos.info())
    return productos


def explore_ventas(ventas):
    print("Ventas Shape:", ventas.shape)
    print(ventas.info())
    return ventas


def explore_devoluciones(devoluciones):
    print("Devoluciones Shape:", devoluciones.shape)
    print(devoluciones.info())
    return devoluciones