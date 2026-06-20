import os
from datetime import datetime
from colorama import Fore, Style, init
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.tools import tool

# Inicializa cores do terminal
init(autoreset=True)

# 1. Configurações e Banco (Simulando um Recurso MCP)
DB_DIR = "rag/chroma_db"
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
llm = Ollama(model="llama3")

# 2. Tools (Conforme Requisito 7 e MCP)
@tool
def buscar_lore_oficial(query: str):
    """Ferramenta para recuperar fatos oficiais do universo The Witcher no banco vetorial."""
    print(f"\n{Fore.CYAN}[MCP Resource] Acessando base de dados vetorial via Tool...{Style.RESET_ALL}")
    docs = db.similarity_search(query, k=4)
    return "\n".join([doc.page_content for doc in docs])

@tool
def registrar_laudo_markdown(conteudo: str):
    """Ferramenta para persistir o parecer da auditoria em formato Markdown."""
    if not os.path.exists("laudos"):
        os.makedirs("laudos")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    caminho = f"laudos/laudo_{timestamp}.md"
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)
    return caminho

# 3. Agentes
def agente_inquisidor(roteiro_usuario):
    print(f"{Fore.CYAN}[Agente 2: Inquisidor] Consolidando auditoria...{Style.RESET_ALL}\n")
    
    # Busca fatos usando a Tool (MCP/RAG)
    fatos = buscar_lore_oficial.invoke(roteiro_usuario)
    
    template = """Você é um auditor rigoroso de lore. Responda APENAS em Português Brasileiro.
    FATOS OFICIAIS: {fatos}
    ROTEIRO: {roteiro}
    Instruções: Se houver contradições, aponte 'FURO DE ROTEIRO' com explicações. Se estiver correto, 'CONTINUIDADE VALIDADA'.
    PARECER DA AUDITORIA:"""
    
    prompt = PromptTemplate(template=template, input_variables=["fatos", "roteiro"])
    laudo = (prompt | llm).invoke({"fatos": fatos, "roteiro": roteiro_usuario})
    
    # Salva usando a Tool de persistência
    caminho = registrar_laudo_markdown.invoke(laudo)
    return laudo, caminho

# 4. Execução
if __name__ == "__main__":
    print(f"{Fore.MAGENTA}=== SISTEMA DE AUDITORIA DE LORE - THE WITCHER ==={Style.RESET_ALL}")
    caminho = input("Digite o caminho do roteiro (.txt):\n> ")
    
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            roteiro = f.read()
        
        laudo, caminho_arquivo = agente_inquisidor(roteiro)
        
        print(f"\n{Fore.GREEN}=== LAUDO FINAL ==={Style.RESET_ALL}\n{laudo}")
        print(f"\n{Fore.YELLOW}>> Salvo em: {caminho_arquivo}{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}Erro: {e}{Style.RESET_ALL}")