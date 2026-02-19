import streamlit as st
import pandas as pd

# 1. Configuração da página
st.set_page_config(
    page_title="Biblioteca Pessoal",
    layout="wide"
)

# 2. Título do App
st.title("📚 Sistema de Gerenciamento de Biblioteca")

# 3. Inicializar a memória (session_state)
if 'biblioteca' not in st.session_state:
    st.session_state.biblioteca = []

st.subheader("Cadastrar Novo Livro")

# --- Lógica do Gênero (FORA do formulário para atualizar na hora) ---
genero_selecionado = st.selectbox(
    "Gênero", 
    ["Ficção", "Não-ficção", "Romance", "Biografia", "Fantasia", "Outro"]
)

# Variável final que será salva
genero_final = genero_selecionado

if genero_selecionado == "Outro":
    genero_final = st.text_input("Digite o Gênero Personalizado")
# -------------------------------------------------------------------

with st.form("novo_livro"):
    # Campos de texto básicos
    titulo = st.text_input("Título (Obrigatório)")
    autor = st.text_input("Autor (Obrigatório)")
    
    # Colunas para dados numéricos e avaliação
    col1, col2, col3 = st.columns(3)
    with col1:
        ano = st.number_input("Ano de Publicação", step=1, format="%d")
    with col2:
        paginas = st.number_input("Número de Páginas", step=1)
    with col3:
        avaliacao = st.slider("Avaliação (1-5)", 1, 5, 3)
    
    # Status de leitura
    status = st.selectbox("Status de Leitura", ["Não lido", "Lendo", "Concluído"])
    
    observacoes = st.text_area("Observações")

    # Botão para enviar
    enviado = st.form_submit_button("Cadastrar Livro")

    # Lógica de validação e salvamento
    if enviado:
        if not titulo or not autor:
            st.error("Por favor, preencha o Título e o Autor!")
        else:
            # Cria o dicionário do novo livro [cite: 47-58]
            novo_livro = {
                "id": len(st.session_state.biblioteca) + 1, # Gera ID automático [cite: 82]
                "titulo": titulo,
                "autor": autor,
                "ano": ano,
                "genero": genero_final, # Usa o gênero tratado (lista ou texto)
                "paginas": paginas,
                "status": status,
                "avaliacao": avaliacao,
                "observacoes": observacoes
            }
            
            # Adiciona na lista da memória
            st.session_state.biblioteca.append(novo_livro)
            
            st.success("Livro cadastrado com sucesso!")