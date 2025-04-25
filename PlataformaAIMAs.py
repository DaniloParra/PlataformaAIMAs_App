import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from graficos import plot_nivel, plot_chuva

################################################################################

#Carrega a base dos dados de Fluviometria
df = pd.read_csv("Dados/ANA/EstacoesRN_FluvioPluvio.csv", dtype={'Estacao':'str'})

df['Data'] = pd.to_datetime(df['Data'])


#Tabela de estações
estacoes_df = pd.DataFrame([[ 'Manaus', 'Rio Negro', '14990000', "Fluvio"],
                            [ 'Manaus', 'Rio Negro', '360000', "Pluvio"],
                           [ 'Santa Isabel', 'Rio Negro', "14400000", "Fluvio"],
                           ["São Gabriel da Cachoeira","Rio Negro", "14320001", "Fluvio"],
                           ["Barcelos", "Rio Negro", "14480002", "Fluvio"],
                           ["Cucuí", "Rio Negro", "14110000", "Fluvio"],
                           ["Yauarete", "Uaupés", "14260000", "Fluvio"],
                           ["Querari", "Uaupés","14010000", "Fluvio"],
                           ['Taracuá','Uaupés','14280000','Fluvio'],
                           ['Taracuá', 'Uaupés', '14280001', "Fluvio"],
                           ['Pari Cachoeira','Tiquié','14300000','Fluvio'],
                           ['Pari Cachoeira','Tiquié','8069003','Pluvio'],
                           ['Pirarara Poço','Tiquié','8069004','Pluvio'],
                           ['Cunuri','Tiquié','14310000','Fluvio'],
                           ['Tunui','Içana','8168000','Pluvio'],
                           ['São Joaquim','Içana','14215000','Fluvio'],
                           ['Assunção','Içana','14230000','Fluvio'],
                           ['Assunção','Içana','8167000','Pluvio'],
                            ['Louro Poço','Içana','14220000','Fluvio'],
                           ['Santana','Içana','8167003','Pluvio']
                           ], columns=['Local', 'Rio', 'N°Estação', 'Tipo'])


#Título
st.title('Dados hidrológico')

#Subtítulo
st.header('Agência Nacional das Águas (ANA)')

#Subtítulo 2
st.subheader('Lista de estações')

#Mostra a tabela das estações
st.table(estacoes_df[['N°Estação','Rio','Local',
                      'Tipo']].set_index('N°Estação'))

#Define 2 colunas para a seleção dos parâmetros do gráfico
colA1, colA2 = st.columns(2)


with colA1:
    #Coluna da Região
    regiao_selected = st.selectbox("Selecione a região",
                                   pd.unique(estacoes_df["Rio"]))

    #Define a máscara da região
    regiao_mask = estacoes_df['Rio'] == regiao_selected
    
with colA2:
    estacao_selected = st.selectbox("Selecione as estações que deseja plotar",
                                    pd.unique(estacoes_df.loc[regiao_mask]['N°Estação']))


#Define a mascara das estacões no dataframe mãe
estacao_mask = df['Estacao'] == estacao_selected

local_estacao = estacoes_df.loc[estacoes_df["N°Estação"] == estacao_selected]["Local"]

##### Define uma segunda linha de caixas de seleção
colB1, colB2 = st.columns(2)

#### Remove valores nulos

#Filtra nas caixa de seleção as datas mínimas e máximas da estação selecionada
with colB1:
    data_inicio_selected = st.date_input("Selecione a data inicial",
                                         min_value = df[estacao_mask]['Data'].min(),
                                         max_value = df[estacao_mask]['Data'].max(),
                                         value=df[estacao_mask]['Data'].min())
    #Convert Date para Datetime
    data_inicio_selected = pd.to_datetime(data_inicio_selected)
    
with colB2:
    data_fim_selected = st.date_input("Selecione a data final",
                                      min_value = df[estacao_mask]['Data'].min(),
                                      max_value = df[estacao_mask]['Data'].max(),
                                      value = df[estacao_mask]['Data'].max())
    #Convert Date para Datetime
    data_fim_selected = pd.to_datetime(data_fim_selected)

#Define as máscaras no dataframe mãe
date_st_mask = df['Data'] >= data_inicio_selected
date_end_mask =df['Data'] <= data_fim_selected 

#Define um dataframe temporário para o Download dos dados
tmp_df = df.loc[estacao_mask & date_st_mask & date_end_mask]
download_file = tmp_df.to_csv(index=False)

##### GRÁFICO
colC1, colC2 = st.columns(2)
with colC1:
    graph_bt = st.button('Gerar Gráfico')
    fig, ax = plt.subplots()
    
if graph_bt:
    # Cria uma coluna com a data correta e dropa os dias errados 
    tmp_df["Data"] = pd.to_datetime(tmp_df[["Year", "Month", "Day"]], errors='coerce')
    tmp_df["Data"] = tmp_df["Data"].dt.date
    tmp_df['Cotas'] = tmp_df['Cotas'].str.replace(",", ".").astype(float)
    #tmp_df['Cotas'] = pd.to_numeric(df['Cotas'], errors='coerce')

    if estacao_selected not in(['8069003', '8069004', '8168000', '8167000','360000', '8167003']):
        fig = plot_nivel(tmp_df.query("NivelConsistencia == 1").sort_values("Data"),
                         local_estacao.item())
        st.pyplot(fig)
        st.write(estacao_selected)
    else:
        fig = plot_chuva(tmp_df.query("NivelConsistencia == 1").sort_values("Data"), local_estacao.item())
        st.pyplot(fig)
        #st.write(tmp_df['Cotas'])
        
with colC2:
    export_bt = st.download_button('Exportar_dado', download_file, 'Dados_fluvio.csv')





# #st.write(subset)
# # st.plotly_chart()

