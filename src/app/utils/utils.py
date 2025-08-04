from entsoe import EntsoePandasClient
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import date
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, root_mean_squared_error, mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, TimeSeriesSplit



def data_transformation(df):
    df.columns = df.columns.get_level_values(0)  
    df = df.astype(float)
    df.index = pd.to_datetime(df.index, utc=True).tz_localize(None)
    df_diario = df.resample('D').sum()
    df_diario.dropna(axis=1, inplace=True)
    df_diario["Total_Renovable"] = df_diario[["Biomass", "Hydro Run-of-river and poundage", "Hydro Water Reservoir", 
                            "Other renewable", "Solar", "Wind Onshore", "Waste"]].sum(axis=1)

    df_diario["Total_Fossil"] = df_diario[["Fossil Gas", "Fossil Hard coal", "Fossil Oil"]].sum(axis=1)
    df_diario.drop(columns=["Hydro Pumped Storage", "Other"], inplace=True)
    df_time_series  = df_diario[['Total_Renovable', 'Total_Fossil', 'Nuclear', 'Solar', 'Fossil Gas']]
    return df_time_series

def prediction_15(df, column):
    # Pipeline con MultiOutput para 15 predicciones
    pipe = Pipeline([
        ('scaler', MinMaxScaler()),
        ('multi_model', MultiOutputRegressor(
            XGBRegressor(
                subsample=0.8,
                reg_lambda=0,
                n_estimators=200,
                max_depth=5,
                learning_rate=0.05,
                gamma=1,
                colsample_bytree=0.8
            )
        ))
    ])
    
    ventana = 30
    horizonte = 15

    serie = df[column].dropna()
    X_multi, Y_multi = [], []

    # Crear lags y etiquetas multisalida
    for i in range(len(serie) - ventana - horizonte + 1):
        X_multi.append(serie[i:i+ventana].values)
        Y_multi.append(serie[i+ventana:i+ventana+horizonte].values)

    X_multi = np.array(X_multi)
    Y_multi = np.array(Y_multi)

    # Entrenar el modelo con todos los datos disponibles
    pipe.fit(X_multi, Y_multi)

    # Última ventana conocida para hacer la predicción
    ultima_ventana = serie[-ventana:].values.reshape(1, -1)
    prediccion = pipe.predict(ultima_ventana)[0]

    # Crear fechas futuras (desde el día siguiente al último)
    fecha_inicio = serie.index[-1] + pd.Timedelta(days=1)
    fechas_futuras = pd.date_range(start=fecha_inicio, periods=horizonte, freq='D')

    # Crear Serie con las predicciones
    pred_series = pd.Series(prediccion, index=fechas_futuras, name='Predicción Solar')

    return pred_series

def comparacion_pred_pasada(new_data, pred_data):
    """
    Visualiza la comparación entre los datos reales y los predichos usando Plotly.

    Parámetros:
    - new_data: pandas.Series con los valores reales (índice = fechas)
    - pred_data: pandas.Series con las predicciones (índice = fechas)
    
    Retorna:
    - fig: Objeto Plotly que puede ser mostrado con st.plotly_chart(fig)
    """
    # Asegurar que los índices estén en formato fecha
    new_data.index = pd.to_datetime(new_data.index)
    pred_data.index = pd.to_datetime(pred_data.index)

    # Normalizar índices si es necesario
    pred_data.index = pred_data.index.normalize()

    # Unir en un solo DataFrame para graficar
    df_plot = pd.DataFrame({
        'Fecha': new_data.index.tolist() + pred_data.index.tolist(),
        'Valor': new_data.values.tolist() + pred_data.values.tolist(),
        'Tipo': ['Real'] * len(new_data) + ['Predicción'] * len(pred_data)
    })

    # Crear gráfico con Plotly Express
    fig = px.line(df_plot, x='Fecha', y='Valor', color='Tipo',
                  markers=True,
                  title='Comparación entre valores reales y predichos')

    fig.update_layout(xaxis_title='Fecha', 
                      yaxis_title='Valor', 
                      xaxis_tickangle=-45, 
                      template='simple_white')
    return fig

def actualización_bbdd(last_time_series, new_data):
    df = pd.concat((last_time_series, new_data), axis=0)
    return df

def visualizar_futuro(last_time_series, new_data, column, predictions):
    """
    Visualiza datos históricos y predicciones futuras con Plotly en Streamlit.
    """
    # Combinar datos pasados
    df_pasado = pd.concat([last_time_series, new_data])
    df_pasado = df_pasado[[column]].copy()
    df_pasado = df_pasado.iloc[-180:]

    # Preparar DataFrame para datos históricos
    df_hist = df_pasado.reset_index().rename(columns={'index': 'Fecha', column: 'Valor'})
    df_hist['Tipo'] = 'Histórico'

    # Asegurar que predictions es una Serie con índice datetime
    df_pred = pd.DataFrame({
        'Fecha': predictions.index,
        'Valor': predictions.values,
        'Tipo': 'Predicción'
    })

    # Concatenar ambos DataFrames
    df_plot = pd.concat([df_hist, df_pred], ignore_index=True)

    # Forzar 'Tipo' como categoría para que Plotly lo interprete correctamente
    df_plot['Tipo'] = df_plot['Tipo'].astype('category')

    # Crear gráfico con Plotly Express
    fig = px.line(df_plot, x='Fecha', y='Valor', color='Tipo', markers=True,
                  title=f'Evolución y predicción de {column}')

    fig.update_layout(
        xaxis_title='Fecha',
        yaxis_title=column,
        xaxis_tickangle=-45,
        template='simple_white'
    )

    return fig

    