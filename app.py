import streamlit as st
import random

st.set_page_config(page_title="Sorteio de Times", layout="centered")

st.title("🏐 Torneio de Vôlei")

st.markdown("### Cabeças de Chave (Inserir de 2 a 6 jogadores)")
cabecas_input = st.text_area("Digite um nome por linha", height=120)

st.markdown("### Demais Jogadores")
jogadores_input = st.text_area("Digite um nome por linha", height=200)


# 🔎 Detecção de gênero (PRIORIDADE para "?")
def detectar_genero(nome):
    nome = nome.lower().strip()

    if "?" in nome:
        return "F"

    if nome.endswith("a"):
        return "F"
    elif nome.endswith(("o", "r", "l")):
        return "M"
    else:
        return random.choice(["M", "F"])


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
        st.error(f"Você precisa de exatamente {total_necessario} jogadores no total.")
        st.stop()

    # 🔥 Separação INTELIGENTE
    mulheres_prioridade = []  # com "?"
    outras_mulheres = []
    homens = []

    for nome in cabecas + jogadores:
        if "?" in nome:
            mulheres_prioridade.append(nome)
        else:
            genero = detectar_genero(nome)
            if genero == "F":
                outras_mulheres.append(nome)
            else:
                homens.append(nome)

    # Criar times
    times = {f"Time {i+1}": [] for i in range(num_times)}

    # 🔥 PASSO 1 — garantir 1 mulher por time (priorizando "?")
    pool_mulheres = mulheres_prioridade + outras_mulheres
    random.shuffle(pool_mulheres)

    for i in range(min(len(pool_mulheres), num_times)):
        times[f"Time {i+1}"].append(pool_mulheres[i])

    # 🔥 PASSO 2 — adicionar cabeças de chave restantes
    cabecas_restantes = [c for c in cabecas if c not in pool_mulheres]
    random.shuffle(cabecas_restantes)

    for i, jogador in enumerate(cabecas_restantes):
        time = f"Time {(i % num_times) + 1}"
        if len(times[time]) < 4:
            times[time].append(jogador)

    # 🔥 PASSO 3 — completar com restantes
    restantes = [j for j in jogadores if j not in pool_mulheres]
    random.shuffle(restantes)

    i = 0
    for jogador in restantes:
        tentativas = 0
        while tentativas < num_times:
            time = f"Time {(i % num_times) + 1}"
            if len(times[time]) < 4:
                times[time].append(jogador)
                i += 1
                break
            i += 1
            tentativas += 1

    st.success("Sorteio realizado com 1 mulher por time (prioridade para '?')!")

    # Exibir resultado
    for time, integrantes in times.items():
        st.markdown(f"# 🏆 {time} ({len(integrantes)}/4)")
        for jogador in integrantes:
            st.write(f"• {jogador}")