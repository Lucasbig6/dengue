"""
PAINEL ARBOVIROSES - PIAUÍ
-------------------------
Dashboard analítico para monitoramento de casos de dengue e outras arboviroses.
Desenvolvido para Vigilância Epidemiológica do Estado do Piauí.
"""

import streamlit as st
import pandas as pd
import polars as pl
import altair as alt
from datetime import datetime
import json
import os

# ==============================================================================
# 1. CONFIGURAÇÕES DA PÁGINA E ESTILIZAÇÃO
# ==============================================================================
st.set_page_config(
    page_title="Painel Arboviroses - Piauí",
    page_icon="🦟",
    layout="wide",
    initial_sidebar_state="expanded"
)

def local_css(file_name):
    """Carrega o arquivo CSS personalizado para injetar estilos no Streamlit."""
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("src/style.css")

def render_kpi_card(label, value, color_class, icon):
    """Renderiza um card de KPI customizado com HTML/CSS."""
    st.markdown(f"""
    <div class="kpi-card {color_class}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-icon">{icon}</div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 2. MAPEAMENTOS E DICIONÁRIOS DE DADOS
# ==============================================================================
@st.cache_data
def load_mappings():
    """Carrega mapeamentos de municípios, regiões e descrições dos códigos SINAM."""
    municipios = {}
    if os.path.exists("municipios_pi.json"):
        with open("municipios_pi.json", "r") as f:
            municipios = json.load(f)
            
    # Mapeamento regional (Macro e Territórios de Desenvolvimento)
    regional = {}
    if os.path.exists("regionalizacao_pi.json"):
        with open("src/regionalizacao_pi.json", "r") as f:
            regional = json.load(f)
    
    # Sexo: De código para descrição amigável
    sexo_map = {'F': 'Feminino', 'M': 'Masculino', 'I': 'Ignorado'}
    
    # Classificação Final: Baseado no dicionário de dados do SINAM
    class_map = {
        '10': 'Dengue', 
        '11': 'Dengue com Sinais de Alarme', 
        '12': 'Dengue Grave', 
        '8': 'Dengue (Provável)',
        '1': 'Chikungunya',
        '2': 'Zika'
    }
    
    # Evolução: Status do desfecho do caso
    evol_map = {'1': 'Cura', '2': 'Óbito por Dengue', '3': 'Óbito por outras causas', '9': 'Ignorado'}
    
    return municipios, regional, sexo_map, class_map, evol_map

municipio_map, regional_map, sexo_map, class_map, evol_map = load_mappings()

# ==============================================================================
# 3. PROCESSAMENTO E CARREGAMENTO DE DADOS
# ==============================================================================
@st.cache_data
def load_data():
    """Lê o arquivo Parquet, filtra para o Piauí e aplica os mapeamentos."""
    df = pl.read_parquet("ingestion/dengue.parquet")
    
    # Limpeza de campos categóricos
    df = df.with_columns([
        pl.col("uf_residencia").cast(pl.Utf8).str.strip_chars(),
        pl.col("municipio_residencia").cast(pl.Utf8).str.strip_chars(),
        pl.col("classificacao_final").cast(pl.Utf8).str.strip_chars(),
        pl.col("evolucao").cast(pl.Utf8).str.strip_chars(),
        pl.col("sexo").cast(pl.Utf8).str.strip_chars()
    ])
    
    # Filtro para o Estado do Piauí (Código IBGE 22)
    df_pi = df.filter(pl.col("uf_residencia") == "22")
    pdf = df_pi.to_pandas()
    pdf['data_notificacao'] = pd.to_datetime(pdf['data_notificacao'], errors='coerce')
    
    # Cálculo da Semana Epidemiológica (Padrão ISO-8601)
    pdf['semana_epi'] = pdf['data_notificacao'].apply(
        lambda x: f"{x.isocalendar()[0]}-SE{x.isocalendar()[1]:02d}" if pd.notnull(x) else "N/I"
    )
    
    def get_regional_info(code, key):
        """Busca informações de municipalidade e regionalização no JSON auxiliar."""
        info = regional_map.get(str(code), {})
        return info.get(key, "Não Informado")
    
    # Aplicação dos mapeamentos para gerar colunas legíveis
    pdf['municipio_nome'] = pdf['municipio_residencia'].apply(lambda x: get_regional_info(x, "nome"))
    pdf['macrorregiao'] = pdf['municipio_residencia'].apply(lambda x: get_regional_info(x, "macrorregiao"))
    pdf['territorio'] = pdf['municipio_residencia'].apply(lambda x: get_regional_info(x, "territorio"))
    
    pdf['sexo_desc'] = pdf['sexo'].map(sexo_map).fillna("Ignorado")
    pdf['classificacao_desc'] = pdf['classificacao_final'].map(class_map).fillna("Outros/Em Investigação")
    pdf['evolucao_desc'] = pdf['evolucao'].map(evol_map).fillna("Em Investigação")
    
    return pdf

# Carregamento inicial do dataset completo
df_full = load_data()

# ==============================================================================
# 4. BARRA LATERAL (SIDEBAR) - FILTROS HIERÁRQUICOS
# ==============================================================================
with st.sidebar:
    # Logotipo Institucional
    st.image("src/sesapi_logo.png", width=250)
    
    st.markdown("---")
    st.markdown("### 🔍 Filtros de Análise")
    
    # Filtro de Macrorregião de Saúde
    macro_list = ["Todas"] + sorted(list(df_full['macrorregiao'].unique()))
    selected_macro = st.selectbox("Macrorregião de Saúde", macro_list)
    
    # Filtro de Território de Desenvolvimento (Dependente da Macro selecionada)
    if selected_macro != "Todas":
        terr_options = sorted(list(df_full[df_full['macrorregiao'] == selected_macro]['territorio'].unique()))
    else:
        terr_options = sorted(list(df_full['territorio'].unique()))
    
    territory_list = ["Todos"] + terr_options
    selected_territory = st.selectbox("Território de Desenvolvimento", territory_list)
    
    # Filtro de Município (Dependente do Território ou Macro selecionada)
    if selected_territory != "Todos":
        mun_options = sorted(list(df_full[df_full['territorio'] == selected_territory]['municipio_nome'].unique()))
    elif selected_macro != "Todas":
        mun_options = sorted(list(df_full[df_full['macrorregiao'] == selected_macro]['municipio_nome'].unique()))
    else:
        mun_options = sorted(list(df_full['municipio_nome'].unique()))
        
    municipality_list = ["Todos"] + mun_options
    selected_municipality = st.selectbox("Município", municipality_list)
    
    # Filtro de Data (Período de Notificação)
    dates = df_full['data_notificacao'].dropna()
    if not dates.empty:
        min_date = dates.min().date()
        max_date = dates.max().date()
        date_range = st.date_input("Período de Notificação", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    else:
        st.warning("Dados de data não disponíveis.")
        date_range = []

# Aplicação dinâmica dos filtros no dataframe
df = df_full.copy()
if selected_macro != "Todas":
    df = df[df['macrorregiao'] == selected_macro]
if selected_territory != "Todos":
    df = df[df['territorio'] == selected_territory]
if selected_municipality != "Todos":
    df = df[df['municipio_nome'] == selected_municipality]

if len(date_range) == 2:
    start_date, end_date = date_range
    df = df[(df['data_notificacao'].dt.date >= start_date) & (df['data_notificacao'].dt.date <= end_date)]

# ==============================================================================
# 5. CONTEÚDO PRINCIPAL - MÉTRICAS CHAVE (KPIs)
# ==============================================================================
st.title("Painel Arboviroses - Piauí")
st.markdown(f"**Vigilância Epidemiológica | Monitoramento de casos de dengue**")
st.divider()

col1, col2, col3, col4 = st.columns(4)
with col1:
    render_kpi_card("Total Notificações", f"{len(df):,}".replace(",", "."), "kpi-blue", "📈")
with col2:
    confirmed = len(df[df['classificacao_desc'].str.contains('Dengue')])
    render_kpi_card("Casos Confirmados", f"{confirmed:,}".replace(",", "."), "kpi-yellow", "✅")
with col3:
    deaths = len(df[df['evolucao_desc'] == 'Óbito por Dengue'])
    render_kpi_card("Óbitos por Dengue", deaths, "kpi-red", "💀")
with col4:
    grave = len(df[df['classificacao_desc'] == 'Dengue Grave'])
    render_kpi_card("Casos Graves", grave, "kpi-green", "🚨")

st.write("---")

# ==============================================================================
# 6. VISUALIZAÇÕES - LINHA 1 (TENDÊNCIA E REGIONAL)
# ==============================================================================
v_col1, v_col2 = st.columns([2, 1])

# Bloco de Tendência Temporal com abas para Diário/Semana Epi
with v_col1:
    with st.container(border=True):
        st.subheader("📈 Tendência Temporal")
        tab_dia, tab_se = st.tabs(["Diário", "Semana Epidemiológica"])
        
        df_clean_trend = df.dropna(subset=['data_notificacao'])
        
        with tab_dia:
            if not df_clean_trend.empty:
                df_trend = df_clean_trend.groupby('data_notificacao').size().reset_index(name='Casos')
                base_trend = alt.Chart(df_trend).mark_line(color='#28a745', strokeWidth=3, point=True).encode(
                    x=alt.X('data_notificacao:T', title='Data de Notificação'),
                    y=alt.Y('Casos:Q', title='Número de Casos'),
                    tooltip=['data_notificacao', 'Casos']
                )
                text_trend = base_trend.mark_text(dy=-15, fontWeight='bold', color='#1e7e34').encode(
                    text='Casos:Q'
                )
                st.altair_chart((base_trend + text_trend).properties(height=320).interactive(), use_container_width=True)
            else:
                st.info("Dados temporais não disponíveis para o período.")
                
        with tab_se:
            if not df_clean_trend.empty:
                df_se = df_clean_trend.groupby('semana_epi').size().reset_index(name='Casos')
                base_se = alt.Chart(df_se).mark_line(color='#ffcc00', strokeWidth=3, point=True).encode(
                    x=alt.X('semana_epi:N', title='Semana Epidemiológica', sort=None),
                    y=alt.Y('Casos:Q', title='Número de Casos'),
                    tooltip=['semana_epi', 'Casos']
                )
                text_se = base_se.mark_text(dy=-15, fontWeight='bold', color='#b8860b').encode(
                    text='Casos:Q'
                )
                st.altair_chart((base_se + text_se).properties(height=320).interactive(), use_container_width=True)
            else:
                st.info("Dados por SE não disponíveis.")

# Distribuição por Macrorregião de Saúde
with v_col2:
    with st.container(border=True):
        st.subheader("🌐 Visão por Macrorregiões")
        df_macro = df['macrorregiao'].value_counts().reset_index()
        df_macro.columns = ['Macro', 'Total']
        base_macro = alt.Chart(df_macro).mark_bar(color='#28a745').encode(
            x=alt.X('Total:Q', title='Notificações'),
            y=alt.Y('Macro:N', sort='-x', title=None),
            tooltip=['Macro', 'Total']
        )
        text_macro = base_macro.mark_text(align='left', dx=5, fontWeight='bold').encode(
            text='Total:Q'
        )
        st.altair_chart((base_macro + text_macro).properties(height=320), use_container_width=True, height=390)

# ==============================================================================
# 7. VISUALIZAÇÕES - LINHA 2 (TERRITÓRIOS, SEXO E PERFIS CLÍNICOS)
# ==============================================================================
v_col3, v_col4, v_col5 = st.columns([1, 1, 1])

# Distribuição por Território de Desenvolvimento
with v_col3:
    with st.container(border=True):
        st.subheader("🗺️ Territórios de Desenvolvimento")
        df_terr = df['territorio'].value_counts().reset_index()
        df_terr.columns = ['Território', 'Total']
        base_terr = alt.Chart(df_terr).mark_bar(color='#0056b3').encode(
            x=alt.X('Total:Q', title='Notificações'),
            y=alt.Y('Território:N', sort='-x', title=None),
            tooltip=['Território', 'Total']
        )
        text_terr = base_terr.mark_text(align='left', dx=5, fontWeight='bold').encode(
            text='Total:Q'
        )
        st.altair_chart((base_terr + text_terr).properties(height=320), use_container_width=True, height=385)

# Distribuição por Sexo
with v_col4:
    with st.container(border=True):
        st.subheader("👥 Distribuição por Sexo")
        df_sex = df['sexo_desc'].value_counts().reset_index()
        df_sex.columns = ['Sexo', 'Total']
        base_sex = alt.Chart(df_sex).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Total", type="quantitative"),
            color=alt.Color(field="Sexo", type="nominal", scale=alt.Scale(range=['#0056b3', '#ffcc00', '#28a745'])),
            tooltip=['Sexo', 'Total']
        )
        text_sex = base_sex.mark_text(radiusOffset=20, fontWeight='bold').encode(
            text='Total:Q'
        )
        st.altair_chart((base_sex + text_sex).properties(height=375), use_container_width=True)

# Perfis Clínicos (Abas: Evolução e Classificação)
with v_col5:
    with st.container(border=True):
        st.subheader("📋 Evolução e Classificação")
        tab_evol, tab_class = st.tabs(["Evolução", "Classificação"])
        with tab_evol:
            df_evol = df['evolucao_desc'].value_counts().reset_index()
            df_evol.columns = ['Evolução', 'Total']
            base_evol = alt.Chart(df_evol).mark_bar(color='#dc3545').encode(
                x=alt.X('Total:Q'),
                y=alt.Y('Evolução:N', sort='-x'),
                tooltip=['Evolução', 'Total']
            )
            text_evol = base_evol.mark_text(align='left', dx=5, fontWeight='bold').encode(
                text='Total:Q'
            )
            st.altair_chart((base_evol + text_evol).properties(height=320), use_container_width=True)
        with tab_class:
            df_class = df['classificacao_desc'].value_counts().reset_index()
            df_class.columns = ['Classificação', 'Total']
            base_class = alt.Chart(df_class).mark_bar(color='#ffcc00').encode(
                x=alt.X('Total:Q'),
                y=alt.Y('Classificação:N', sort='-x'),
                tooltip=['Classificação', 'Total']
            )
            text_class = base_class.mark_text(align='left', dx=5, fontWeight='bold').encode(
                text='Total:Q'
            )
            st.altair_chart((base_class + text_class).properties(height=320), use_container_width=True)

# ==============================================================================
# 8. VISUALIZAÇÕES - LINHA 3 (RANKING MUNICIPAL)
# ==============================================================================
with st.container(border=True):
    st.subheader("📍 Ranking por Município")
    df_mun = df['municipio_nome'].value_counts().head(15).reset_index()
    df_mun.columns = ['Município', 'Total']
    base_mun = alt.Chart(df_mun).mark_bar(color='#0056b3').encode(
        x=alt.X('Município:N', sort='-y', title=None, axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('Total:Q', title='Casos'),
        tooltip=['Município', 'Total']
    )
    text_mun = base_mun.mark_text(align='center', dy=-10, fontWeight='bold').encode(
        text='Total:Q'
    )
    st.altair_chart((base_mun + text_mun).properties(height=320), use_container_width=True)

# ==============================================================================
# 9. RODAPÉ INSTITUCIONAL
# ==============================================================================
st.write("---")
st.markdown(f"""
<div style='text-align: center; color: #666; font-size: 0.8rem;'>
    Painel de Monitoramento Arboviroses Piauí | Fonte: SINAM/SUS | © {datetime.now().year} Governo do Piauí <br> 
    Secretaria de Estado da Saúde - Vigilância Epidemiológica | Desenvolvido por Lucas Pablo
</div>
""", unsafe_allow_html=True)
