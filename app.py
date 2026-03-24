import streamlit as st
import random

st.set_page_config(page_title="Sorteio de Times", layout="centered")

st.title("🏐 Open Village 18+ 🏐")

# ✅ Cabeças de chave
st.markdown("### Cabeças de Chave (homens)")
cabecas_input = st.text_area("Digite um nome por linha", height=120)

# ✅ Mulheres (SEPARADO - SOLUÇÃO DEFINITIVA)
st.markdown("### Mulheres (1 por time obrigatório)")
mulheres_input = st.text_area("Digite um nome por linha", height=120)

# ✅ Demais jogadores
st.markdown("### Demais Jogadores")
jogadores_input = st.text_area("Digite um nome por linha", height=200)


if st.button("🎲 Sortear Times"):

    cabecas = [c.strip() for c in cabecas_input.split("\n") if c.strip()]
    mulheres = [m.strip() for m in mulheres_input.split("\n") if m.strip()]
    jogadores = [j.strip() for j in jogadores_input.split("\n") if j.strip()]

    # ✅ Validação básica
    if len(cabecas) == 0:
        st.error("Adicione pelo menos 1 cabeça de chave.")
        st.stop()

    num_times = len(cabecas)

    # 🚨 Regra obrigatória
    if len(mulheres) < num_times:
        st.error(f"Você precisa de pelo menos {num_times} mulheres (1 por time).")
        st.stop()

    # ✅ Total necessário
    total_necessario = num_times * 4
    total_atual = len(cabecas) + len(mulheres) + len(jogadores)

    if total_atual != total_necessario:
        st.error(f"Total deve ser {total_necessario} jogadores ({num_times} times de 4).")
        st.stop()

    # 🚨 Duplicados
    todos = cabecas + mulheres + jogadores
    if len(set(todos)) != len(todos):
        st.error("Existem nomes duplicados.")
        st.stop()

    # 🔥 Criar times
    times = {f"Time {i+1}": [cabecas[i]] for i in range(num_times)}

    # 🔥 PASSO 1 — Garantir mulher por time (100% garantido)
    random.shuffle(mulheres)

    for i in range(num_times):
        times[f"Time {i+1}"].append(mulheres[i])

    # 🔥 PASSO 2 — Preencher restantes
    restantes = mulheres[num_times:] + jogadores
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

    # 📊 Exibir
    for time, integrantes in times.items():
        st.markdown(f"# 🏆 {time} ({len(integrantes)}/4)")
        for jogador in integrantes:
            st.write(f"• {jogador}")