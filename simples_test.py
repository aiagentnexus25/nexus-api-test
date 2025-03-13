import streamlit as st
from openai import OpenAI

# Configuração da página com parâmetros mínimos
st.set_page_config(page_title="Teste API OpenAI", page_icon="🔍")

st.title("Teste de Conexão com API OpenAI")
st.write("Este é um aplicativo simples para testar a conexão com a API da OpenAI.")

# Inicialização da sessão
if 'client' not in st.session_state:
    st.session_state.client = None
if 'api_key_configured' not in st.session_state:
    st.session_state.api_key_configured = False

# Interface para entrada da API key
api_key = st.text_input("OpenAI API Key", type="password", help="Insira sua chave de API da OpenAI")

if api_key:
    try:
        # Inicialização básica do cliente OpenAI
        st.session_state.client = OpenAI(api_key=api_key)
        if not st.session_state.api_key_configured:
            st.session_state.api_key_configured = True
            st.success("API configurada com sucesso!")
    except Exception as e:
        st.error(f"Erro ao configurar a API: {str(e)}")

# Teste simples de geração de texto
if st.session_state.api_key_configured:
    if st.button("Testar API"):
        try:
            with st.spinner("Testando conexão com a API..."):
                response = st.session_state.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "Olá, por favor responda com uma frase curta."}],
                    temperature=0.7,
                    max_tokens=50
                )
                
                st.success("Conexão estabelecida com sucesso!")
                st.write("Resposta da API:")
                st.write(response.choices[0].message.content)
                
                # Exibir informações de uso
                st.write("Informações de uso:")
                st.write(f"Tokens de entrada: {response.usage.prompt_tokens}")
                st.write(f"Tokens de saída: {response.usage.completion_tokens}")
                st.write(f"Total de tokens: {response.usage.total_tokens}")
                
        except Exception as e:
            st.error(f"Erro ao testar a API: {str(e)}")
else:
    st.info("Por favor, configure sua API key para testar a conexão.")

# Rodapé com informações
st.markdown("---")
st.caption("Este é um aplicativo de teste simples para verificar a conexão com a API da OpenAI.")
