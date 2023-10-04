import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style = 'dark', palette = 'deep')

# CARGA DE DATOS #
dataset = 'data/meat_consumption.csv'



@st.cache_data
def load_data(dataset='data/meat_consumption.csv'):
    df = pd.read_csv(dataset)
    # Transformar los títulos de columnas a mayúsculas.
    df.columns = [column.upper() for column in df.columns]
    return df

data = load_data()

tipos = {'BEEF': 'Ternera', 'PIG': 'Cerdo',
         'POULTRY': 'Pollo (Aves)', 'SHEEP': 'Cordero'}
subjects = data['SUBJECT'].unique()
colors = sns.color_palette('Paired', n_colors=len(subjects)*2+1)
subject_color = {'BEEF': 0, 'PIG': 2, 'POULTRY': 4, 'SHEEP': 6}

# Eliminar columnas innecesarias.
data = data.drop(['INDICATOR', 'FREQUENCY'], axis=1)


@st.cache_data
def split_measure(df):

    # Seleccionar columnas de interés
    df = df[['LOCATION', 'SUBJECT', 'TIME', 'MEASURE', 'VALUE']]

    # Aplicar pivot
    df_pivot = df.pivot(
        index=['LOCATION', 'SUBJECT', 'TIME'], columns='MEASURE', values='VALUE')
    df_pivot = df_pivot.reset_index()
    df_pivot.columns.name = ''
    return df_pivot


@st.cache_data
def replace_country_code(df):
    paises = {
        'AUS': 'Australia',
        'BGD': 'Bangladesh',
        'CAN': 'Canada',
        'JPN': 'Japan',
        'KOR': 'South Korea',
        'MEX': 'Mexico',
        'NZL': 'New Zealand',
        'TUR': 'Turkey',
        'USA': 'United States',
        'ARG': 'Argentina',
        'BRA': 'Brazil',
        'CHL': 'Chile',
        'CHN': 'China',
        'COL': 'Colombia',
        'DZA': 'Argelia',
        'EGY': 'Egypt',
        'ETH': 'Ethiopia',
        'IND': 'India',
        'IDN': 'Indonesia',
        'IRN': 'Iran',
        'ISR': 'Israel',
        'KAZ': 'Kazakhstan',
        'MYS': 'Malaysia',
        'NGA': 'Nigeria',
        'PAK': 'Pakistan',
        'PRY': 'Paraguay',
        'PER': 'Peru',
        'PHL': 'Philippines',
        'RUS': 'Russia',
        'SAU': 'Saudi Arabia',
        'ZAF': 'South Africa',
        'THA': 'Thailand',
        'TZA': 'Tanzania',
        'UKR': 'Ukraine',
        'URY': 'Uruguay',
        'VNM': 'Vietnam',
        'NOR': 'Norway',
        'CHE': 'Switzerland',
        'GBR': 'United Kingdom',
        'GHA': 'Ghana',
        'HTI': 'Haiti',
        'MOZ': 'Mozambique',
        'SDN': 'Sudan',
        'ZMB': 'Zambia',
        'EU27': 'European Union',
        'WLD': 'World'
    }
    df['CODE'] = df['LOCATION']
    df['LOCATION'] = df['LOCATION'].replace(paises)
    df = df.reindex(columns=["CODE", "LOCATION", "SUBJECT", "TIME", "KG_CAP", "THND_TONNE"])
    return df


@st.cache_data
def plot_meat_consumption(df=data, country='World'):
    
    ndf = split_measure(data)
    ndf = replace_country_code(ndf)

    if country == 'European Union':
        ndf = ndf[ndf['TIME'] >= 2000]

    # filtrar los datos por país
    kg_cap = ndf
    thnd_tonne = ndf

    kg_cap_wld = kg_cap[kg_cap['LOCATION'] == country]
    thnd_tonne_wld = thnd_tonne[thnd_tonne['LOCATION'] == country]

    subjects = ndf['SUBJECT'].unique()
    valor_maximo_kg = kg_cap_wld['KG_CAP'].max() + 10
    valor_maximo_thnd = thnd_tonne_wld['THND_TONNE'].max() + 10

    fig = plt.figure(figsize=(12, 8))

    colors = sns.color_palette('Paired', n_colors=len(subjects)*2+1)

    for i, subject in enumerate(subjects):
        row = i // 2
        col = i % 2

        ax = plt.subplot(2, 2, i+1)

        data1 = thnd_tonne_wld[thnd_tonne_wld['SUBJECT'] == subject]
        ax.bar(data1['TIME'], data1['THND_TONNE'], color=colors[i*2])
        ax.set_ylabel("Miles de Toneladas", fontsize=12)

        ax2 = ax.twinx()

        data2 = kg_cap_wld[kg_cap_wld['SUBJECT'] == subject]
        ax2.plot(data2['TIME'], data2['KG_CAP'], color=colors[i*2+1])

        ax2.set_ylabel("Kg per cápita", fontsize=10)

        ax2.set_ylim(bottom=0, top=valor_maximo_kg+10)

        ax.set_title(tipos[subject])
        ax.set_ylim(bottom=0, top=valor_maximo_thnd*1.1)

    plt.tight_layout()

    return fig


