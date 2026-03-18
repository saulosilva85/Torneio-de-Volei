import streamlit as st
import random
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Sorteio de Times PRO", layout="centered")

st.title("🏐 Sorteio Inteligente de Times")

# 🔎 Base simples de nomes brasileiros (pode expandir depois)
nomes_masculinos = {
    "joao","carlos","pedro","lucas","marcos","andre","rafael","bruno","gabriel","felipe"
}

nomes_femininos = {
    "maria","ana","julia","fernanda","patricia","camila","beatriz","larissa","amanda","juliana"
}

# 🔎 Detecção inteligente
def detectar_genero(nome):
    primeiro_nome = nome.split()[0].lower()

    if primeiro_nome in nomes_masculinos:
        return "M"
    elif primeiro_nome in nomes_femininos:
        return "F"

    # fallback heurístico
    if primeiro_nome.endswith("a"):
        return "F"
    elif primeiro_nome.endswith(("o","r","l")):
        return "M"
    else:
        return random.choice(["M","F"])

def gerar_excel(times):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')

    for time, integrantes in times.items():
        df = pd.DataFrame(integrantes, columns=["Jogadores"])
        df.to_excel(writer, sheet_name=time, index=False)

    writer.close()
    output.seek(0)
    return output

# 📥 Inputs
st.markdown("### Cabeças de Chave (2 a 6)")
cabecas_input = st.text_area("Digite os nomes", height=120)

st.markdown("### Demais Jogadores")
jogadores_input = st.text_area("Digite os nomes", height=200)

if st.button("🎲 Sortear Times"):

    cabecas = [c.strip() for c in cabecas_input.split("\n") if c.strip()]
    jogadores = [j.strip() for j in jogadores_input.split("\n") if j.strip()]

    if len(cabecas) < 2 or len(cabecas) > 6:
        st.error("Você deve inserir entre 2 e 6 cabeças de chave.")
        st.stop()

    num_times = len(cabecas)

    todos = cabecas + jogadores

    # 🔎 Detectar gênero
    generos_detectados = {nome: detectar_genero(nome) for nome in todos}

    st.markdown("### 🔧 Confirme / ajuste os gêneros")

    generos_corrigidos = {}

    # 🧠 Interface de correção manual
    for nome in todos:
        generos_corrigidos[nome] = st.selectbox(
            f"{nome}",
            ["M", "F"],
            index=0 if generos_detectados[nome] == "M" else 1
        )

    if st.button("✅ Confirmar e Gerar Times"):

        homens = [n for n, g in generos_corrigidos.items() if g == "M"]
        mulheres = [n for n, g in generos_corrigidos.items() if g == "F"]

        # Criar times
        times = {f"Time {i+1}": [] for i in range(num_times)}

        # Distribuir cabeças de chave primeiro
        random.shuffle(cabecas)
        for i in range(num_times):
            times[f"Time {i+1}"].append(cabecas[i])

        # Separar restantes
        restantes = [j for j in jogadores]

        # Separar por gênero
        homens = [n for n in restantes if generos_corrigidos[n] == "M"]
        mulheres = [n for n in restantes if generos_corrigidos[n] == "F"]

        random.shuffle(homens)
        random.shuffle(mulheres)

        # Distribuir equilibrado
        for i, jogador in enumerate(homens):
            times[f"Time {(i % num_times) + 1}"].append(jogador)

        for i, jogador in enumerate(mulheres):
            times[f"Time {(i % num_times) + 1}"].append(jogador)

        st.success("Times gerados com balanceamento inteligente!")

        for time, integrantes in times.items():
            st.markdown(f"## 🏆 {time}")
            for jogador in integrantes:
                st.write(f"• {jogador}")

        excel_file = gerar_excel(times)

        st.download_button(
            label="📥 Baixar Excel",
            data=excel_file,
            file_name="times_inteligentes.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )