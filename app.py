import streamlit as st
import random

st.set_page_config(page_title="Torneio de Vôlei", layout="centered")

st.title("🏐 Torneio de Vôlei - Sorteio + Tabela")

# Inputs
st.markdown("## 🔹 Cabeças de Chave (5 homens)")
cabecas_input = st.text_area("Digite 5 nomes")

st.markdown("## 🔹 Mulheres (5 obrigatórias)")
mulheres_input = st.text_area("Digite 5 nomes femininos")

st.markdown("## 🔹 Demais Jogadores")
jogadores_input = st.text_area("Digite os demais jogadores")


def gerar_tabela(times):
    # Método round-robin com número ímpar
    lista = times[:]
    lista.append("FOLGA")

    n = len(lista)
    rodadas = []

    for rodada in range(n - 1):
        jogos = []
        for i in range(n // 2):
            t1 = lista[i]
            t2 = lista[n - 1 - i]

            if t1 != "FOLGA" and t2 != "FOLGA":
                jogos.append((t1, t2))

        rodadas.append(jogos)

        # Rotaciona (mantém o primeiro fixo)
        lista = [lista[0]] + [lista[-1]] + lista[1:-1]

    return rodadas


if st.button("🎲 Sortear e Gerar Tabela"):

    cabecas = [n.strip() for n in cabecas_input.split("\n") if n.strip()]
    mulheres = [n.strip() for n in mulheres_input.split("\n") if n.strip()]
    jogadores = [n.strip() for n in jogadores_input.split("\n") if n.strip()]

    # Validações
    if len(cabecas) != 5:
        st.error("Informe 5 cabeças de chave.")
        st.stop()

    if len(mulheres) != 5:
        st.error("Informe 5 mulheres.")
        st.stop()

    todos = cabecas + mulheres + jogadores
    if len(todos) != len(set(todos)):
        st.error("Existem nomes duplicados.")
        st.stop()

    random.shuffle(mulheres)
    random.shuffle(jogadores)

    # Criar times
    times = []
    nomes_times = []

    for i in range(5):
        time = [cabecas[i], mulheres[i]]
        times.append(time)
        nomes_times.append(f"Time {i+1}")

    # Distribuir jogadores restantes
    i = 0
    while jogadores:
        times[i % 5].append(jogadores.pop(0))
        i += 1

    # Exibir times
    st.markdown("## 🏆 Times")

    for i, time in enumerate(times):
        st.markdown(f"### {nomes_times[i]}")
        for jogador in time:
            st.write(f"• {jogador}")

    # Gerar tabela
    tabela = gerar_tabela(nomes_times)

    st.markdown("## 📅 Tabela de Jogos (Pontos Corridos)")

    for i, rodada in enumerate(tabela):
        st.markdown(f"### Rodada {i+1}")
        for jogo in rodada:
            st.write(f"{jogo[0]} 🆚 {jogo[1]}")