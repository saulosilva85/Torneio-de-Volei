import streamlit as st
import random

st.set_page_config(page_title="Sorteio de Times", layout="centered")

st.title("🏐 Torneio de Vôlei")

st.markdown("### Cabeças de Chave (Inserir de 2 a 6 jogadores)")
cabecas_input = st.text_area("Digite um nome por linha", height=120)

st.markdown("### Demais Jogadores")
jogadores_input = st.text_area("Digite um nome por linha", height=200)


# 🔎 Função simples de detecção de gênero
def detectar_genero(nome):
    nome = nome.lower().strip()

    if nome.endswith("a"):
        return "F"
    elif nome.endswith(("o", "r", "l")):
        return "M"
    else:
        return random.choice(["M", "F"])


# 🔎 Separar por gênero
def separar_generos(lista):
    homens = []
    mulheres = []

    for nome in lista:
        genero = detectar_genero(nome)
        if genero == "M":
            homens.append(nome)
        else:
            mulheres.append(nome)

    return homens, mulheres


if st.button("🎲 Sortear Times"):
    cabecas = [c.strip() for c in cabecas_input.split("\n") if c.strip()]
    jogadores = [j.strip() for j in jogadores_input.split("\n") if j.strip()]

    # Validação
    if len(cabecas) < 2 or len(cabecas) > 6:
        st.error("Você deve inserir entre 2 e 6 cabeças de chave.")
    else:
        num_times = len(cabecas)

        # Separar todos por gênero
        cab_h, cab_m = separar_generos(cabecas)
        jog_h, jog_m = separar_generos(jogadores)

        # Criar times
        times = {f"Time {i+1}": [] for i in range(num_times)}

        # 🔥 Distribuir cabeças de chave alternando gênero
        cabecas_mix = cab_h + cab_m
        random.shuffle(cabecas_mix)

        for i in range(num_times):
            times[f"Time {i+1}"].append(cabecas_mix[i])

        # Embaralhar jogadores
        random.shuffle(jog_h)
        random.shuffle(jog_m)

        # ⚖️ Distribuir homens equilibradamente
        for i, jogador in enumerate(jog_h):
            time = f"Time {(i % num_times) + 1}"
            times[time].append(jogador)

        # ⚖️ Distribuir mulheres equilibradamente
        for i, jogador in enumerate(jog_m):
            time = f"Time {(i % num_times) + 1}"
            times[time].append(jogador)

        st.success("Sorteio realizado com balanceamento!")

        # Exibir resultado
        for time, integrantes in times.items():
            st.markdown(f"# 🏆 {time}")
            for jogador in integrantes:
                st.write(f"• {jogador}")