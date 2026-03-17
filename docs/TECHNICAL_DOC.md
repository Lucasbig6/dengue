# Documentação Técnica - Painel Arboviroses Piauí

Este documento fornece uma visão geral técnica do desenvolvimento, estrutura e manutenção do Dashboard de Arboviroses do Estado do Piauí.

## 📋 Visão Geral
O dashboard é uma aplicação analítica desenvolvida em Python utilizando **Streamlit**, projetada para monitorar casos de dengue e outras arboviroses no Piauí. Os dados são processados a partir de arquivos Parquet do SINAM e visualizados através da biblioteca **Altair**.

## 🏗️ Estrutura do Projeto

- `src/dashboard.py`: Script principal contendo a lógica de processamento de dados e interface Streamlit.
- `src/style.css`: Estilização personalizada seguindo a identidade visual do Governo do Piauí.
- `src/regionalizacao_pi.json`: Mapeamento de municípios para Macrorregiões e Territórios de Desenvolvimento.
- `src/municipios_pi.json`: Dicionário de códigos IBGE para nomes de municípios.
- `src/assets/logo_sesapi.png`: Logotipo oficial utilizado na barra lateral.

## 🛠️ Componentes Principais

### 1. Processamento de Dados (`load_data`)
- Filtragem por UF (Piauí - 22).
- Mapeamento de descrições para códigos (Sexo, Classificação, Evolução).
- Cálculo da **Semana Epidemiológica (SE)** no padrão ISO.
- Enriquecimento regional (Macro e Territórios).

### 2. Interface de Usuário (Layout)
- **Barra Lateral**: Filtros hierárquicos (Macro -> Território -> Município) e filtros de data.
- **KPIs**: Cards métricos com bordas coloridas dinâmicas via CSS.
- **Gráficos**:
    - Tendência Temporal (Diário vs. SE).
    - Distribuição Regional (Macro e Território).
    - Perfis Epidemiológicos (Sexo, Evolução, Classificação).
    - Ranking de Municípios.

## 🎨 Design e UI
O design utiliza **Technical Brutalism** adaptado para uma identidade institucional premium:
- **Cores**: Azul (#0056b3), Amarelo (#ffcc00), Verde (#28a745), Vermelho (#dc3545).
- **Alinhamento**: Estratégia de Flexbox CSS aplicada para garantir que todos os containers em uma linha tenham a mesma altura.
- **Interatividade**: Gráficos responsivos com tooltips detalhados.

## 🔧 Manutenção
Para adicionar novos filtros ou gráficos:
1. Atualize a função `load_data` se novos campos forem necessários.
2. Adicione o widget na `sidebar` se for um filtro global.
3. Crie o novo gráfico Altair seguindo o padrão de altura (`height=320`).
4. Envolva em um `st.container(border=True)` para manter a consistência visual.

---
*Desenvolvido para a Secretaria de Estado da Saúde do Piauí (SESAPI).*
