# 🏐 Torneio de Vôlei 🏐

Sistema web desenvolvido em Streamlit para criação automática de torneios de vôlei com:

- Sorteio de times
- Distribuição automática de jogadores
- Separação por grupos
- Geração de confrontos
- Exportação para Excel

## 🚀 Funcionalidades

- Criação automática de times baseada nos cabeças de chave
- Distribuição obrigatória de 1 mulher por time
- Suporte a número ilimitado de jogadores
- Geração automática de grupos equilibrados
- Criação de tabela de jogos (fase de grupos)
- Estrutura de mata-mata (semifinal e final)
- Exportação completa para Excel (.xlsx)

## 🧠 Regras do Sistema

- Cada cabeça de chave forma um time
- Cada time recebe automaticamente 1 mulher
- O número de mulheres deve ser ≥ número de times
- Jogadores restantes são distribuídos automaticamente
- Os times são divididos em 2 grupos equilibrados

## 🖥️ Como usar

1. Insira os cabeças de chave (um por linha)
2. Insira as mulheres (mínimo igual ao número de times)
3. Insira os demais jogadores
4. Clique em "Sortear Torneio"
5. Visualize os grupos e jogos
6. Baixe a planilha Excel

## 📊 Estrutura do Excel

O arquivo gerado contém:

- Aba "Times": jogadores por equipe
- Aba "Grupos": divisão dos grupos
- Aba "Jogos": confrontos da fase de grupos
- Aba "Mata-Mata": estrutura das finais

## ⚙️ Tecnologias

- Python
- Streamlit
- OpenPyXL

## 📦 Instalação

```bash
git clone https://github.com/saulosilva85/Torneio-de-Volei
cd seu-repo
pip install -r requirements.txt
streamlit run app.py

## 8. 🌐 Deploy

Se estiver no Streamlit Cloud:

```md
## 🌐 Deploy

Aplicação disponível via Streamlit Cloud.

## 📈 Roadmap

- [ ] Classificação automática por pontos
- [ ] Inserção de resultados
- [ ] Ranking em tempo real
- [ ] Definição automática de campeão
- [ ] Interface mobile aprimorada

## 🧑‍💻 Autor

Desenvolvido por Saulo Santos