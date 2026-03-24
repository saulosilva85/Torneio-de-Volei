import streamlit as st
import random
import unicodedata

st.set_page_config(page_title="Sorteio de Times", layout="centered")

st.title("🏐 Open Village 18+ 🏐")

st.markdown("### Cabeças de Chave")
cabecas_input = st.text_area("Digite um nome por linha", height=120)

st.markdown("### Demais Jogadores")
jogadores_input = st.text_area("Digite um nome por linha", height=200)


# 🔥 Base feminina BR
nomes_femininos = {
    "milena", "mika", "joyce", "re", "isabela"
}


def normalizar(nome):
    nome = nome.lower().strip()
    return ''.join(c for c in unicodedata.normalize('NFD', nome)
                   if unicodedata.category(c) != 'Mn')


def detectar_genero(nome):
    nome_n = normalizar(nome)

    if nome_n in nomes_femininos:
        return "F"

    if nome_n.endswith("a"):
        return "F"

    return "M"


if st.button("🎲 Sortear Times"):

    cabecas = [c.strip() for c in cabecas_input.split("\n") if c.strip()]
    jogadores = [j.strip() for j in jogadores_input.split("\n") if j.strip()]

    if len(cabecas) == 0:
        st.error("Adicione pelo menos 1 cabeça de chave.")
        st.stop()

    num_times = len(cabecas)

    total_necessario = num_times * 4
    total_atual = len(cabecas) + len(jogadores)

    if total_atual != total_necessario:
        st.error(f"Você precisa de exatamente {total_necessario} jogadores.")
        st.stop()

    todos = cabecas + jogadores
    if len(set(todos)) != len(todos):
        st.error("Existem nomes duplicados.")
        st.stop()

    # 🔥 DEBUG AQUI
    mulheres = [j for j in jogadores if detectar_genero(j) == "F"]
    homens = [j for j in jogadores if detectar_genero(j) == "M"]

    st.write("### 🔍 Debug de Gênero")
    st.write("👩 Mulheres detectadas:", mulheres)
    st.write("👨 Homens detectados:", homens)

    if len(mulheres) < num_times:
        st.error(f"É necessário pelo menos {num_times} mulheres (1 por time).")
        st.stop()

    times = {f"Time {i+1}": [cabecas[i]] for i in range(num_times)}

    random.shuffle(mulheres)

    for i in range(num_times):
        times[f"Time {i+1}"].append(mulheres[i])

    restantes = mulheres[num_times:] + homens
    random.shuffle(restantes)

    i = 0
    for jogador in restantes:
        while True:
            time = f"Time {(i % num_times) + 1}"
            if len(times[time]) < 4:
                times[time].append(jogador)
                i += 1
                break
            i += 1

    st.success("Sorteio realizado com sucesso!")

    for time, integrantes in times.items():
        st.markdown(f"# 🏆 {time} ({len(integrantes)}/4)")
        for jogador in integrantes:
            st.write(f"• {jogador}")