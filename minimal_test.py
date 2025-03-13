import streamlit as st
from openai import OpenAI

st.title("Minimal OpenAI Test")

# API key do input manual apenas
api_key = st.text_input("OpenAI API Key", type="password")

if api_key and st.button("Testar"):
    st.write("Tentando conectar com a API...")
    
    try:
        # Cliente com configuração mínima
        client = OpenAI(api_key=api_key)
        
        # Teste mais simples possível
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Olá"}],
            max_tokens=5
        )
        
        st.success(f"Funcionou! Resposta: {response.choices[0].message.content}")
        
    except Exception as e:
        st.error(f"Erro: {type(e).__name__}: {str(e)}")
