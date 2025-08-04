from entsoe import EntsoePandasClient
import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
from datetime import date
from utils.utils import *

tabs = ['Total_Renovable', 'Total_Fossil', 'Nuclear', 'Solar', 'Fossil Gas']
last_df = pd.read_csv(
    r'..\data\produccion_electrica_ES.csv',
    header=[0, 1],           
    index_col=0,             
    parse_dates=True,        
    low_memory=False)

last_time_series = data_transformation(last_df)
last_date= last_time_series.tail(1).index

today_date = date.today()

start = pd.Timestamp(last_date[0], tz='UTC')
end = pd.Timestamp(today_date, tz='UTC')

with open(r'..\..\token.txt', 'r') as file:
    API_KEY = file.read()


client = EntsoePandasClient(api_key=API_KEY)

new_download = client.query_generation(
    country_code='ES',
    start=start, end=end
)

new_data = data_transformation(new_download)

tab1, tab2, tab3, tab4, tab5 = st.tabs(tabs)

with tab1:
    st.header(f"Total Renovable energy production in ES")
    st.markdown(f"### Última actualización el {str(last_date[0])[:10]}")
    st.line_chart(last_time_series[tabs[0]], use_container_width=True)
    predictions = prediction_15(last_time_series, tabs[0])
    fig = comparacion_pred_pasada(new_data[tabs[0]], predictions)
    st.plotly_chart(fig)
    future_predictions = prediction_15(actualización_bbdd(last_time_series, new_data), tabs[0])
    fig = visualizar_futuro(last_time_series, new_data, tabs[0], future_predictions)
    st.plotly_chart(fig)

with tab2:
    st.header(f"Total Fossil energy production in ES")
    st.markdown(f"### Última actualización el {str(last_date[0])[:10]}")
    st.line_chart(last_time_series[tabs[1]], use_container_width=True)
    predictions = prediction_15(last_time_series, tabs[1])
    fig = comparacion_pred_pasada(new_data[tabs[1]], predictions)
    st.plotly_chart(fig)
    future_predictions = prediction_15(actualización_bbdd(last_time_series, new_data), tabs[1])
    fig = visualizar_futuro(last_time_series, new_data, tabs[1], future_predictions)
    st.plotly_chart(fig)
with tab3:
    st.header(f"Nuclear energy production in ES")
    st.markdown(f"### Última actualización el {str(last_date[0])[:10]}")
    st.line_chart(last_time_series[tabs[2]], use_container_width=True)
    predictions = prediction_15(last_time_series, tabs[2])
    fig = comparacion_pred_pasada(new_data[tabs[2]], predictions)
    st.plotly_chart(fig)
    future_predictions = prediction_15(actualización_bbdd(last_time_series, new_data), tabs[2])
    fig = visualizar_futuro(last_time_series, new_data, tabs[2], future_predictions)
    st.plotly_chart(fig)
with tab4:
    st.header(f"Solar energy production in ES")
    st.markdown(f"### Última actualización el {str(last_date[0])[:10]}")
    st.line_chart(last_time_series[tabs[3]], use_container_width=True)
    predictions = prediction_15(last_time_series, tabs[3])
    fig = comparacion_pred_pasada(new_data[tabs[3]], predictions)
    st.plotly_chart(fig)
    future_predictions = prediction_15(actualización_bbdd(last_time_series, new_data), tabs[3])
    fig = visualizar_futuro(last_time_series, new_data, tabs[3], future_predictions)
    st.plotly_chart(fig)
with tab5:
    st.header(f"Fossil Gas energy production in ES")
    st.markdown(f"### Última actualización el {str(last_date[0])[:10]}")
    st.line_chart(last_time_series[tabs[4]], use_container_width=True)        
    predictions = prediction_15(last_time_series, tabs[4])
    fig = comparacion_pred_pasada(new_data[tabs[4]], predictions)
    st.plotly_chart(fig)
    future_predictions = prediction_15(actualización_bbdd(last_time_series, new_data), tabs[4])
    fig = visualizar_futuro(last_time_series, new_data, tabs[4], future_predictions)
    st.plotly_chart(fig)

df_final = actualización_bbdd(last_df, new_download)
df_final.to_csv(r'..\data\produccion_electrica_ES.csv')