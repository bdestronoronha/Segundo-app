import pandas as pd
import streamlit as st

# Configuração da Página
st.set_page_config(
    page_title="Simulador de Custos e Orçamento", page_icon="💰", layout="wide"
)


# Base de Dados Interna Simulada (10 itens)
@st.cache_data
def carregar_dados():
  dados = {
      "Item": [
          "Chapa de Aço Inox",
          "Parafusos e Fixadores",
          "Soldador Especializado",
          "Frete Regional",
          "Energia da Oficina",
          "Chave de Fenda de Precisão",
          "Aluguel de Empilhadeira",
          "Lubrificantes Industriais",
          "EPIs Básicos",
          "Consultoria Técnica",
      ],
      "Categoria": [
          "Matéria-Prima",
          "Matéria-Prima",
          "Mão de Obra",
          "Logística",
          "Energia",
          "Ferramentas",
          "Logística",
          "Matéria-Prima",
          "Ferramentas",
          "Mão de Obra",
      ],
      "Valor (R$)": [
          4500.0,
          800.0,
          6500.0,
          1200.0,
          1500.0,
          350.0,
          2200.0,
          600.0,
          450.0,
          3500.0,
      ],
      "Prioridade": [
          "Alta",
          "Baixa",
          "Alta",
          "Média",
          "Alta",
          "Baixa",
          "Média",
          "Baixa",
          "Média",
          "Alta",
      ],
  }
  return pd.DataFrame(dados)


df = carregar_dados()

# 1. Barra Lateral (Sidebar)
st.sidebar.header("⚙️ Painel de Controle")

orcamento_total = st.sidebar.slider(
    "Orçamento Total Disponível (R$)",
    min_value=5000.0,
    max_value=50000.0,
    value=20000.0,
    step=500.0,
)

categorias_disponiveis = df["Categoria"].unique().tolist()
categorias_selecionadas = st.sidebar.multiselect(
    "Filtrar por Categoria",
    options=categorias_disponiveis,
    default=categorias_disponiveis,
)

# Lógica de Filtragem
if categorias_selecionadas:
  df_filtrado = df[df["Categoria"].isin(categorias_selecionadas)]
else:
  df_filtrado = df.iloc[0:0]  # DataFrame vazio se nenhum filtro for marcado

# 3. Área Principal
st.title("📊 Simulador de Custos e Orçamento")
st.markdown(
    "Gerencie despesas, visualize impactos por categoria e acompanhe seu saldo"
    " em tempo real."
)
st.divider()

# Cálculos Financeiros
gasto_filtrado = df_filtrado["Valor (R$)"].sum()
saldo_restante = orcamento_total - gasto_filtrado

# Painel de 3 Métricas
col1, col2, col3 = st.columns(3)
with col1:
  st.metric(label="Orçamento Definido", value=f"R$ {orcamento_total:,.2f}")
with col2:
  st.metric(label="Gasto Filtrado", value=f"R$ {gasto_filtrado:,.2f}")
with col3:
  st.metric(
      label="Saldo Restante",
      value=f"R$ {saldo_restante:,.2f}",
      delta=f"R$ {saldo_restante:,.2f}",
      delta_color="normal" if saldo_restante >= 0 else "inverse",
  )

# Alerta Visual Condicional
if gasto_filtrado <= orcamento_total:
  st.success(
      "✅ **Projeto dentro da meta!** O gasto total filtrado está dentro do"
      " limite do orçamento estabelecido."
  )
else:
  excedente = gasto_filtrado - orcamento_total
  st.error(
      f"🚨 **Alerta de Orçamento Estourado!** Os custos filtrados ultrapassam"
      f" o orçamento em **R$ {excedente:,.2f}**."
  )

st.markdown("### 📈 Visualização e Detalhamento")

if not df_filtrado.empty:
  col_grafico, col_tabela = st.columns(2)

  with col_grafico:
    st.subheader("Gastos por Categoria")
    # Agrupamento otimizado para o st.bar_chart nativo
    df_cat = (
        df_filtrado.groupby("Categoria")["Valor (R$)"].sum().reset_index()
    )
    st.bar_chart(df_cat.set_index("Categoria"))

  with col_tabela:
    st.subheader("Itens Correspondentes")
    st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
else:
  st.warning(
      "Nenhuma categoria selecionada. Por favor, selecione ao menos uma"
      " categoria na barra lateral."
  )
