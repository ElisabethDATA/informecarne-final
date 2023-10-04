import streamlit as st

st.set_page_config(
    page_title="Agradecimientos",
    page_icon="📈",
)

st.title('Agradecimientos')

st.subheader('Profesores')

st.markdown("""
- [Demetrio Esteban Alférez](#) por su dedicación y por compartir sus conocimientos.
- [Andrés Mateo Piñol](#) por su dedicación y por compartir sus conocimientos.
- PATATA
""")

st.subheader('Familia')

st.markdown("""
- [Ana Pérez Bono](#).
- [Borja Ramos](#).
- [Cristian Valencia](#).
- [Elisabeth Pérez](#).
- [Enrique Vasallo](#).
- [Jordi Roig de la Rosa](#).
- [Guillermo Naveros](#).
- [Marco Antonio García](#).
- [Pilar Castellano Carreras](#).
- [Pedro Llamas López](#).
- [Chati](#).

""")

st.subheader('Recursos')


st.markdown("""
- [Streamlit](https://streamlit.io/) por hacer que sea tan fácil crear aplicaciones web con Python.
- [Kaggle](https://www.kaggle.com/datasets/allenkong/worldwide-meat-consumption) por proporcionar los datos utilizados en este proyecto.
- [Nileg Production](https://www.youtube.com/watch?v=RjiqbTLW9_E&list=PLa6CNrvKM5QU7AjAS90zCMIwi9RTFNIIW) por proporcionar un tutorial sobre cómo crear una aplicación web con Streamlit.
""")

st.balloons()