import streamlit as st
import random

st.set_page_config(page_title="Sorteio de Times", layout="centered")

st.title("🏐 Torneio de Vôlei")

st.markdown("### Cabeças de Chave (Inserir de 2 a 6 jogadores)")
cabecas_input = st.text_area("Digite um nome por linha", height=120)

st.markdown("### Demais Jogadores")
jogadores_input = st.text_area("Digite um nome por linha", height=200)


# 🔎 Função de detecção de gênero
def detectar_genero(nome):
    nome = nome.lower().strip()

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

    todos = cabecas + jogadores

    # 🔥 Separações corretas
    cabecas_f = [c for c in cabecas if detectar_genero(c) == "F"]
    cabecas_m = [c for c in cabecas if detectar_genero(c) != "F"]

    mulheres = [j for j in jogadores if detectar_genero(j) == "F"]
    homens = [j for j in jogadores if detectar_genero(j) != "F"]

    # 🚨 Regra obrigatória
    if len(cabecas_f) + len(mulheres) < num_times:
        st.error(f"É necessário pelo menos {num_times} mulheres no total.")
        st.stop()

    # 🔥 Criar times com cabeça fixo
    times = {}
    for i in range(num_times):
        times[f"Time {i+1}"] = [cabecas[i]]

    # 🔥 PASSO 1 — garantir 1 mulher por time
    random.shuffle(mulheres)

    for i in range(num_times):
        time = f"Time {i+1}"
        cabeca = cabecas[i]

        if detectar_genero(cabeca) == "F":
            continue  # já tem mulher
        else:
            mulher = mulheres.pop()
            times[time].append(mulher)

    # 🔥 PASSO 2 — juntar restantes
    restantes = []

    # mulheres que sobraram
    restantes.extend(mulheres)

    # todos os homens
    restantes.extend(homens)

    random.shuffle(restantes)

    # 🔥 PASSO 3 — completar times até 4 jogadores
    for jogador in restantes:
        for i in range(num_times):
            time = f"Time {i+1}"
            if len(times[time]) < 4:
                times[time].append(jogador)
                break

    st.success("Sorteio realizado com sucesso!")

    # 📊 Exibir resultado
    for time, integrantes in times.items():
        st.markdown(f"# 🏆 {time} ({len(integrantes)}/4)")
        for jogador in integrantes:
            st.write(f"• {jogador}")