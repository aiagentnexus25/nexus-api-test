import streamlit as st
from openai import OpenAI

# Configuração mais simples possível
st.set_page_config(page_title="Teste Mínimo OpenAI")

st.title("Teste Mínimo OpenAI API")
st.write("Versão mais básica possível para testar a API OpenAI")

# Usar API key configurada nos secrets
api_key = st.secrets.get("OPENAI_API_KEY", "")

# Opção para digitar API key manualmente
if not api_key:
    api_key = st.text_input("OpenAI API Key", type="password")

# Testar apenas se tiver uma API key
if api_key:
    # Inicialização do cliente (versão nova da API 1.x.x)
    client = OpenAI(api_key=api_key)
    
    if st.button("Testar Conexão"):
        try:
            with st.spinner("Testando..."):
                # Chamada usando a nova sintaxe da versão 1.x.x
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "Responda apenas com a palavra 'Funcionou'"}],
                    max_tokens=5
                )
                
                # Acessar o resultado na nova estrutura
                resultado = response.choices[0].message.content
                st.success(f"Conexão estabelecida! Resposta: {resultado}")
        except Exception as e:
            st.error(f"Erro na conexão: {str(e)}")
else:
    st.info("Por favor, forneça uma API key para testar.")
