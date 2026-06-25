# Auditor de Lore - The Witcher (Sistema Multiagente)

Projeto final da disciplina de Inteligência Artificial. Este sistema realiza auditoria automática de continuidade (lore) para a franquia The Witcher utilizando arquitetura multiagente, Retrieval-Augmented Generation (RAG) e execução local de modelos de linguagem.

## Integrantes

* Álan Da Silva Brum
* Vitório Quadros da Silva
* Marcelo De Mello Copelli
* Lucas Zanini Minussi

## Descrição do Problema

Universos ficcionais complexos possuem uma grande quantidade de personagens, eventos, locais e regras próprias. Durante a produção de novos roteiros, é comum que autores introduzam inconsistências em relação ao cânone oficial da obra.

O problema abordado por este projeto consiste em verificar automaticamente se um roteiro proposto está de acordo com os fatos estabelecidos no universo de The Witcher.

## Objetivo da Solução

Desenvolver um sistema capaz de analisar roteiros e identificar possíveis inconsistências de lore, auxiliando roteiristas e revisores na validação da continuidade narrativa da franquia.

## Arquitetura Multiagente

O sistema foi desenvolvido seguindo uma arquitetura baseada em agentes especializados e ferramentas (Tools). O agente principal é responsável pela análise do roteiro e utiliza ferramentas específicas para recuperar informações da base de conhecimento e registrar os resultados da auditoria.

Essa separação de responsabilidades permite maior organização, modularidade e facilidade de manutenção do sistema.

### Agente Inquisidor

Responsável pela coordenação da auditoria e pela geração do parecer final.

Funções:

* Receber o roteiro informado pelo usuário.
* Solicitar informações relevantes à base de conhecimento.
* Comparar os fatos do roteiro com o conhecimento recuperado.
* Identificar inconsistências narrativas.
* Gerar o laudo final da auditoria.

## Papel de Cada Componente

| Componente             | Responsabilidade                      |
| ---------------------- | ------------------------------------- |
| Agente Inquisidor      | Análise do roteiro e geração do laudo |
| Tool de Busca Vetorial | Recuperação semântica de informações  |
| Tool de Persistência   | Armazenamento dos laudos gerados      |

## Tools Disponíveis

O sistema utiliza ferramentas especializadas para abstrair o acesso aos recursos externos.

### Tool de Busca Vetorial

Responsável por consultar a base vetorial ChromaDB e recuperar documentos semanticamente relevantes para a análise.

### Tool de Leitura de Arquivos

Responsável por carregar os roteiros submetidos para auditoria.

### Tool de Geração de Laudos

Responsável por armazenar o resultado da análise em arquivos de saída.

## Utilização do MCP

O projeto adota os princípios do Model Context Protocol (MCP) por meio da utilização de Tools que encapsulam o acesso aos recursos externos.

Em vez de acessar diretamente arquivos ou bancos de dados, o agente interage com ferramentas especializadas responsáveis por executar essas operações. Dessa forma, o sistema segue a ideia central do MCP de separar agentes inteligentes dos recursos utilizados durante a execução, promovendo desacoplamento, reutilização e organização arquitetural.

## Estratégia de RAG

O sistema utiliza Retrieval-Augmented Generation (RAG) para fornecer contexto confiável ao modelo de linguagem.

Fluxo:

1. Os documentos da base de conhecimento são carregados.
2. O conteúdo é dividido em fragmentos menores (chunks).
3. Cada fragmento é convertido em embeddings vetoriais.
4. Os embeddings são armazenados no banco vetorial ChromaDB.
5. Durante a auditoria, é realizada uma busca semântica na base vetorial.
6. Os trechos mais relevantes são recuperados.
7. O contexto recuperado é enviado ao modelo de linguagem.
8. O modelo gera o parecer final com base nas informações encontradas.

## Origem e Natureza da Base de Conhecimento

A base de conhecimento foi construída a partir de informações obtidas na Wiki oficial da comunidade de The Witcher e de conteúdos relacionados ao universo da franquia.

Os dados foram organizados em arquivos de texto armazenados na pasta:

data/

Esses documentos contêm informações canônicas sobre personagens, eventos, locais e elementos importantes da narrativa, servindo como fonte de consulta para a auditoria de lore.

## Embeddings e Armazenamento Vetorial

### Modelo de Embeddings

* all-MiniLM-L6-v2 (Sentence Transformers)

Funções:

* Converter textos em representações vetoriais.
* Permitir busca semântica por similaridade.

### Banco Vetorial

* ChromaDB

Funções:

* Armazenamento dos embeddings.
* Recuperação de documentos relevantes por similaridade vetorial.

## Modelo Local Utilizado

O sistema utiliza o modelo:

* Llama 3

A execução ocorre localmente através do Ollama.

A integração é realizada por meio do LangChain, que envia os prompts ao serviço Ollama em execução na máquina local. Dessa forma, todo o processamento ocorre localmente, sem necessidade de APIs externas.

Vantagens:

* Privacidade dos dados.
* Baixo custo operacional.
* Independência de serviços externos.
* Execução totalmente local.

Download do modelo:

```bash
ollama pull llama3
```

Inicialização do serviço:

```bash
ollama serve
```

## Dependências do Projeto

```txt
colorama
langchain
langchain-community
langchain-core
langchain-text-splitters
chromadb
sentence-transformers
ollama
```

Instalação:

```bash
pip install -r requirements.txt
```

## Instruções de Instalação e Execução no WINDOWS:

### Pré-requisitos

* Python 3.10 ou superior
* Ollama instalado
* Modelo llama3 baixado

### Passo 1 - Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 2 - Baixar o Modelo

```bash
ollama pull llama3
```

### Passo 3 - Iniciar o Ollama

```bash
ollama serve
```

### Passo 4 - Construir a Base Vetorial

```bash
python rag/build_db.py
```

Observação:

Sempre que novos documentos forem adicionados ou modificados na pasta `data/`, a base vetorial deverá ser reconstruída.

### Passo 5 - Executar o Sistema

```bash
python main.py
```


## Instruções de Instalação e Execução no LINUX:
### Pré requisitos:

* Python 3.10 ou superior
* Ollama instalado (se não estiver instalado: curl -fsSL https://ollama.com/install.sh | sh )

### 1. Crie o ambiente virtual (chamado 'venv')
```bash
python3 -m venv venv
```

### 2. Ative o ambiente virtual
```bash
source venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Instalar o ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 5. Baixar o modelo 
```bash
ollama pull llama3
```

### Passo 6 - Construir a Base Vetorial
```bash
python rag/build_db.py
```
Observação:

Sempre que novos documentos forem adicionados ou modificados na pasta `data/`, a base vetorial deverá ser reconstruída.

### Executar:
```bash
python main.py
```

## Exemplos de Uso pelo Terminal

### Execução

```bash
python main.py
```

Saída:

```text
=== AUDITOR DE LORE - THE WITCHER ===

Digite o caminho do roteiro (.txt):
> data/roteiro_teste.txt
```

### Exemplo de Resultado

```text
=== LAUDO DE AUDITORIA ===

Inconsistências encontradas:

- O roteiro afirma que determinado evento ocorreu em um período incompatível com os fatos registrados na base de conhecimento.

Veredito Final:
REPROVADO
```

O laudo completo será salvo automaticamente na pasta:

```text
laudos/
```
