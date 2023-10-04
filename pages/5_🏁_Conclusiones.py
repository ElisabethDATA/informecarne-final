import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


sns.set_theme(style = 'dark', palette = 'deep')

st.set_page_config(
    page_title="Conclusiones",
    page_icon="🏁",
)

st.title('Conclusiones')

st.markdown('''
En este proyecto se ha realizado un análisis exploratorio de los datos de consumo de carne en diferentes países del mundo. Se ha realizado un análisis descriptivo de los datos, así como un análisis confirmatorio de la hipótesis planteada.

En el análisis exploratorio se ha observado que el consumo per cápita de carne de ternera ha disminuido en los últimos años en la mayoría de los países, y que el consumo de carne de pollo (o aves) ha aumentado en la mayoría de los mismos. Además, se ha observado que el consumo de carne de pollo es mayor que el de carne de vacuno y porcino en la mayoría de los países.

En el análisis confirmatorio se ha observado mediante la aplicación de pruebas estadísticas que el consumo de carne de pollo ha aumentado en la mayoría de los países, mientras que el consumo de carne de vacuno ha disminuido en la mayoría de los países. Según el análisis realizado utilizando modelos de regresión lineal, se encontró que el consumo de carne en el mundo ha aumentado en general a lo largo del tiempo. Además, se encontraron diferencias significativas en el consumo de diferentes tipos de carne entre países y regiones.

Esto sugiere que el consumo de carne puede estar siendo afectado por factores como la disponibilidad y los precios de la carne, así como por cambios en las preferencias alimentarias de la población en general.

Es importante tener en cuenta que estos resultados se basan en los datos disponibles y en el modelo utilizado, y no necesariamente reflejan toda la complejidad de los factores que influyen en el consumo de carne en todo el mundo. Por lo tanto, estos resultados deben interpretarse con precaución y deben ser validados con datos adicionales y modelos más complejos.

''')