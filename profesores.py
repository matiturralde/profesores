from collections import namedtuple
import altair as alt
import pandas as pd
import numpy as np
import streamlit as st
from io import BytesIO
import base64

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
        df.rename(columns = {' Total': 'total'}, inplace = True)
        df.rename(columns = {'Fecha de pago': 'Fecha_de_pago'}, inplace = True)
        df.rename(columns = {'proveedor': 'profesor'}, inplace = True)
        #df['monto total'] = df['monto total'].fillna(0)
        #df['monto total'] = df['monto total'].str.replace(' ','')
        #df['monto total'] = df['monto total'].str.replace('-','0')
        #df['monto total'] = df['monto total'].str.replace(',','.').astype('float')
        df['total'] = df['total'].fillna(0)
        df['total'] = df['total'].str.replace(' ','')
        df['total'] = df['total'].str.replace('-','0')
        #df['total'] = df['total'].str.replace('.','')
        #df['total'] = df['total'].str.replace(',','.').astype('float')
        df['total'] = df['total'].str.replace(',','').astype('float')
        df['cuit'] = df['cuit'].astype('string')
        df['cbu'] = df['cbu'].astype('string')
        df['email'] = df['email'].astype('string')
        st.write('Monto total:' , "ARS {0:,.2f}".format(df['total'].sum()))
        " "
        " "
        fecha_liquidacion = st.date_input('Fecha de la Liquidación a Pagar (reconocidos, no reconocidos, etc):')
        if fecha_liquidacion is not None:
            df_sum_fecha = df[ (df.Fecha_de_pago == str(fecha_liquidacion)) & (df.Factura != 'PENDIENTE') & (df.cuit != '-') & (df.cbu != "'-") & (df.cbu != "-") ]
            monto_total = "{:,.2f}".format(df_sum_fecha['total'].sum())
            'Monto total a pagar en fecha seleccionada: ARS', monto_total
        " "
        " "
        orden_compra = st.text_input("Insertar último número de orden de pago anterior:", 0)
        # txt base:
        with open('PAP Coderhouse.txt', encoding='latin-1') as f:
            txt = f.readlines()
        
        #Cabecera (fila única 010)

        CUIT = '0030714528749'
        SUCURSAL_CODER = '00170052260100075195'
        FECHA_DE_PAGO = str(fecha_liquidacion)[0:4] + str(fecha_liquidacion)[5:7] + str(fecha_liquidacion)[8:10]
        IMPORTE_RAW = "{:.2f}".format(round(df_sum_fecha['total'].sum(), 2))
        IMPORTE = IMPORTE_RAW.replace('.','')
        CEROS_IMPORTE = str(IMPORTE).zfill(13)
        CANTIDAD = df_sum_fecha.shape[0]
        CEROS_CANTIDAD = str(CANTIDAD).zfill(7)
        NOMBRE_ARCHIVO = 'PAPR' + FECHA_DE_PAGO
        NRO_CONTRATO = '00170052232700000316'

        txt[0] = txt[0][:31] + CEROS_IMPORTE + txt[0][44:]
        txt[0] = txt[0][:44] + 'AB' + txt[0][46:]
        txt[0] = txt[0][:47] + '0' + txt[0][48:]
        txt[0] = txt[0][:49] + FECHA_DE_PAGO + txt[0][57:]
        txt[0] = txt[0][:57] + FECHA_DE_PAGO + txt[0][65:]
        txt[0] = txt[0][:65] + FECHA_DE_PAGO + txt[0][73:]
        txt[0] = txt[0][:73] + SUCURSAL_CODER + txt[0][93:]
        txt[0] = txt[0][:93] + CEROS_CANTIDAD + txt[0][100:]
        txt[0] = txt[0][:112] + NOMBRE_ARCHIVO + txt[0][124:]
        txt[0] = txt[0][:124] + FECHA_DE_PAGO + txt[0][132:]
        txt[0] = txt[0][:132] + NRO_CONTRATO + txt[0][152:]

        liquidacion_profesores = [txt[0]]

        SUCURSAL = '0001'
        pago = 1
        CALLE = 'CALLE FALSA 123'

        #for p in range (0,df_sum_fecha.shape[0]):

        NRO_ORDEN = int(orden_compra)
        
        for p in range (0,df_sum_fecha.shape[0]):

            #datos proveedor:
            CUIT_BENEFICIARIO = '00' + df_sum_fecha['cuit'].iloc[p]
            NRO_PAGO = pago
            NRO_PROVEEDOR = p + 1
            NRO_ORDEN = p + 1
            NOMBRE_ARCHIVO = '   PAPR' + FECHA_DE_PAGO

            # proveedor 020
            CEROS_NRO_PAGO = str(NRO_PAGO).zfill(6)
            CEROS_NRO_PROVEEDOR = str(NRO_PROVEEDOR).zfill(15)
            CEROS_NRO_ORDEN = str(NRO_ORDEN).zfill(8)
            IMPORTE_RAW_PROV = "{:.2f}".format(round(df_sum_fecha['total'].iloc[p].sum(), 2))
            IMPORTE_PROV = IMPORTE_RAW_PROV.replace('.','')
            CEROS_IMPORTE_PROV = str(IMPORTE_PROV).zfill(13)
            CUIT_PROV = str(df_sum_fecha['cuit'].iloc[p])
            CEROS = str(0).zfill(15)
            NOMBRE_PROVEEDOR = (df_sum_fecha['profesor'].iloc[p]).upper()
            NOMBRE_PROVEEDOR = str(NOMBRE_PROVEEDOR).replace('I\xad','I')
            CEROS_NOMBRE_PROVEEDOR = str(NOMBRE_PROVEEDOR).ljust(40)
            CBU = (df_sum_fecha['cbu'].iloc[p]).replace("'","")
            CHECKBBVA = ''
            if CBU[:3] == '017':
                CHECKBBVA = ' '
            else:
                CHECKBBVA = 'S'
            CALLE_PROV = str(CALLE).ljust(24)
            EMAIL = (df_sum_fecha['email'].iloc[p][:40])
            EMAIL_PROV = str(EMAIL).ljust(40)
            txt[1] = txt[1][:11] + CUIT + txt[1][24:]
            txt[1] = txt[1][:24] + CEROS_NRO_PAGO + txt[1][30:]
            txt[1] = txt[1][:30] + CEROS_NRO_PROVEEDOR + txt[1][45:]
            txt[1] = txt[1][:45] + CEROS_NRO_ORDEN + txt[1][53:]
            txt[1] = txt[1][:53] + CEROS_IMPORTE_PROV + txt[1][66:]
            txt[1] = txt[1][:167] + NOMBRE_ARCHIVO + txt[1][182:]
            txt[1] = txt[1][:192] + CHECKBBVA + txt[1][193:]
            # ver si tiene sentido dejar el cuit acá, no es campo obligatorio
            txt[1] = txt[1][:193] + CEROS_IMPORTE_PROV + txt[1][206:]
            # no siempre es CUIL, a veces CUIT
            ES_CUIL = (df_sum_fecha['cuit'].iloc[p])
            CHECK_CUIL = ''
            if ES_CUIL[:1] == '2':
                CHECK_CUIL = 'CUL'
            else:
                CHECK_CUIL = 'CUI'
            txt[1] = txt[1][:246] + CHECK_CUIL + txt[1][249:]
            txt[1] = txt[1][:249] + CUIT_PROV + txt[1][260:]
            txt[1] = txt[1][:260] + SUCURSAL + txt[1][264:]
            txt[1] = txt[1][:264] + '00000000' + txt[1][272:]
            txt[1] = txt[1][:272] + '00000000' + txt[1][280:]
            txt[1] = txt[1][:280] + '  ' + txt[1][282:]
            pago = pago + 1
            liquidacion_profesores.append(txt[1])
            
            # proveedor 090
            NRO_PAGO = pago
            CEROS_NRO_PAGO = str(NRO_PAGO).zfill(6)
            CEROS_NRO_ORDEN = str(NRO_ORDEN).zfill(8)
            txt[2] = txt[2][:11] + CUIT + txt[2][24:]
            txt[2] = txt[2][:24] + CEROS_NRO_PAGO + txt[2][30:]
            txt[2] = txt[2][:30] + NOMBRE_ARCHIVO + txt[2][45:]
            txt[2] = txt[2][:45] + CEROS_NRO_PROVEEDOR + txt[2][60:]
            txt[2] = txt[2][:61] + CHECK_CUIL + txt[2][64:]
            txt[2] = txt[2][:64] + CUIT_PROV + txt[2][75:]
            txt[2] = txt[2][:75] + CEROS_NOMBRE_PROVEEDOR + txt[2][115:]
            txt[2] = txt[2][:133] + CBU + txt[2][155:]
            txt[2] = txt[2][:166] + CALLE_PROV + txt[2][190:]
            txt[2] = txt[2][:228] + 'C1000' + txt[2][233:]
            txt[2] = txt[2][:233] + '01' + txt[2][235:]
            txt[2] = txt[2][:238] + EMAIL_PROV + txt[2][278:]
            txt[2] = txt[2][:416] + ' '.ljust(100) + txt[2][516:]
            txt[2] = txt[2][:444] + '00000000' + txt[2][452:]
            txt[2] = txt[2][:480] + '00000000' + txt[2][488:]
            txt[2] = txt[2][:516] + '00000000' + txt[2][524:]
            txt[2] = txt[2][:624] + CEROS_NRO_ORDEN + txt[2][632:]
            pago = pago + 1
            liquidacion_profesores.append(txt[2])

        CANTIDAD_TOTAL = CANTIDAD * 2 + 2
        CEROS_CANTIDAD_TOTAL = str(CANTIDAD_TOTAL).zfill(10)
        NRO_PAGO = pago
        CEROS_NRO_PAGO = str(NRO_PAGO).zfill(6)

        txt[7] = txt[7][:24] + CEROS_NRO_PAGO + txt[7][30:]
        txt[7] = txt[7][:30] + CEROS_IMPORTE + txt[7][43:]
        txt[7] = txt[7][:43] + CEROS_CANTIDAD + txt[7][50:]
        txt[7] = txt[7][:50] + CEROS_CANTIDAD_TOTAL + txt[7][60:]
        liquidacion_profesores.append(txt[7])
        NOMBRE_ARCHIVO = 'PAPR' + FECHA_DE_PAGO
        " "
        " "
        submit_button = st.button(label='Exportar .txt para BBVA')
        if submit_button:
            #bajar = np.savetxt(NOMBRE_ARCHIVO+ '.txt', liquidacion_profesores, fmt='%s',delimiter=' ', newline='', header='', footer='', comments='# ', encoding=None)
            reference = NOMBRE_ARCHIVO
            to_save = liquidacion_profesores
            href = f'<a href="data:text/plain;charset=UTF-8,{to_save}" download="{reference}.txt">Click para bajar archivo</a> ({reference}.txt)'
            st.markdown(href, unsafe_allow_html=True)






        " "
        " "
        error_fila = st.text_input("Insertar número de fila con error en BBVA:", 0)
        error_fila = int(error_fila)-1
        'CUIT: ' + liquidacion_profesores[error_fila][64:75]
        'PROVEEDOR: ' + liquidacion_profesores[error_fila][75:115]
        'CBU: ' + liquidacion_profesores[error_fila][133:155]
        'mail: ' + liquidacion_profesores[error_fila][238:278]

