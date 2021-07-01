from collections import namedtuple
import altair as alt
import pandas as pd
import streamlit as st
import io

col1, col2, col3 = st.beta_columns(3)
image = 'https://res.cloudinary.com/hdsqazxtw/image/upload/v1559681445/logo_coderhouse_3_bllxal.png'
col2.image(image)

st.markdown("""
<style>
.big-font {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Liquidación Profesores</p>', unsafe_allow_html=True)

#st.title('Liquidación Profesores:')
#st.text('Cargar archivo de liquidación mensual:')
#st.sidebar

multiple_files = st.file_uploader('Subir csv',type="csv", accept_multiple_files=True)
for file in multiple_files:
	dataframe = pd.read_csv(file)
	file.seek(0)
	st.write(dataframe)
    
st.write("###")