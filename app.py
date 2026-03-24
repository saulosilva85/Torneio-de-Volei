import streamlit as st
import random

st.set_page_config(page_title="Sorteio de Times", layout="centered")

st.title("🏐 Open Village 18+ 🏐")

# ✅ Texto ajustado (sem obrigatoriedade de 5 homens)
st.markdown("### Cabeças de Chave")
cabecas_input = st.text_area("Digite um nome por linha", height=120)

st.markdown("### Demais Jogadores")
jogadores_input = st.text_area("Digite um nome por linha", height=200)


# 🔎 Função de detecção de gênero (somente para os demais jogadores)
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

    # ✅ Validação: precisa ter pelo menos 1 cabeça
    if len(cabecas) == 0:
        st.error("Adicione pelo menos 1 cabeça de chave.")
        st.stop()

    num_times = len(cabecas)

    # ✅ Total de jogadores necessário (4 por time)
    total_necessario = num_times * 4
    total_atual = len(cabecas) + len(jogadores)

    if total_atual != total_necessario:
        st.error(f"Você precisa de exatamente {total_necessario} jogadores no total ({num_times} times de 4).")
        st.stop()

    # 🚨 Validação de nomes duplicados
    todos_nomes = cabecas + jogadores
    if len(set(todos_nomes)) != len(todos_nomes):
        st.error("Existem nomes duplicados. Corrija antes de sortear.")
        st.stop()

    # 🔥 Separar mulheres (somente dos demais jogadores)
    mulheres_jogadores = [n for n in jogadores if detectar_genero(n) == "F"]
    total_mulheres = len(mulheres_jogadores)

    # 🚨 Regra obrigatória: 1 mulher por time
    if total_mulheres < num_times:
        st.error(f"É necessário pelo menos {num_times} mulheres (1 por time).")
        st.stop()

    # 🔥 Criar times com cabeças fixos
    times = {f"Time {i+1}": [cabecas[i]] for i in range(num_times)}

    # 🔥 PASSO 1 — Garantir 1 mulher por time
    mulheres_disponiveis = mulheres_jogadores.copy()
    random.shuffle(mulheres_disponiveis)

    for i in range(num_times):
        time = f"Time {i+1}"
        mulher = mulheres_disponiveis.pop()
        times[time].append(mulher)

    # 🔥 PASSO 2 — Preencher restantes
    usados = set()
    for jogadores_time in times.values():
        usados.update(jogadores_time)

    restantes = [j for j in jogadores if j not in usados]
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

    # 📊 Exibir resultado
    for time, integrantes in times.items():
        st.markdown(f"# 🏆 {time} ({len(integrantes)}/4)")
        for jogador in integrantes:
            st.write(f"• {jogador}")