import streamlit as st
import openai

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
    # Configurar a API key (versão antiga da biblioteca)
    openai.api_key = api_key
    
    if st.button("Testar Conexão"):
        try:
            with st.spinner("Testando..."):
                # Chamada mais básica possível (sintaxe da versão 0.28.1)
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "Responda apenas com a palavra 'Funcionou'"}],
                    max_tokens=5
                )
                
                # Mostrar resultado
                resultado = response['choices'][0]['message']['content']
                st.success(f"Conexão estabelecida! Resposta: {resultado}")
                
        except Exception as e:
            st.error(f"Erro na conexão: {str(e)}")
else:
    st.info("Por favor, forneça uma API key para testar.")
        except Exception as e:
            st.error(f"Erro na conexão: {str(e)}")
else:
    st.info("Por favor, forneça uma API key para testar.")
