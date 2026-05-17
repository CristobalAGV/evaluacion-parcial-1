"""
data_preprocessing.py
=====================
Funciones de limpieza, transformación y preparación de datos para el proyecto de ML.

Autores: Equipo Evaluación Parcial N°2 - SCY1101
"""

import pandas as pd
import numpy as np
import re
import os

# ──────────────────────────────────────────────
# CONSTANTES
# ──────────────────────────────────────────────

RAW_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')

ENCODING = 'latin1'

# Mapas de normalización para variables categóricas
MAPA_METODO_PAGO = {
    'tarjeta crédito': 'Tarjeta Crédito',
    'tarjeta credito': 'Tarjeta Crédito',
    'tarjeta débito': 'Tarjeta Débito',
    'tarjeta debito': 'Tarjeta Débito',
    'webpay': 'Webpay',
    'transferencia': 'Transferencia',
    'efectivo': 'Efectivo',
}

MAPA_SEGMENTO = {
    'regular': 'Regular',
    'vip': 'VIP',
    'premium': 'Premium',
    'nuevo': 'Nuevo',
}

MAPA_CATEGORIA = {
    'belleza': 'Belleza',
    'deportes': 'Deportes',
    'alimentos': 'Alimentos',
    'hogar': 'Hogar',
    'ropa': 'Ropa',
    'tecnología': 'Tecnología',
    'tecnologia': 'Tecnología',
    'electrónica': 'Electrónica',
    'electronica': 'Electrónica',
}

MAPA_MOTIVO = {
    'talla incorrecta': 'Talla incorrecta',
    'llegó dañado': 'Llegó dañado',
    'llego danado': 'Llegó dañado',
    'no es lo esperado': 'No es lo esperado',
    'defectuoso': 'Defectuoso',
    'cambio de opinión': 'Cambio de opinión',
    'cambio de opinion': 'Cambio de opinión',
}

MAPA_ESTADO_DEV = {
    'en revisión': 'En revisión',
    'en revision': 'En revisión',
    'pendiente': 'Pendiente',
    'rechazada': 'Rechazada',
    'procesada': 'Procesada',
}


# ──────────────────────────────────────────────
# FUNCIONES UTILITARIAS
# ──────────────────────────────────────────────

