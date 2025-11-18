import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import logging

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)

st.set_page_config(
    page_title="App Preço de Ações Globais",
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
# INICIALIZAÇÃO DO ESTADO DA SESSÃO
# ---------------------------------------------------------------------
# Padrão: Apenas GOOG selecionada
if 'selected_tickers' not in st.session_state:
    st.session_state.selected_tickers = ["GOOG"]

# ---------------------------------------------------------------------
# FUNÇÃO DE CALLBACK PARA TOGGLE (Alternar)
# ---------------------------------------------------------------------
def toggle_ticker(ticker):
    current_list = st.session_state.selected_tickers
    
    if ticker in current_list:
        # Se o ticker estiver na lista, remova, mas EVITE UMA LISTA VAZIA
        if len(current_list) > 1:
            current_list.remove(ticker)
        # Se for o último, mantém para evitar erro no download
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
def carregar_dados(tickers_list):
    """
    Carrega os dados históricos para uma lista de tickers, retorna apenas
    os preços de fechamento ajustado (Close), prontos para o gráfico.
    """
    if not tickers_list:
        return pd.DataFrame()
        
    logging.info(f"Tentando carregar dados para: {tickers_list}")
    
    data_fim = datetime.now()
    data_inicio = data_fim - timedelta(days=366) 
    
    start_date = data_inicio.strftime("%Y-%m-%d")
    end_date = data_fim.strftime("%Y-%m-%d")
    
    try:
        cotacoes_acao = yf.download(
            tickers_list, 
            start=start_date, 
            end=end_date, 
            progress=False,
            auto_adjust=True 
        )
        
        if cotacoes_acao.empty:
             logging.warning(f"O DataFrame retornado para {tickers_list} está vazio.")
             return pd.DataFrame()
        
        # --- Processamento do DataFrame MultiIndex / SingleIndex ---
        
        if len(tickers_list) > 1 and isinstance(cotacoes_acao.columns, pd.MultiIndex):
            # Múltiplos Tickers: Filtra 'Close' e achata colunas
            dados_para_plotar = cotacoes_acao.loc[:, pd.IndexSlice[:, 'Close']]
            dados_para_plotar.columns = dados_para_plotar.columns.get_level_values(1)
        
        elif len(tickers_list) == 1 and 'Close' in cotacoes_acao.columns:
            # Um único Ticker: Seleciona 'Close' e renomeia
            dados_para_plotar = cotacoes_acao[['Close']].copy()
            dados_para_plotar.rename(columns={'Close': tickers_list[0]}, inplace=True)
        
        else:
            logging.warning(f"O DataFrame retornado para {tickers_list} está malformado após o download.")
            return pd.DataFrame()
        
        dados_para_plotar.index.name = "Data"
        logging.info(f"Dados carregados com sucesso para {tickers_list}. Colunas: {list(dados_para_plotar.columns)}")
        return dados_para_plotar
        
    except Exception as e:
        # Captura erros gerais de download, como falhas de conexão
        logging.error(f"Falha grave ao carregar dados durante o download: {e}")
        return pd.DataFrame()


# ---------------------------------------------------------------------
# EXECUÇÃO E LAYOUT DO APP
# ---------------------------------------------------------------------

st.title("📈 App Preço de Ações Globais")

st.markdown("### Selecione os Ativos para Visualizar (Último Ano)")

# --- Botões Lado a Lado (Multi-Select Simulada) ---

tickers_list = list(EMPRESAS_DISPONIVEIS.values())
cols = st.columns(len(tickers_list))

# Itera sobre as empresas e cria um botão em cada coluna
for i, (full_name, ticker) in enumerate(EMPRESAS_DISPONIVEIS.items()):
    button_label = ticker.replace(".SA", "")
    
    is_selected = ticker in st.session_state.selected_tickers
    
    # Adiciona um indicador visual e estilo
    display_label = f"✔️ {button_label}" if is_selected else button_label

    # Adiciona estilo CSS para mudar a cor do botão selecionado
    # Este é um truque para mudar a cor do botão selecionado no Streamlit.
    button_style = ""
    if is_selected:
        # A sintaxe CSS abaixo tenta selecionar o botão certo na coluna.
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
            pass # A lógica está toda no on_click e no callback


# Define a lista de Tickers para o carregamento de dados
TICKERS_SELECIONADOS = st.session_state.selected_tickers

# Carrega os dados para os tickers selecionados
DADOS_PLOTAGEM = carregar_dados(TICKERS_SELECIONADOS)


st.markdown("---")


if TICKERS_SELECIONADOS:
    st.markdown(f"**Visualizando:** {', '.join(TICKERS_SELECIONADOS)}")
    
    if not DADOS_PLOTAGEM.empty:
        
        st.subheader("Evolução do Preço de Fechamento Ajustado")
        
        # st.line_chart plota múltiplas colunas automaticamente
        st.line_chart(DADOS_PLOTAGEM) 
        
        st.markdown("---")
        
        st.subheader("Dados Históricos (Amostra do Fechamento Ajustado)")
        
        # Exibe os dados de fechamento ajustado para as ações selecionadas
        st.dataframe(DADOS_PLOTAGEM.tail(10)) 
        
    else:
        # Mensagem de erro robusta
        st.error("❌ Erro ao carregar dados históricos das ações.")
        st.warning(f"Não foi possível obter dados para os tickers selecionados: **{', '.join(TICKERS_SELECIONADOS)}**.")
        st.markdown("""
        ---
        ### O que pode estar causando a falha?
        1.  **Bloqueio de API/Rate Limit:** Se você viu `YFRateLimitError` no terminal, o acesso à API do Yahoo Finance está temporariamente bloqueado. **Solução: Espere 10-15 minutos e tente novamente.**
        2.  **Conexão de Rede:** Verifique sua conexão.
        """)
else:
    st.info("Por favor, selecione uma ou mais ações para visualizar o gráfico.")

st.markdown("""
---
# Fim do app
""")