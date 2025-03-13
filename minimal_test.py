import streamlit as st
import os
from openai import OpenAI

# Desativar configurações de proxy que podem estar no ambiente
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)
os.environ.pop('OPENAI_PROXY', None)
os.environ.pop('openai_proxy', None)

st.title("Ultra Minimal OpenAI Test")

# API key do input manual apenas
api_key = st.text_input("OpenAI API Key", type="password")

if api_key and st.button("Testar"):
    st.write("Tentando conectar com a API...")
    
    try:
        # Redefinir todos os possíveis argumentos de proxy para None
        # antes de criar o cliente
        os.environ['no_proxy'] = '*'
        
        # Cliente com configuração mínima
        # Usando a classe diretamente para evitar qualquer inicialização padrão
        client = OpenAI.__new__(OpenAI)
        client.api_key = api_key
        client.base_url = "https://api.openai.com/v1"
        
        # Teste mais simples possível
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Olá"}],
            max_tokens=5
        )
        
        st.success(f"Funcionou! Resposta: {response.choices[0].message.content}")
        
    except Exception as e:
        st.error(f"Erro: {type(e).__name__}: {str(e)}")
        
        # Mostrar todas as variáveis de ambiente relevantes para debug
        proxy_vars = {k: v for k, v in os.environ.items() if 'proxy' in k.lower()}
        if proxy_vars:
            st.write("Variáveis de proxy encontradas:")
            st.write(proxy_vars)
