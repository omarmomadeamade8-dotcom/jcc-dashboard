# =========================================================================
# FUNÇÕES DE ENGENHARIA (No Topo)
# =========================================================================
import streamlit as st
import pandas as pd
import numpy as np 
import datetime

def verificar_alerta_custo(linha, LIMITE_ALERTA_MT=100000.00):
    """
    Cria um status de alerta se o Custo_Total de um item for muito alto.
    """
    if 'Custo_Total' in linha and pd.notna(linha['Custo_Total']):
        if linha['Custo_Total'] > LIMITE_ALERTA_MT:
            return 'ALERTA DE CUSTO ELEVADO'
        elif linha['Custo_Total'] <= 0:
            return 'DADO INVÁLIDO / CUSTO ZERO'
    return 'Custo OK'

# =========================================================================
# 0. INICIALIZAÇÃO DA SESSÃO (Streamlit Session State)
# =========================================================================
# Se as variáveis de estado não existirem, inicialize-as.
if 'status_calculo' not in st.session_state:
    st.session_state['status_calculo'] = "PENDENTE"
if 'Custo_Geral' not in st.session_state:
    st.session_state['Custo_Geral'] = 0.0
if 'Itens_Unicos' not in st.session_state:
    st.session_state['Itens_Unicos'] = 0
if 'df_alertas' not in st.session_state:
    st.session_state['df_alertas'] = pd.DataFrame()
if 'st_descritiva' not in st.session_state:
    st.session_state['st_descritiva'] = pd.DataFrame()
    

# =========================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E TÍTULOS
# =========================================================================
st.set_page_config(
    page_title="JCC - JURIDIO CHICALA CONSTRUÇÕES, E.I.",
    layout="wide"
)

st.title("🚧 JCC - Dashboard de Fiscalização de Obras 📊")
st.markdown("### JURIDIO CHICALA CONSTRUÇÕES, E.I.") 
st.markdown("---")


# =CHECHOUT
# 2. CARREGADOR DE FICHEIROS (INPUT PRINCIPAL)
# =========================================================================
st.header("Upload da Planilha de Orçamento/BOQ")
uploaded_file = st.file_uploader("Carregar Ficheiro Excel (.xlsx) ou CSV", type=['xlsx', 'csv'])

# =========================================================================
# 3. LÓGICA DE PROCESSAMENTO (SÓ EXECUTA SE HOUVER FICHEIRO)
# =========================================================================
if uploaded_file is not None:
    
    try:
        # Tenta ler o ficheiro
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            # CORREÇÃO CRUCIAL: 'header=2' para ler o cabeçalho na Linha 3
            df = pd.read_excel(uploaded_file, header=2)
            
        
        # 1. LIMPEZA AGRESSIVA DOS NOMES DAS COLUNAS
        df.columns = df.columns.astype(str).str.strip().str.replace('\n', ' ').str.replace('\r', ' ', regex=False)
        
        # Nomes de colunas da sua planilha:
        COL_ITEM = 'Item'
        COL_QUANTIDADE = 'Quant'
        COL_PRECO = 'Preco Unit (Mt)'
        
        # 2. TRATAMENTO DE LINHAS VAZIAS/RODAPÉS
        df.dropna(how='all', inplace=True)
            
        st.success("Planilha carregada com sucesso! Pronto para análise.")
        
        # 4. EXIBIR DADOS INICIAIS
        st.header("Análise Rápida - Primeiras Linhas")
        st.dataframe(df.head(20)) 
        st.info(f"O seu ficheiro contém {len(df)} itens/linhas.")

        # =========================================================================
        # INÍCIO DOS CÁLCULOS E GRÁFICOS
        # =========================================================================
        if COL_PRECO in df.columns and COL_QUANTIDADE in df.columns:
            
            # Limpeza e conversão de dados para cálculo
            for col in [COL_PRECO, COL_QUANTIDADE]:
                df[col] = df[col].astype(str).str.replace(' ', '').str.replace(',', '.', regex=False)
                df[col] = pd.to_numeric(df[col], errors='coerce')

            df['Custo_Total'] = df[COL_QUANTIDADE] * df[COL_PRECO]
            df.dropna(subset=['Custo_Total'], inplace=True) 

            # Armazenamento das variáveis na sessão (SUBSTITUIU O 'GLOBAL')
            st.session_state['Custo_Geral'] = df['Custo_Total'].sum()
            st.session_state['Itens_Unicos'] = len(df)
            st.session_state['status_calculo'] = "SUCESSO"

            # =========================================================================
            # SEÇÃO A: CÁLCULO DE CUSTO TOTAL E MÉTRICAS
            # =========================================================================
            st.header("1. Resumo do Orçamento Geral")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total de Itens de BOQ", f"{st.session_state['Itens_Unicos']} itens")
            
            with col2:
                st.metric("Custo Total do Projeto", f"MT {st.session_state['Custo_Geral']:,.2f}")
            
            with col3:
                st.metric("Média por Item", f"MT {st.session_state['Custo_Geral'] / st.session_state['Itens_Unicos']:,.2f}")
            
            st.markdown("---")

            # =========================================================================
            # SEÇÃO B: FISCALIZAÇÃO AUTOMÁTICA
            # =========================================================================
            st.header("2. Relatório de Alertas de Custo (Não Conformidade)")
            
            df['Status_Fiscalizacao'] = df.apply(verificar_alerta_custo, axis=1)
            st.session_state['df_alertas'] = df[df['Status_Fiscalizacao'] == 'ALERTA DE CUSTO ELEVADO']
            
            if not st.session_state['df_alertas'].empty:
                st.error(f"⚠️ {len(st.session_state['df_alertas'])} itens excederam o limite de custo (MT 100,000.00). Atenção!")
                st.dataframe(st.session_state['df_alertas'])
            else:
                st.success("✅ Nenhuma não conformidade grave de custo detetada. Custos sob controle.")

            st.markdown("---")
            
            # =========================================================================
            # SEÇÃO C: ESTATÍSTICA DESCRITIVA AVANÇADA E VISUALIZAÇÃO
            # =========================================================================
            st.header("3. Distribuição Estatística dos Custos")
            
            if len(df) > 1: 
                st.session_state['st_descritiva'] = df['Custo_Total'].describe().to_frame()
                
                col_stat1, col_stat2 = st.columns([1, 2])
                
                with col_stat1:
                    st.subheader("Métricas de Dispersão")
                    st.dataframe(st.session_state['st_descritiva'])

                with col_stat2:
                    st.subheader("Visualização dos 20 Maiores Custos")
                    df_top20 = df.sort_values(by='Custo_Total', ascending=False).head(20)
                    st.bar_chart(df_top20, y='Custo_Total', x=COL_ITEM)
            else:
                 st.info("Não há dados suficientes (menos de 2 itens) para fazer uma análise estatística.")
            
            st.markdown("---")


        else:
            # DIAGNÓSTICO DE COLUNAS (Mostra o que falhou)
            st.warning(f"As colunas de cálculo ('{COL_QUANTIDADE}' ou '{COL_PRECO}') não foram encontradas.")
            st.markdown("---")
            st.subheader("🛠️ DIAGNÓSTICO DE COLUNAS DETECTADAS")
            st.code(f"Nomes de coluna detectados: {list(df.columns)}") 
            st.session_state['status_calculo'] = "FALHOU"
            st.markdown("---")
            

    except Exception as e:
        # Erro geral de processamento
        st.error(f"Erro catastrófico ao processar os dados. Erro: {e}")
        st.session_state['status_calculo'] = "ERRO"