@st.cache_data
def plot_consumption_all(df=data, country='World'):

    if country == 'European Union':
        year = 1999
    else:
        year = 1992

    beef = df.loc[(df['SUBJECT'] == 'BEEF') & (
        df['LOCATION'] == country) & (df['TIME'] > year)]
    pig = df.loc[(df['SUBJECT'] == 'PIG') & (
        df['LOCATION'] == country) & (df['TIME'] > year)]
    poultry = df.loc[(df['SUBJECT'] == 'POULTRY') & (
        df['LOCATION'] == country) & (df['TIME'] > year)]
    sheep = df.loc[(df['SUBJECT'] == 'SHEEP') & (
        df['LOCATION'] == country) & (df['TIME'] > year)]

    fig, ax = plt.subplots()

    ax.plot(beef['TIME'], beef['KG_CAP'], linestyle='--', label='Ternera')
    ax.plot(pig['TIME'], pig['KG_CAP'], color='green',
            linestyle='--', label='Cerdo')
    ax.plot(poultry['TIME'], poultry['KG_CAP'],
            color='red', linestyle=':', label='Aves')
    ax.plot(sheep['TIME'], sheep['KG_CAP'],
            color='orange', linestyle='-.', label='Cordero')
    ax.set_ylabel('Kg per cápita')
    ax.set_xlabel('Año')
    ax.legend(loc='upper left')

    return fig

# Grafico por tipo de carne
@st.cache_data
def plot_meat_subject(df=data, subject='BEEF', country='World'):

    if country == 'European Union':
        year = 2000
    else:
        year = 1993

    ndf = split_measure(data)
    ndf = replace_country_code(ndf)

    # filtrar los datos por país
    kg_cap = ndf.loc[ndf['TIME'] > year]
    thnd_tonne = ndf.loc[ndf['TIME'] > year]

    kg_cap_wld = kg_cap.loc[(kg_cap['LOCATION'] == country) & (kg_cap['SUBJECT'] == subject)]
    thnd_tonne_wld = thnd_tonne.loc[(thnd_tonne['LOCATION'] == country) & (thnd_tonne['SUBJECT'] == subject)]
    
    fig, ax = plt.subplots()

    ax.set_ylabel("Miles de Toneladas", fontsize=12)
    ax.bar(thnd_tonne_wld['TIME'], thnd_tonne_wld['THND_TONNE'], color=colors[subject_color[subject]], label='Producción', alpha=0.7)
    
    ax1 = ax.twinx()
    ax1.set_ylabel('Kg per cápita')
    ax1.plot(kg_cap_wld['TIME'], kg_cap_wld['KG_CAP'],
             linestyle='--', label='Consumo Kg/Cap', color=colors[subject_color[subject]+1])
    
    ax.set_title(f'Producción y consumo de {tipos[subject]} en {country} (1993-2025)')
    ax.set_xlabel('Año')
    ax.legend(loc='upper left')
    ax1.legend(loc='upper right')

    # Ajustar límites con margen superior del 10%
    # ax.set_ylim(0, max(thnd_tonne_wld['THND_TONNE'])*1.1)
    ax1.set_ylim(bottom=0, top=kg_cap_wld['KG_CAP'].max()*1.3)

    ax.margins(y=0.1)

    return fig


@st.cache_data
def plot_top_consumers(data, subject='BEEF', year=2018, n=10):
    # Filtrar los datos por año y tipo de carne
    data = data[(data['TIME'] == year) & (data['SUBJECT'] == subject)]

    # Ordenar los países por consumo descendente
    data = data.sort_values('KG_CAP', ascending=False)

    # Tomar los n países con mayor consumo
    data = data.head(n)

    # Crear un gráfico de barras horizontal
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='KG_CAP', y='LOCATION', data=data,
                color=colors[subject_color[subject]])

    # Configurar el título y los ejes
    ax.set_title(f'Mayores consumidores de carne de {tipos[subject]} en {year}')
    ax.set_xlabel('Consumo per cápita (kg)')
    ax.set_ylabel('Países')

    return fig


@st.cache_data
def plot_dispersion(df=data, year=2023):

    # Crear un DataFrame con los datos de interés
    filtered_data = df.loc[df['TIME'] == year]

    # Colores de cajas
    colores = [colors[subject_color[subject]] for subject in filtered_data['SUBJECT']]

    filtered_data.loc[:, 'SUBJECT'] = filtered_data['SUBJECT'].replace(tipos)

    # Crear el gráfico de dispersión
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(data=filtered_data, x="SUBJECT", y="KG_CAP", palette=colores, ax=ax)

    # Configurar los títulos y etiquetas de los ejes
    plt.title(f"Consumo de carne por tipo ({year})")
    plt.xlabel("Tipo de carne")
    plt.ylabel("Kg per cápita)")

    # Mostrar el gráfico
    return fig
