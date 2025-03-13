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
st.info("Compatível com chaves API atuais (sk-proj-) e antigas (sk-)")

# API key do input manual apenas
api_key = st.text_input("OpenAI API Key", type="password", 
                        help="Insira sua chave API da OpenAI (formatos sk-proj- e sk-svca- são suportados)")

# Informações sobre a API
with st.expander("Sobre as chaves API da OpenAI"):
    st.write("""
    Novas chaves API da OpenAI agora começam com `sk-proj-` ou `sk-svca-`. 
    Este formato é uma mudança recente na organização da OpenAI para melhor controle de projetos e faturamento.
    
    Chaves antigas que começavam apenas com `sk-` não são mais geradas para novas contas.
    """)

if api_key and st.button("Testar Conexão"):
    st.write("Tentando conectar com a API via HTTP direto...")
    
    try:
        # Definir cabeçalhos com a chave API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # Dados para o teste
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Olá, responda apenas com uma palavra."}],
            "max_tokens": 5
        }
        
        # Adicionar headers específicos para formatos novos, se necessário
        if api_key.startswith("sk-proj-"):
            st.info("Detectada chave no formato de projeto (sk-proj-)")
        elif api_key.startswith("sk-svca-"):
            st.info("Detectada chave de conta de serviço (sk-svca-)")
        
        # Fazer a requisição diretamente à API
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=30
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
            st.write(f"Total de tokens: {result['usage']['total_tokens']}")
            
            # Exibir opções para prosseguir
            st.write("✅ Conexão com a API OpenAI estabelecida com sucesso!")
            st.info("Você pode usar esta abordagem para implementar o NEXUS completo.")
        else:
            st.error(f"Erro da API: Status {response.status_code}")
            st.code(response.text)
            
            # Mostrar ajuda específica com base no código de erro
            if response.status_code == 401:
                st.warning("""
                Erro 401: Autenticação falhou. Verifique se sua chave API está correta e ativa.
                Se você está usando uma chave organizacional ou de projeto, certifique-se de que ela tem permissões adequadas.
                """)
            elif response.status_code == 429:
                st.warning("Erro 429: Limite de taxa excedido. Sua conta pode ter atingido o limite de solicitações ou crédito.")
        
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão: {str(e)}")
    except Exception as e:
        st.error(f"Erro inesperado: {type(e).__name__}: {str(e)}")