# =========================================================================
# 5. FORMULÁRIO E RELATÓRIO FINAL (NA BARRA LATERAL)
# =========================================================================
with st.sidebar:
    st.header("✉️ Enviar Relatório")
    st.markdown("Preencha para gerar o relatório final.")
    
    # O formulário armazena os valores
    with st.form(key='email_form'):
        nome = st.text_input("Seu Nome")
        email = st.text_input("Seu Email")
        observacoes = st.text_area("Notas/Observações")
        
        # O botão do formulário deve ter submit_button
        submit_button = st.form_submit_button(label='Gerar Relatório Resumido')
        
    # A GERAÇÃO DO RELATÓRIO OCORRE APÓS O BOTÃO SER CLICADO
    if submit_button:
        if st.session_state['status_calculo'] == "SUCESSO":
            st.success("Dados de contacto recolhidos! O relatório foi gerado abaixo.")
            
            # =========================================================================
            # SEÇÃO 4: RELATÓRIO FINAL PARA ENVIO
            # =========================================================================
            st.markdown("---")
            st.header("4. Relatório Final de Engenharia")
            st.info("Para enviar, imprima esta página (Ctrl+P) ou salve como PDF.")
            
            # Variáveis da sessão
            custo_geral = st.session_state['Custo_Geral']
            itens_unicos = st.session_state['Itens_Unicos']
            df_alertas = st.session_state['df_alertas']
            st_descritiva = st.session_state['st_descritiva']

            relatorio_texto = f"""
**RELATÓRIO DE ENGENHARIA JCC - {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}**
----------------------------------------------------------------------------------
**INFORMAÇÕES DE CONTACTO:**
- Nome: {nome}
- Email: {email}

**1. RESUMO GERAL DO PROJETO:**
- **Custo Total do Projeto:** MT {custo_geral:,.2f}
- **Total de Itens Analisados:** {itens_unicos}
- **Média de Custo por Item:** MT {custo_geral / itens_unicos:,.2f}

**2. FISCALIZAÇÃO DE CUSTO:**
- {len(df_alertas)} Itens excederam o limite de custo (MT 100.000,00).

**3. ESTATÍSTICAS CHAVE (Custo_Total):**
{st_descritiva.transpose().to_markdown(index=False)}

**OBSERVAÇÕES DO ANALISTA:**
{observacoes if observacoes else 'Nenhuma observação fornecida.'}
----------------------------------------------------------------------------------
"""
            st.code(relatorio_texto, language='markdown')
            
        elif st.session_state['status_calculo'] == "PENDENTE":
            st.warning("Carregue e processe primeiro uma planilha.")
        else:
            st.error("Não foi possível gerar o relatório: Falha na leitura ou cálculo dos dados da planilha. Verifique a seção de diagnóstico na página principal.")