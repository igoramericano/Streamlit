import streamlit as st
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime, timedelta
import logging

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)

st.set_page_config(
    page_title="App Preço de Ações Alpha Vantage",
    layout="wide",
)

# ---------------------------------------------------------------------
# LISTA DE EMPRESAS GLOBAIS
# ---------------------------------------------------------------------
EMPRESAS_DISPONIVEIS = {
    "Alphabet Inc. (GOOG)": "GOOG",
    "Microsoft (MSFT)": "MSFT",
    "Apple (AAPL)": "AAPL",
    "Amazon (AMZN)": "AMZN",
    "Tesla (TSLA)": "TSLA",
}

# ---------------------------------------------------------------------
# CONFIGURAÇÃO E ESTADO
# ---------------------------------------------------------------------

# A chave fornecida pelo usuário (d6e5895c99ba4a4ab3a74e31781c5ddf) está aqui
# como valor inicial. O campo é do tipo 'password' por segurança.
ALPHA_VANTAGE_API_KEY = st.text_input(
    "🔑 Cole sua Chave de API da Alpha Vantage:",
    value="d6e5895c99ba4a4ab3a74e31781c5ddf", 
    type="password"
)

# Inicialização do estado da sessão: lista de tickers selecionados
if 'selected_tickers' not in st.session_state:
    st.session_state.selected_tickers = ["GOOG", "MSFT"]

# ---------------------------------------------------------------------
# FUNÇÃO DE CALLBACK PARA TOGGLE (Alternar)
# ---------------------------------------------------------------------
def toggle_ticker(ticker):
    current_list = st.session_state.selected_tickers
    
    if ticker in current_list:
        # Se o ticker estiver na lista, remova, mas EVITE UMA LISTA VAZIA
        if len(current_list) > 1:
            current_list.remove(ticker)
    else:
        # Se o ticker não estiver na lista, adicione
        current_list.append(ticker)
    
    st.session_state.selected_tickers = current_list
    st.rerun() # Força o Streamlit a recarregar


# ---------------------------------------------------------------------
# FUNÇÃO DE CARREGAMENTO DE DADOS COM CACHE
# ---------------------------------------------------------------------

# Cache por 1 dia (86400 segundos)
@st.cache_data(ttl=86400) 
def carregar_dados(tickers_list, api_key):
    """
    Carrega os dados históricos para uma lista de tickers usando Alpha Vantage.
    Retorna apenas os preços de fechamento ajustado.
    """
    if not api_key:
        return pd.DataFrame()
        
    logging.info(f"Tentando carregar dados para: {tickers_list}")
    
    data_fim = datetime.now()
    data_inicio = data_fim - timedelta(days=366) 
    
    dados_combinados = pd.DataFrame()
    
    try:
        ts = TimeSeries(key=api_key, output_format='pandas')
        
        for ticker in tickers_list:
            # Alpha Vantage retorna a série completa, não apenas o período
            data, meta_data = ts.get_daily_adjusted(symbol=ticker, outputsize='full')
            
            # 1. Limpeza e Seleção da Coluna
            # A coluna de fechamento ajustado na Alpha Vantage é geralmente '5. adjusted close'
            data_fechamento = data['5. adjusted close'].rename(ticker)
            
            # 2. Inverte o Index (Alpha Vantage retorna o mais novo primeiro)
            data_fechamento = data_fechamento.iloc[::-1]
            
            # 3. Filtra pelo período de 1 ano
            data_fechamento = data_fechamento[(data_fechamento.index >= data_inicio.strftime('%Y-%m-%d')) & 
                                              (data_fechamento.index <= data_fim.strftime('%Y-%m-%d'))]
            
            # 4. Combina os dados
            if dados_combinados.empty:
                dados_combinados = data_fechamento.to_frame()
            else:
                dados_combinados = dados_combinados.join(data_fechamento, how='outer')

        if dados_combinados.empty:
            logging.warning(f"O DataFrame retornado para {tickers_list} está vazio.")
            return pd.DataFrame() 

        dados_combinados.index.name = "Data"
        logging.info(f"Dados carregados com sucesso para {tickers_list}. Total de {len(dados_combinados)} linhas.")
        return dados_combinados.copy()
        
    except Exception as e:
        # Captura erros de API key inválida, Rate Limit (sim, Alpha Vantage tem limites)
        logging.error(f"Falha grave ao carregar dados da Alpha Vantage: {e}")
        return pd.DataFrame()


# ---------------------------------------------------------------------
# EXECUÇÃO E LAYOUT DO APP
# ---------------------------------------------------------------------

if not ALPHA_VANTAGE_API_KEY:
    st.warning("⚠️ Por favor, insira sua chave de API da Alpha Vantage acima para continuar.")
else:
    st.title("📈 App Preço de Ações Alpha Vantage")

    st.markdown("### Selecione os Ativos para Visualizar (Último Ano)")

    # --- Botões Lado a Lado (Multi-Select Simulada) ---

    tickers_list_all = list(EMPRESAS_DISPONIVEIS.values())
    cols = st.columns(len(tickers_list_all))

    for i, (full_name, ticker) in enumerate(EMPRESAS_DISPONIVEIS.items()):
        button_label = ticker
        
        is_selected = ticker in st.session_state.selected_tickers
        
        display_label = f"✔️ {button_label}" if is_selected else button_label

        # Tenta aplicar estilo CSS para o botão selecionado
        button_style = ""
        if is_selected:
            button_style = f"""
                <style>
                div[data-testid*="stHorizontalBlock"] > div:nth-child({i + 1}) button {{
                    background-color: #264b9b;
                    color: white;
                    border-color: #264b9b;
                }}
                </style>
            """
            st.markdown(button_style, unsafe_allow_html=True)
        
        
        with cols[i]:
            if st.button(
                display_label, 
                key=f"btn_{ticker}", 
                use_container_width=True,
                on_click=toggle_ticker,
                args=(ticker,)
            ):
                pass 


    # Define a lista de Tickers para o carregamento de dados
    TICKERS_SELECIONADOS = st.session_state.selected_tickers

    # Carrega os dados para os tickers selecionados
    DADOS_PLOTAGEM = carregar_dados(TICKERS_SELECIONADOS, ALPHA_VANTAGE_API_KEY)


    st.markdown("---")


    if TICKERS_SELECIONADOS and ALPHA_VANTAGE_API_KEY:
        st.markdown(f"**Visualizando:** {', '.join(TICKERS_SELECIONADOS)}")
        
        if not DADOS_PLOTAGEM.empty:
            
            st.subheader("Evolução do Preço de Fechamento Ajustado")
            
            st.line_chart(DADOS_PLOTAGEM) 
            
            st.markdown("---")
            
            st.subheader("Dados Históricos (Amostra do Fechamento Ajustado)")
            
            st.dataframe(DADOS_PLOTAGEM.tail(10)) 
            
        else:
            st.error("❌ Erro ao carregar dados históricos das ações.")
            st.warning(f"Não foi possível obter dados para os tickers selecionados: **{', '.join(TICKERS_SELECIONADOS)}**.")
            st.markdown("""
            ---
            ### O que pode estar causando a falha?
            1.  **API Key Inválida:** Verifique se a chave de API está correta.
            2.  **Limite de Taxa (Rate Limit) da Alpha Vantage:** O limite gratuito é de 5 chamadas por minuto. O `st.cache_data` ajuda, mas se você clicar muito rápido, pode esbarrar nesse limite.
            """)
    else:
        st.info("Por favor, selecione uma ou mais ações para visualizar o gráfico.")

    st.markdown("""
---
# Fim do app
""")