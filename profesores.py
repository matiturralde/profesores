from collections import namedtuple
import altair as alt
import pandas as pd
import streamlit as st
import io

favicon = 'https://res.cloudinary.com/hdsqazxtw/image/upload/v1559681445/logo_coderhouse_1_rec5vl.png'
st.set_page_config(page_title='Profesores', page_icon = favicon, initial_sidebar_state = 'auto', layout="centered")
# favicon being an object of the same kind as the one you should provide st.image() with (ie. a PIL array for example) or a string (url or local file path)

col1, col2, col3 = st.beta_columns(3)
image = 'https://res.cloudinary.com/hdsqazxtw/image/upload/v1559681445/logo_coderhouse_3_bllxal.png'
col2.image(image)

markdown = st.markdown("""
<style>
.big-font {
    font-size:20px !important;
    text-align: left
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Liquidación Profesores</p>', unsafe_allow_html=True)

#st.title('Liquidación Profesores:')
#st.text('Cargar archivo de liquidación mensual:')
#st.sidebarS

multiple_files = st.file_uploader('Subir csv:',type="csv", accept_multiple_files=True)
if multiple_files is not None:
    for file in multiple_files:
	    df = pd.read_csv(file)
	    st.dataframe(df)
        
if multiple_files is not None:
    for file in multiple_files:
        df['monto total'] = df['monto total'].fillna(0)
        df['monto total'] = df['monto total'].str.replace('-','0')
        df['monto total'] = df['monto total'].str.replace(',','.').astype('float')
        st.write('Monto Total:' , "ARS {0:,.2f}".format(df['monto total'].sum()))