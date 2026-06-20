from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

# Define os caminhos relativos para os arquivos
FILE_PATH = "data/lore_geralt.txt"
DB_DIR = "rag/chroma_db"

def build_database():
    print("1. Lendo o arquivo de texto...")
    # O encoding='utf-8' previne erros de leitura com acentuações no Windows
    loader = TextLoader(FILE_PATH, encoding="utf-8")
    documento = loader.load()

    print("2. Quebrando o texto em pedaços menores (chunks)...")
    # Divide o texto em blocos de 1000 caracteres, com uma sobreposição de 200 caracteres para preservar o contexto
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documento)
    print(f"Texto dividido em {len(chunks)} pedaços.")

    print("3. Carregando o modelo de embeddings (pode demorar na primeira execução)...")
    # Modelo leve e eficiente para rodar localmente e gerar os vetores matemáticos
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print("4. Criando e salvando o banco de dados vetorial (ChromaDB)...")
    db = Chroma.from_documents(chunks, embeddings, persist_directory=DB_DIR)
    
    print("Sucesso! Banco de dados RAG criado e salvo na pasta rag/chroma_db.")

if __name__ == "__main__":
    build_database()