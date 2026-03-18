import streamlit as st
import random

st.set_page_config(page_title="Sorteio de Times", layout="centered")

st.title("🏐 Torneio de Vôlei")

st.markdown("### Cabeças de Chave (Inserir de 2 a 6 jogadores)")
cabecas_input = st.text_area("Digite um nome por linha", height=120)

st.markdown("### Demais Jogadores")
jogadores_input = st.text_area("Digite um nome por linha", height=200)


def detectar_genero(nome):
    nome = nome.lower().strip()

    if nome.endswith("a"):
        return "F"
    elif nome.endswith(("o", "r", "l")):
        return "M"
    else:
        return "M"


if st.button("🎲 Sortear Times"):
    cabecas = [c.strip() for c in cabecas_input.split("\n") if c.strip()]
    jogadores = [j.strip() for j in jogadores_input.split("\n") if j.strip()]

    if len(cabecas) < 2 or len(cabecas) > 6:
        st.error("Você deve inserir entre 2 e 6 cabeças de chave.")
        st.stop()

    num_times = len(cabecas)

    total_necessario = num_times * 4
    total_atual = len(cabecas) + len(jogadores)

    if total_atual != total_necessario:
        st.error(f"Você precisa de exatamente {total_necessario} jogadores.")
        st.stop()

    todos = cabecas + jogadores

    mulheres = [n for n in todos if detectar_genero(n) == "F"]

    if len(mulheres) < num_times:
        st.error(f"Precisa de pelo menos {num_times} mulheres.")
        st.stop()

    # 🔥 Criar times com cabeça fixa
    times = {f"Time {i+1}": [cabecas[i]] for i in range(num_times)}

    # 🔥 Separar mulheres
    mulheres_cabeca = [c for c in cabecas if detectar_genero(c) == "F"]
    mulheres_restantes = [m for m in mulheres if m not in mulheres_cabeca]

    random.shuffle(mulheres_restantes)

    # 🔥 GARANTIR 1 mulher por time
    for i in range(num_times):
        time = f"Time {i+1}"
        cabeca = cabecas[i]

        if detectar_genero(cabeca) == "F":
            continue  # já tem mulher

        if not mulheres_restantes:
            st.error("Erro: faltam mulheres para distribuir.")
            st.stop()

        times[time].append(mulheres_restantes.pop())

    # 🔥 Completar times
    usados = set(sum(times.values(), []))
    restantes = [j for j in todos if j not in usados]

    random.shuffle(restantes)

    for jogador in restantes:
        for i in range(num_times):
            time = f"Time {i+1}"
            if len(times[time]) < 4:
                times[time].append(jogador)
                break

    st.success("Sorteio realizado corretamente com 1 mulher por time!")

    for time, integrantes in times.items():
        st.markdown(f"# 🏆 {time} ({len(integrantes)}/4)")
        for jogador in integrantes:
            st.write(f"• {jogador}")