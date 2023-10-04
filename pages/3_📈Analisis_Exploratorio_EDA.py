import streamlit as st
from funciones import load_data, plot_meat_consumption, plot_consumption_all, plot_meat_subject, split_measure, replace_country_code, plot_top_consumers, plot_dispersion
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Gráficos",
    page_icon="📈",
)

# Funciones para filtrar los datos.


def select_year(df, year):
    df_year = df[df['TIME'] == year]
    return df_year


def plot_subjects(ndf):
    kg_cap = ndf[ndf["MEASURE"] == 'KG_CAP']
    thnd_tonne = ndf[ndf['MEASURE'] == 'THND_TONNE']

    kg_cap_wld = kg_cap[kg_cap['LOCATION'] == 'World']
    thnd_tonne_wld = thnd_tonne[thnd_tonne['LOCATION'] == 'World']

    subjects = ndf['SUBJECT'].unique()

    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

    colors = sns.color_palette('Paired', n_colors=len(subjects)*2+1) # Paleta de 10 colores por pares

    for i, subject in enumerate(subjects):
        row = i // 2
        col = i % 2

        data1 = thnd_tonne_wld[thnd_tonne_wld['SUBJECT'] == subject]
        axs[row, col].bar(data1['TIME'], data1['VALUE'], color=colors[i*2]) # Barra de miles de toneladas colores impares
        axs[row, col].set_ylabel("Miles de Toneladas", fontsize=12)

        ax2 = axs[row, col].twinx()

        data2 = kg_cap_wld[kg_cap_wld['SUBJECT'] == subject]
        ax2.plot(data2['TIME'], data2['VALUE'], color=colors[i*2+1]) # Linea de Kg per cápita colores pares

        ax2.set_ylabel("Kg per cápita", fontsize=10)

        axs[row, col].set_title(subject)

    plt.tight_layout()
    plt.show()


paises = {'AUS': 'Australia', 'CAN': 'Canada', 'JPN': 'Japan', 'KOR': 'South Korea', 'MEX': 'Mexico', 'NZL': 'New Zealand', 'TUR': 'Turkey', 'USA': 'United States', 'ARG': 'Argentina', 'BRA': 'Brazil', 'CHL': 'Chile', 'CHN': 'China', 'COL': 'Colombia', 'EGY': 'Egypt', 'ETH': 'Ethiopia', 'IND': 'India', 'IDN': 'Indonesia', 'IRN': 'Iran', 'ISR': 'Israel', 'KAZ': 'Kazakhstan', 'MYS': 'Malaysia', 'NGA': 'Nigeria', 'PAK': 'Pakistan', 'PRY': 'Paraguay', 'PER': 'Peru', 'PHL': 'Philippines', 'RUS': 'Russia', 'SAU': 'Saudi Arabia', 'ZAF': 'South Africa', 'THA': 'Thailand', 'UKR': 'Ukraine', 'VNM': 'Vietnam', 'NOR': 'Norway', 'CHE': 'Switzerland', 'GBR': 'United Kingdom', 'EU27': 'European Union', 'WLD': 'World'}


def prepare_data(df):
    df = split_measure(df)
    df = replace_country_code(df)
    return df


st.sidebar.subheader('Índice')
st.sidebar.markdown("""
<style>
    .indice {list-style: none;}
    .indice li a {text-decoration: none; color: #000;}
    .indice li a:hover {color: #FF4B4B;}
</style>
<ul class="indice">
    <li><a href="#distribuci-n-de-consumo-por-tipo-de-carne">Distribución de consumo de carne</a></li>
    <li><a href="#top-10-pa-ses-consumidores">Top 10 países consumidores</a></li>
    <li><a href="#consumo-por-tipo-de-carne">Consumo por tipo de carne</a></li>
    <li><a href="#contraste-en-escala-de-consumo-para-todos-los-tipos-de-carne">Contraste en la escala de consumo</a></li>
</ul>
""", unsafe_allow_html=True)

st.title('Análisis exploratorio de datos')
st.markdown("""
En esta sección se muestran los gráficos que se han realizado para el análisis de los datos.
""")
            

# SIDEBAR: FILTRO POR TIPO DE CARNE #
tipos = {'Carne de ternera': 'BEEF', 'Carne de cerdo': 'PIG',
         'Carne de pollo (aves)': 'POULTRY', 'Carne de oveja': 'SHEEP'}

lista_paises = sorted(list(paises.values()))

df = load_data()
df = prepare_data(df)


# GRAFICO DE DISTRIBUCION DE CONSUMO POR TIPO DE CARNE GRAFÍCO CAJAS Y BIGOTES#
st.subheader('Distribución de consumo por tipo de carne')
st.markdown('En el siguiente gráfico se muestra la distribución de consumo por tipo de carne a nivel mundial. Se puede observar que el consumo de carne de ternera ha ido disminuyendo con el paso de los años a medida que aumenta el consumo de carne de pollo (aves). El consumo de carne de cordero es el más bajo.')

# SELECTOR DE FECHAS
year_to_filter = st.slider('Seleccionar año', 1993, 2028, 2023)
grafico3 = plot_dispersion(df, year_to_filter)

with st.spinner('Cargando gráfico...'):
    st.pyplot(grafico3)

# TOP 10 PAÍSES CONSUMIDORES #
st.subheader('Top 10 países consumidores')
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

# GRAFICO DE LOS 10 MAYORES CONSUMIDORES BARRAS HORIZONTALES #
top10 = plot_top_consumers(df, year=year_to_filter, subject=meat)
with st.spinner('Cargtando gráfico...'):
    df_year = select_year(df, year_to_filter)
    st.pyplot(top10)
    st.markdown('''En el gráfico anterior se muestran los 10 países que más carne consumen en el año seleccionado. El consumo se muestra en toneladas.
    ''')


# CONSUMO POR TIPO DE CARNE LINEAS Y BARRAS #

st.subheader('Consumo por tipo de carne')
select = st.selectbox('Seleccionar país', lista_paises,
                      index=lista_paises.index('European Union'))

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Todos", "Ternera", "Cerdo", "Aves", "Cordero"])


with tab1:
    if select == 'European Union':
        year = 2000
    else:
        year = 1993
    st.subheader(f'Consumo de carne en {str(select)} ({year}-2028)')
    grafico2 = plot_consumption_all(df, country=select)
    st.pyplot(grafico2)


with tab2:
   st.subheader("Ternera")
   grafico_ternera = plot_meat_subject(df, country=select, subject='BEEF')
   st.pyplot(grafico_ternera)

with tab3:
   st.subheader("Cerdo")
   grafico_cerdo = plot_meat_subject(df, country=select, subject='PIG')
   st.pyplot(grafico_cerdo)

with tab4:
   st.subheader("Aves")
   grafico_aves = plot_meat_subject(df, country=select, subject='POULTRY')
   st.pyplot(grafico_aves)

with tab5:
    st.subheader("Cordero")
    grafico_cordero = plot_meat_subject(df, country=select, subject='SHEEP')
    st.pyplot(grafico_cordero)

#                                                                                                                                    
st.subheader("Contraste en escala de consumo para todos los tipos de carne")
grafico = plot_meat_consumption(country=select)
with st.spinner('Cargando gráfico...'):
    st.pyplot(grafico)
    st.markdown('En el gráfico anterior, la línea representa el consumo per cápita de carne en kg, mientras que las barras representan el consumo total de carne en Kg per cápita.')


