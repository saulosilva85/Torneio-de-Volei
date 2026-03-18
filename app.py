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
    primeiro_nome = nome.split()[0]

    # PRIORIDADE: ?
    if "?" in nome:
        return "F"

    # Base de nomes femininos comuns
    nomes_femininos = {
        "maria","ana","julia","fernanda","patricia","camila",
        "beatriz","larissa","amanda","juliana","carla","Rê"
    }

    if primeiro_nome in nomes_femininos:
        return "F"

    # Heurística
    if nome.endswith("a"):
        return "F"
    elif nome.endswith(("o", "r", "l")):
        return "M"
    else:
        return "M"  # fallback mais seguro


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

    # Validação cabeças
    if len(cabecas) < 2 or len(cabecas) > 6:
        st.error("Você deve inserir entre 2 e 6 cabeças de chave.")
        st.stop()

    num_times = len(cabecas)

    # 🔥 Validação TOTAL de jogadores
    total_necessario = num_times * 4
    total_atual = len(cabecas) + len(jogadores)

    if total_atual != total_necessario:
        st.error(f"Você precisa de exatamente {total_necessario} jogadores no total.")
        st.stop()

    # Separar por gênero
    cab_h, cab_m = separar_generos(cabecas)
    jog_h, jog_m = separar_generos(jogadores)

    mulheres = cab_m + jog_m
    homens = cab_h + jog_h

    # 🚨 REGRA OBRIGATÓRIA
    if len(mulheres) != num_times:
        st.error(f"É obrigatório ter exatamente {num_times} mulheres (1 por time).")
        st.stop()

    # Criar times
    times = {f"Time {i+1}": [] for i in range(num_times)}

    # 🔥 PASSO 1 — 1 mulher por time (GARANTIDO)
    random.shuffle(mulheres)

    for i in range(num_times):
        times[f"Time {i+1}"].append(mulheres[i])

    # 🔥 PASSO 2 — adicionar cabeças de chave restantes
    cabecas_restantes = [c for c in cabecas if c not in mulheres]
    random.shuffle(cabecas_restantes)

    for i, jogador in enumerate(cabecas_restantes):
        time = f"Time {(i % num_times) + 1}"
        if len(times[time]) < 4:
            times[time].append(jogador)

    # 🔥 PASSO 3 — completar com demais jogadores
    restantes = [j for j in jogadores if j not in mulheres]
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

    st.success("Sorteio realizado com 1 mulher por time!")

    # Exibir resultado
    for time, integrantes in times.items():
        st.markdown(f"# 🏆 {time} ({len(integrantes)}/4)")
        for jogador in integrantes:
            st.write(f"• {jogador}")