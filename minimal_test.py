import streamlit as st
import os
import requests
import json

# Desativar configurações de proxy que podem estar no ambiente
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)
os.environ.pop('OPENAI_PROXY', None)
os.environ.pop('openai_proxy', None)
os.environ['no_proxy'] = '*'

st.title("Teste Direto API OpenAI")
st.write("Esta versão usa requests diretamente, sem a biblioteca OpenAI")

# API key do input manual apenas
api_key = st.text_input("OpenAI API Key", type="password")

if api_key and st.button("Testar"):
    st.write("Tentando conectar com a API via HTTP direto...")
    
    try:
        # Usar requests diretamente para evitar problemas com a biblioteca OpenAI
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Olá, responda apenas com uma palavra."}],
            "max_tokens": 5
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )
        
        # Verificar se a resposta foi bem-sucedida
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            st.success(f"Funcionou! Resposta: {content}")
            
            # Mostrar detalhes do uso para confirmar
            st.write("Detalhes de uso:")
            st.write(f"Tokens de entrada: {result['usage']['prompt_tokens']}")
            st.write(f"Tokens de saída: {result['usage']['completion_tokens']}")
        else:
            st.error(f"Erro da API: Status {response.status_code}")
            st.write(response.text)
        
    except Exception as e:
        st.error(f"Erro: {type(e).__name__}: {str(e)}")
