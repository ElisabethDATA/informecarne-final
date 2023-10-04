import statsmodels.api as sm
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from funciones import load_data

sns.set_theme(style = 'dark', palette = 'deep')

st.set_page_config(
    page_title="Análisis Confirmatorio",
    page_icon="📊",
)

# CARGA DE DATOS #
dataset = 'data/processed_data.csv'

data = load_data(dataset)

paises = {'AUS': 'Australia', 'CAN': 'Canada', 'JPN': 'Japan', 'KOR': 'South Korea', 'MEX': 'Mexico', 'NZL': 'New Zealand', 'TUR': 'Turkey', 'USA': 'United States', 'ARG': 'Argentina', 'BRA': 'Brazil', 'CHL': 'Chile', 'CHN': 'China', 'COL': 'Colombia', 'EGY': 'Egypt', 'ETH': 'Ethiopia', 'IND': 'India', 'IDN': 'Indonesia', 'IRN': 'Iran', 'ISR': 'Israel',
          'KAZ': 'Kazakhstan', 'MYS': 'Malaysia', 'NGA': 'Nigeria', 'PAK': 'Pakistan', 'PRY': 'Paraguay', 'PER': 'Peru', 'PHL': 'Philippines', 'RUS': 'Russia', 'SAU': 'Saudi Arabia', 'ZAF': 'South Africa', 'THA': 'Thailand', 'UKR': 'Ukraine', 'VNM': 'Vietnam', 'NOR': 'Norway', 'CHE': 'Switzerland', 'GBR': 'United Kingdom', 'EU27': 'European Union', 'WLD': 'World'} 

def linear_regression(data, country, meat_type):
    tipos = {'BEEF': 'Ternera', 'PIG': 'Cerdo',
             'POULTRY': 'Pollo (Aves)', 'SHEEP': 'Cordero'}
    
    if country == 'European Union':
        data = data[data['TIME'] >= 2000]
    df = data[(data['LOCATION'] == country) & (data['SUBJECT'] == meat_type)]
    x = df['TIME']
    y = df['KG_CAP']

    model = sm.OLS(y, sm.add_constant(x)).fit()

    # Crear figura seaborn
    fig, ax = plt.subplots()
    sns.regplot(x=x, y=y, ax=ax) # Añadir regresión lineal para visualizar tendencia
    ax.set_xlabel('Año')
    ax.set_ylabel('Consumo de carne per cápita (kg)')
    ax.set_title(f'{tipos[meat_type]} - {country}')

    return model.summary(), fig


def contrastar_consumo_carne(df, inicio=2000, fin=2025, confianza=0.95):
    df_filtrado = df.loc[(df['TIME'] >= inicio) & (df['TIME'] <= fin)]

    # Subconjunto de datos de carne de vacuno y de pollo
    df_vacuno = df_filtrado[df_filtrado['SUBJECT'] == 'BEEF']
    df_pollo = df_filtrado[df_filtrado['SUBJECT'] == 'POULTRY']

    # Cálculo del consumo promedio de carne de vacuno y de pollo en cada año
    vacuno_promedio = df_vacuno.groupby('TIME')['KG_CAP'].mean()
    pollo_promedio = df_pollo.groupby('TIME')['KG_CAP'].mean()

    # Contraste de hipótesis
    modelo = sm.OLS(vacuno_promedio, sm.add_constant(pollo_promedio)).fit()
    coeficiente_pollo, p_valor_pollo = modelo.params[1], modelo.pvalues[1]

    # Resultados del contraste de hipótesis
    intervalo_confianza = modelo.conf_int(alpha=1-confianza)[1]
    resultado = {'coeficiente_pollo': coeficiente_pollo, 'p_valor_pollo': p_valor_pollo,
                 'intervalo_confianza': intervalo_confianza, 'confianza': confianza}

    return resultado

st.title('Análisis Confirmatorio')

st.write('En esta sección se realizará un análisis confirmatorio de los datos obtenidos en la sección anterior.')

st.write("En el análisis exploratorio se observan tendencias en los datos, pero no podemos asegurar que estas tendencias sean significativas. Para ello, realizaremos un análisis confirmatorio de los datos. Por ejemplo, en el análisis exploratorio observamos que en la muchos de los países tienen una tendencia a disminuir su consumo de carne de ternera. Sin embargo en muchos otros países, esta tendencia no es tan clara y en algunos países incluso se observa una tendencia a aumentar el consumo de carne de ternera.")

st.write("Para comprobar si esta tendencia es significativa, realizaremos un análisis de regresión lineal simple. Para ello, utilizaremos la librería statsmodels.")

meat_type = st.radio(
    "Seleccionar tipo de carne",
    ('Ternera', 'Cerdo', 'Aves', 'Cordero'))

if meat_type == 'Ternera':
    meat = 'BEEF'
elif meat_type == 'Cerdo':
    meat = 'PIG'
elif meat_type == 'Aves':
    meat = 'POULTRY'
elif meat_type == 'Cordero':
    meat = 'SHEEP'

lista_paises = sorted(list(paises.values()))
country = st.selectbox('Seleccionar país', lista_paises,
                      index=lista_paises.index('European Union'))

result, fig = linear_regression(data, country, meat)


st.subheader('Gráfico')
st.pyplot(fig)


st.write("En este caso, la variable dependiente será el consumo de carne de ternera y la variable independiente será el año.")

st.write("Para realizar el análisis de regresión lineal simple, utilizaremos la función OLS de la librería statsmodels.")


st.subheader('Resumen del modelo')
st.text(result)


resultado = contrastar_consumo_carne(data)

st.write(resultado)