def fix_encoding(text: str) -> str:
    """
    Corrige errores de doble codificación latin1→UTF-8 comunes en los datos.

    Parameters
    ----------
    text : str
        Texto con posibles caracteres mal codificados.

    Returns
    -------
    str
        Texto corregido.
    """
    if not isinstance(text, str):
        return text
    try:
        return text.encode('latin1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


def normalizar_categorica(valor: str, mapa: dict) -> str:
    """
    Normaliza un valor categórico usando un mapa de referencia.
    Elimina espacios, convierte a minúsculas y busca en el mapa.

    Parameters
    ----------
    valor : str
        Valor a normalizar.
    mapa : dict
        Diccionario {clave_normalizada: valor_final}.

    Returns
    -------
    str
        Valor normalizado o NaN si no se encuentra.
    """
    if pd.isna(valor):
        return np.nan
    key = str(valor).strip().lower()
    # Corregir encoding primero
    key = fix_encoding(key)
    return mapa.get(key, np.nan)


def parsear_fecha(serie: pd.Series) -> pd.Series:
    """
    Parsea una serie de fechas con formatos mixtos (YYYY-MM-DD y DD/MM/YYYY).

    Parameters
    ----------
    serie : pd.Series
        Serie con fechas como strings.

    Returns
    -------
    pd.Series
        Serie con fechas como datetime.
    """
    def _parse(val):
        if pd.isna(val):
            return pd.NaT
        val = str(val).strip()
        for fmt in ('%Y-%m-%d', '%d/%m/%Y'):
            try:
                return pd.to_datetime(val, format=fmt)
            except ValueError:
                continue
        return pd.NaT

    return serie.apply(_parse)


# ──────────────────────────────────────────────
# FUNCIONES DE CARGA
# ──────────────────────────────────────────────

def cargar_datos_raw() -> dict:
    """
    Carga los cuatro datasets raw desde data/raw/.

    Returns
    -------
    dict
        Diccionario con DataFrames: 'clientes', 'ventas', 'productos', 'devoluciones'.
    """
    return {
        'clientes':    pd.read_csv(os.path.join(RAW_PATH, 'clientes.csv'), encoding=ENCODING),
        'ventas':      pd.read_csv(os.path.join(RAW_PATH, 'ventas.csv'), encoding=ENCODING),
        'productos':   pd.read_csv(os.path.join(RAW_PATH, 'productos.csv'), encoding=ENCODING),
        'devoluciones':pd.read_csv(os.path.join(RAW_PATH, 'devoluciones.csv'), encoding=ENCODING),
    }


# ──────────────────────────────────────────────
# LIMPIEZA POR DATASET
# ──────────────────────────────────────────────

def limpiar_clientes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia el dataset de clientes:
    - Elimina duplicados
    - Corrige encoding en columnas de texto
    - Normaliza 'segmento' y 'region'
    - Parsea 'fecha_registro'
    - Elimina filas sin id_cliente

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame raw de clientes.

    Returns
    -------
    pd.DataFrame
        DataFrame limpio.
    """
    df = df.copy()

    # Eliminar duplicados
    df = df.drop_duplicates()

    # Eliminar filas sin ID (no podemos identificarlas)
    df = df.dropna(subset=['id_cliente'])
    df['id_cliente'] = df['id_cliente'].astype(int)

    # Corregir encoding en columnas de texto
    for col in ['nombre', 'email', 'region', 'ciudad']:
        df[col] = df[col].apply(fix_encoding).str.strip()

    # Normalizar segmento
    df['segmento'] = df['segmento'].apply(
        lambda x: normalizar_categorica(x, MAPA_SEGMENTO)
    )

    # Normalizar region (corregir encoding)
    df['region'] = df['region'].apply(fix_encoding).str.strip()

    # Parsear fecha_registro
    df['fecha_registro'] = parsear_fecha(df['fecha_registro'])

    # Rellenar nulos restantes en segmento con moda
    moda_segmento = df['segmento'].mode()[0]
    df['segmento'] = df['segmento'].fillna(moda_segmento)

    df = df.reset_index(drop=True)
    return df


def limpiar_productos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia el dataset de productos:
    - Elimina duplicados
    - Corrige encoding
    - Normaliza 'categoria' y 'subcategoria'
    - Convierte tipos numéricos
    - Elimina filas sin id_producto

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame raw de productos.

    Returns
    -------
    pd.DataFrame
        DataFrame limpio.
    """
    df = df.copy()
    df = df.drop_duplicates()
    df = df.dropna(subset=['id_producto'])
    df['id_producto'] = df['id_producto'].astype(int)

    # Corregir encoding en nombre
    df['nombre'] = df['nombre'].apply(fix_encoding).str.strip()

    # Normalizar categoria
    df['categoria'] = df['categoria'].apply(
        lambda x: normalizar_categorica(x, MAPA_CATEGORIA)
    )

    # Normalizar subcategoria (solo strip + fix encoding)
    df['subcategoria'] = df['subcategoria'].apply(fix_encoding).str.strip().str.title()

    # Normalizar proveedor
    df['proveedor'] = df['proveedor'].str.strip()

    # Tipos numéricos
    df['precio_lista'] = pd.to_numeric(df['precio_lista'], errors='coerce')
    df['stock'] = pd.to_numeric(df['stock'], errors='coerce').astype('Int64')

    # Rellenar nulos en categoria con moda
    moda_cat = df['categoria'].mode()[0]
    df['categoria'] = df['categoria'].fillna(moda_cat)

    # Rellenar nulos en precio_lista con mediana por categoria
    df['precio_lista'] = df.groupby('categoria')['precio_lista'].transform(
        lambda x: x.fillna(x.median())
    )

    df = df.reset_index(drop=True)
    return df


def limpiar_ventas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia el dataset de ventas:
    - Elimina duplicados
    - Corrige encoding en metodo_pago y canal_venta
    - Normaliza metodo_pago (múltiples variantes → 5 categorías)
    - Parsea fechas con formato mixto
    - Convierte cantidad y precio_unitario a numérico
    - Calcula total_venta
    - Elimina filas sin id_venta o sin fecha válida

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame raw de ventas.

    Returns
    -------
    pd.DataFrame
        DataFrame limpio.
    """
    df = df.copy()
    df = df.drop_duplicates()
    df = df.dropna(subset=['id_venta'])
    df['id_venta'] = df['id_venta'].astype(int)

    # Parsear fecha
    df['fecha'] = parsear_fecha(df['fecha'])
    df = df.dropna(subset=['fecha'])

    # Normalizar metodo_pago
    df['metodo_pago'] = df['metodo_pago'].apply(fix_encoding)
    df['metodo_pago'] = df['metodo_pago'].apply(
        lambda x: normalizar_categorica(x, MAPA_METODO_PAGO)
    )
    moda_mp = df['metodo_pago'].mode()[0]
    df['metodo_pago'] = df['metodo_pago'].fillna(moda_mp)

    # Normalizar canal_venta
    df['canal_venta'] = df['canal_venta'].apply(fix_encoding).str.strip()

    # Tipos numéricos
    df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
    df['precio_unitario'] = pd.to_numeric(
        df['precio_unitario'].astype(str).str.replace(',', '.'), errors='coerce'
    )

    # Eliminar filas sin cantidad o precio (no podemos imputar ventas)
    df = df.dropna(subset=['cantidad', 'precio_unitario'])
    df['cantidad'] = df['cantidad'].astype(int)

    # Calcular total_venta
    df['total_venta'] = df['cantidad'] * df['precio_unitario']

    # IDs relacionados como Int (nullable)
    df['id_cliente'] = pd.to_numeric(df['id_cliente'], errors='coerce').astype('Int64')
    df['id_producto'] = pd.to_numeric(df['id_producto'], errors='coerce').astype('Int64')

    # Features temporales
    df['mes'] = df['fecha'].dt.month
    df['dia_semana'] = df['fecha'].dt.dayofweek  # 0=lunes
    df['trimestre'] = df['fecha'].dt.quarter

    df = df.reset_index(drop=True)
    return df


def limpiar_devoluciones(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia el dataset de devoluciones:
    - Elimina duplicados
    - Corrige encoding en motivo y estado
    - Normaliza motivo y estado
    - Parsea fecha_devolucion

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame raw de devoluciones.

    Returns
    -------
    pd.DataFrame
        DataFrame limpio.
    """
    df = df.copy()
    df = df.drop_duplicates()
    df = df.dropna(subset=['id_venta'])
    df['id_venta'] = df['id_venta'].astype(int)

    df['fecha_devolucion'] = parsear_fecha(df['fecha_devolucion'])

    df['motivo'] = df['motivo'].apply(
        lambda x: normalizar_categorica(x, MAPA_MOTIVO)
    )
    df['estado'] = df['estado'].apply(
        lambda x: normalizar_categorica(x, MAPA_ESTADO_DEV)
    )

    df = df.reset_index(drop=True)
    return df


# ──────────────────────────────────────────────
# CONSTRUCCIÓN DEL DATASET MAESTRO
# ──────────────────────────────────────────────

def construir_dataset_ml(
    ventas: pd.DataFrame,
    clientes: pd.DataFrame,
    productos: pd.DataFrame,
    devoluciones: pd.DataFrame
) -> pd.DataFrame:
    """
    Une los cuatro datasets limpios para construir el dataset maestro de ML.

    Genera dos targets:
    - 'tiene_devolucion' (0/1): para clasificación binaria.
    - 'total_venta': para regresión.

    Parameters
    ----------
    ventas, clientes, productos, devoluciones : pd.DataFrame
        Datasets ya limpios.

    Returns
    -------
    pd.DataFrame
        Dataset unificado con features y targets.
    """
    # IDs de ventas con devolución
    ids_devolucion = set(devoluciones['id_venta'].dropna().astype(int))

    df = ventas.copy()

    # Target clasificación
    df['tiene_devolucion'] = df['id_venta'].apply(
        lambda x: 1 if x in ids_devolucion else 0
    )

    # Unir con clientes
    clientes_sel = clientes[['id_cliente', 'region', 'segmento']].copy()
    clientes_sel['id_cliente'] = clientes_sel['id_cliente'].astype('Int64')
    df = df.merge(clientes_sel, on='id_cliente', how='left')

    # Unir con productos
    productos_sel = productos[['id_producto', 'categoria', 'precio_lista', 'proveedor']].copy()
    productos_sel['id_producto'] = productos_sel['id_producto'].astype('Int64')
    df = df.merge(productos_sel, on='id_producto', how='left')

    # Feature: diferencia entre precio_unitario y precio_lista
    df['descuento_relativo'] = (
        (df['precio_lista'] - df['precio_unitario']) / df['precio_lista']
    ).clip(-1, 1)

    # Imputar categóricas que quedaron nulas tras el join
    for col in ['region', 'segmento', 'categoria', 'proveedor']:
        if col in df.columns:
            moda = df[col].mode()
            if len(moda) > 0:
                df[col] = df[col].fillna(moda[0])

    return df.reset_index(drop=True)


def pipeline_completo() -> pd.DataFrame:
    """
    Ejecuta el pipeline completo: carga → limpieza → unión → dataset ML.

    Returns
    -------
    pd.DataFrame
        Dataset maestro listo para modelado.
    """
    raw = cargar_datos_raw()

    clientes    = limpiar_clientes(raw['clientes'])
    productos   = limpiar_productos(raw['productos'])
    ventas      = limpiar_ventas(raw['ventas'])
    devoluciones = limpiar_devoluciones(raw['devoluciones'])

    df_ml = construir_dataset_ml(ventas, clientes, productos, devoluciones)

    return df_ml, clientes, productos, ventas, devoluciones
