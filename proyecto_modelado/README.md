# Proyecto Modelado — SCY1101 Evaluación Parcial N°2

## Descripción
Pipeline completo de Machine Learning sobre datos de ventas retail.
- **Clasificación**: predecir si una venta tendrá devolución
- **Regresión**: predecir el monto total de venta

## Estructura
```
proyecto_modelado/
├── notebooks/
│   ├── 01_exploratory_analysis.ipynb     # EDA y limpieza
│   ├── 02_supervised_modeling.ipynb      # Modelos supervisados
│   ├── 03_model_evaluation.ipynb         # Evaluación comparativa
│   ├── 04_hyperparameter_optimization.ipynb  # Optimización
│   └── 05_final_analysis.ipynb           # Análisis final
├── src/
│   ├── data_preprocessing.py             # Limpieza y preparación
│   ├── model_training.py                 # Entrenamiento de modelos
│   ├── model_evaluation.py               # Métricas y comparación
│   └── hyperparameter_tuning.py          # Optimización hiperparámetros
├── data/
│   └── raw/                              # CSVs originales
├── models/trained_models/                # Modelos serializados (.pkl)
└── results/
    ├── metrics/                          # Tablas de métricas
    ├── plots/                            # Gráficos generados
    └── reports/                          # Reportes finales
```

## Instalación
```bash
pip install scikit-learn pandas numpy matplotlib seaborn jupyter
```

## Ejecución
Abrir los notebooks en orden desde Jupyter Lab/Notebook o VS Code.
