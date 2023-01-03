import pdfplumber
import pandas as pd
import plotly.express  as plt
import streamlit as st
import streamlit.components.v1 as components

dados = ''
cab = ''
lista = []
lista_kr = []
lista_cab = []
pegar_comp = []
lista_comp = []
lista_valor = []
lista_result = []
comp = ''
ME = False


st.set_page_config(page_title="Dashboard")
st.markdown("<h1 style='text-align: center;'>Simples Nacional</h1>", unsafe_allow_html=True)
st.write()
st.write()

uploaded_file = st.file_uploader("Choose your .pdf file", type="pdf")
if uploaded_file is not None:
    with pdfplumber.open(uploaded_file) as pdf:           
    
        for i, paginas in enumerate(pdf.pages):
            lista.append(paginas.extract_text().split('\n'))
        
            for x in range(0, len(lista[i])):
                if lista[i][x][0:12] == 'CNPJ Básico:':
                    dados = dados + '|' + lista[i][x].strip().split(':')[2]
                
                if lista[i][x].find('(PA):') != -1:
                    dados = dados + '|' + lista[i][x].strip().replace('Período de Apuração (PA): ','') 
                    
                if lista[i][x].find('(RBT12)') != -1:
                    dados = dados + '|' + lista[i][x-1].strip().split(' ')[2]
                        
                if lista[i][x][2:3] == "/":
                    if ME == False:
                        pegar_comp.append(lista[i][x].strip().split(' '))
                        
                if lista[i][x][0:5] == '2.2.2':
                    ME = True
                # if  (lista[i][x][0:24] == 'Receita Bruta Informada:') or (lista[i][x][0:16] == 'Valor Informado:'):
                #     dados = dados + '|' + lista[i][x].strip().split(':')[1]                    
                #     lista_cab.append((lista[i][x+2].strip().split(' ')))
                #     break
        
                if  (lista[i][x][0:31] == 'Informações por Estabelecimento') or (lista[i][x][0:25] == 'Totais do Estabelecimento'):
                    dados = dados + '|' + lista[i][x+1].strip().split(':')[1]                    
                    lista_cab.append((lista[i][x+4].strip().split(' ')))
                    break    
        dados = dados + '|'
        # dados = dados.replace('.','')
        # dados = dados.replace(',','.')
        # # dados = dados.replace('R$','')    
        

        
        # for y in lista_cab:
        #     cab = cab + '|' + y
        
        # cab = cab.replace('.','')
        # cab = cab.replace(',','.')
        # cab = cab + '|'
        
        for y in range(0, len(pegar_comp)):
            for z, w in enumerate(pegar_comp[y]):
                if (z%2) == 0:
                    lista_comp.append(w)
                if z % 2:
                    w = w.replace('.','')
                    w = w.replace(',','.')
                    lista_valor.append(float(w))

    
    
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown("<h5 style='text-align: left;'>" +dados.split('|')[1] + "</h5>", unsafe_allow_html=True)
        
    with right_column:
        st.markdown("<h3 style='text-align: right;'>" +dados.split('|')[2] + "</h3>", unsafe_allow_html=True)

       
    
    faturamento = {'Competência': lista_comp,
                'Valor': lista_valor}
    
    faturamento_df = pd.DataFrame(faturamento)

    # left_column, right_column = st.columns(2)
    # with left_column:
    fig = plt.line(faturamento_df, x = 'Competência' , y = 'Valor', width=800)
    st.write(fig)
            
    # with right_column:
    fig = plt.bar(faturamento_df, x = 'Competência' , y = 'Valor', width=800)
    st.write(fig)  
    
    lista_cab[0].insert(9,(dados.split('|')[3]))
    lista_cab[0].insert(10,(dados.split('|')[4]))
               


    cabecalho =   {'dados': ['IRPJ', 'CSLL', 'COFINS', 'PIS', 'INSS', 'ICMS', 'IPI', 'ISS', 'TOTAL','Receita Bruta Acumulada', 'Receita Bruta Informada'],
                   'Valores': lista_cab[0]}

    cabecalho_df = pd.DataFrame(cabecalho)
    st.checkbox("Use container width", value=False, key="use_container_width")
    st.dataframe(cabecalho_df.style.hide_index(), use_container_width=st.session_state.use_container_width)