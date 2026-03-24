import streamlit as st
import random

st.set_page_config(page_title="Sorteio de Times", layout="centered")

st.title("🏐 Open Village 18+ 🏐")

st.markdown("### Cabeças de Chave (Inserir exatamente 5 jogadores - TODOS HOMENS)")
cabecas_input = st.text_area("Digite um nome por linha", height=120)

st.markdown("### Demais Jogadores (incluindo mulheres)")
jogadores_input = st.text_area("Digite um nome por linha", height=200)


# 🔎 Detecção de gênero (somente para jogadores)
def detectar_genero(nome):
    nome = nome.lower().strip()

    femininos = [
        "ana","maria","julia","juliana","fernanda","patricia","amanda",
        "carla","beatriz","camila","luciana","aline","daniela",
        "milena","mika","joyce","isabela","isabella","gabriela",
        "rafaela","leticia","renata","bianca","bruna","larissa",
        "mariana","paula","priscila","talita","vanessa"
    ]

    primeiro = nome.split()[0]

    if primeiro in femininos:
        return "F"

    if nome.endswith("a"):
        return "F"

    return "M"


if st.button("🎲 Sortear Times"):
    cabecas = [c.strip() for c in cabecas_input.split("\n") if c.strip()]
    jogadores = [j.strip() for j in jogadores_input.split("\n") if j.strip()]

    num_times = 5

    # ✅ Validação cabeças
    if len(cabecas) != num_times:
        st.error("Você deve inserir exatamente 5 cabeças de chave.")
        st.stop()

    # ✅ Validação total jogadores
    total_necessario = num_times * 4
    total_atual = len(cabecas) + len(jogadores)

    if total_atual != total_necessario:
        st.error(f"Você precisa de exatamente {total_necessario} jogadores no total.")
        st.stop()

    # 🚨 Sem duplicados
    todos = cabecas + jogadores
    if len(set(todos)) != len(todos):
        st.error("Existem nomes duplicados.")
        st.stop()

    # 🔥 Mulheres (somente dos jogadores)
    mulheres = [j for j in jogadores if detectar_genero(j) == "F"]

    if len(mulheres) < num_times:
        st.error(f"É necessário pelo menos {num_times} mulheres nos jogadores.")
        st.stop()

    # 🔥 Criar times (cabeças fixos - homens)
    times = {f"Time {i+1}": [cabecas[i]] for i in range(num_times)}

    # 🔥 PASSO 1 — garantir exatamente 1 mulher por time
    random.shuffle(mulheres)

    mulheres_usadas = mulheres[:num_times]  # pega exatamente 5
    mulheres_restantes = mulheres[num_times:]

    for i in range(num_times):
        time = f"Time {i+1}"
        times[time].append(mulheres_usadas[i])

    # 🔥 PASSO 2 — restantes (SEM duplicar)
    usados = set(cabecas + mulheres_usadas)

    restantes = [j for j in jogadores if j not in usados]
    random.shuffle(restantes)

    # 🔥 PASSO 3 — completar times
    for jogador in restantes:
        for i in range(num_times):
            time = f"Time {i+1}"
            if len(times[time]) < 4:
                times[time].append(jogador)
                break

    # 🔒 VALIDAÇÃO FINAL (garantia absoluta)
    for time, integrantes in times.items():
        if len(integrantes) != 4:
            st.error(f"{time} não tem 4 jogadores.")
            st.stop()

        if not any(detectar_genero(j) == "F" for j in integrantes):
            st.error(f"{time} ficou sem mulher.")
            st.stop()

    st.success("Sorteio realizado com sucesso!")

    # 📊 Exibir
    for time, integrantes in times.items():
        st.markdown(f"# 🏆 {time} ({len(integrantes)}/4)")
        for j in integrantes:
            st.write(f"• {j}")