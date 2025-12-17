import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np


st.set_page_config(
    page_title="Super-Dashboard Integrado",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        background-color: #2b2b2b;
    }
    .stApp {
        background-color: #2b2b2b;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff;
    }
    [data-testid="stMetricLabel"] {
        color: #e0e0e0;
    }
    .stMarkdown {
        color: #e0e0e0;
    }
    h1, h2, h4, h5, h6 {
        color: #4da6ff !important;
    }
    h3{
        color: #69C6DB !important;
    }
    .stSelectbox label, .stMultiSelect label, .stDateInput label {
        color: #e0e0e0 !important;
    }
    [data-baseweb="select"] {
        background-color: #3b3b3b;
    }
    .stAlert {
        background-color: #3b3b3b;
        color: #ffffff;
    }
    div[data-testid="stExpander"] {
        background-color: #3b3b3b;
        border: 1px solid #4da6ff;
    }
    div[data-testid="stExpander"] summary {
        color: #4da6ff !important;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def carregar_dados():
    df_estoque = pd.read_csv('FCD_estoque.csv', sep=';', encoding='utf-8')
    df_vendas = pd.read_csv('FCD_vendas.csv', sep=';', encoding='utf-8')
    df_compras = pd.read_csv('FCD_compras.csv', sep=';', encoding='utf-8')
    df_produtos = pd.read_csv('FCD_produtos.csv', sep=';', encoding='utf-8')
    
    df_estoque['data_referencia'] = pd.to_datetime(df_estoque['data_referencia'])
    df_vendas['data_venda'] = pd.to_datetime(df_vendas['data_venda'], format='%d/%m/%Y')
    df_compras['data_compra'] = pd.to_datetime(df_compras['data_compra'], format='%d/%m/%Y')
    
    df_produtos = df_produtos.rename(columns={
        'produto_nome': 'nome_produto',
        'preco_unitario': 'valor_unitario_estoque'
    })
    
    df_produtos = df_produtos[['produto_id', 'nome_produto', 'categoria', 'valor_unitario_estoque']]
    
    return df_estoque, df_vendas, df_compras, df_produtos

df_estoque, df_vendas, df_compras, df_produtos = carregar_dados()


idx = df_estoque.groupby(["produto_id", "localizacao"])["data_referencia"].idxmax()
df_estoque = df_estoque.loc[idx]

df_estoque = df_estoque.merge(df_produtos, on='produto_id', how='left')
df_vendas = df_vendas.merge(df_produtos, on='produto_id', how='left')
df_compras = df_compras.merge(df_produtos, on='produto_id', how='left')

df_estoque['valor_total_estoque'] = df_estoque['quantidade_estoque'] * df_estoque['valor_unitario_estoque']


st.markdown("<h1 style='text-align: center;'>Super-Dashboard Integrado</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #b3b3b3;'>Estoque • Vendas • Compras</h3>", unsafe_allow_html=True)
st.markdown("---")


st.sidebar.markdown("## Filtros")

categorias_disponiveis = sorted(df_produtos['categoria'].unique().tolist())
categorias_selecionadas = st.sidebar.multiselect('Categoria', categorias_disponiveis, default=categorias_disponiveis)

if len(categorias_selecionadas) > 0:
    produtos_filtrados = df_produtos[df_produtos['categoria'].isin(categorias_selecionadas)]
else:
    produtos_filtrados = df_produtos


produtos_disponiveis = sorted(produtos_filtrados['nome_produto'].tolist())
if len(produtos_disponiveis) > 0:
    produtos_selecionados = st.sidebar.multiselect(
        'Produto', 
        produtos_disponiveis, 
        default=[],  
        help=f"Deixe vazio para incluir todos. {len(produtos_disponiveis)} produtos disponíveis"
    )

    if len(produtos_selecionados) == 0:
        st.sidebar.caption(f"✓ Todos os {len(produtos_disponiveis)} produtos selecionados")
        produtos_selecionados = produtos_disponiveis 
    else:
        st.sidebar.caption(f"{len(produtos_selecionados)} de {len(produtos_disponiveis)} produtos selecionados")
else:
    produtos_selecionados = []



loja_nomes = {1: 'Loja 1', 2: 'Loja 2', 3: 'Depósito Central'}
lojas_ids = sorted(df_vendas['loja_id'].unique().tolist())
lojas_disponiveis = [loja_nomes.get(loja_id, f'Loja {loja_id}') for loja_id in lojas_ids]
lojas_selecionadas_nomes = st.sidebar.multiselect('Loja', lojas_disponiveis, default=lojas_disponiveis)

loja_nomes_invertido = {v: k for k, v in loja_nomes.items()}
lojas_selecionadas = [loja_nomes_invertido[nome] for nome in lojas_selecionadas_nomes]


st.sidebar.markdown("### Período")
data_min = df_vendas['data_venda'].min()
data_max = df_vendas['data_venda'].max()

col1, col2 = st.sidebar.columns(2)
with col1:
    data_inicio = st.date_input('De', data_min, min_value=data_min, max_value=data_max)
with col2:
    data_fim = st.date_input('Até', data_max, min_value=data_min, max_value=data_max)


df_estoque_filtrado = df_estoque.copy()
df_vendas_filtrado = df_vendas.copy()
df_compras_filtrado = df_compras.copy()

if len(categorias_selecionadas) > 0:
    df_estoque_filtrado = df_estoque_filtrado[df_estoque_filtrado['categoria'].isin(categorias_selecionadas)]
    df_vendas_filtrado = df_vendas_filtrado[df_vendas_filtrado['categoria'].isin(categorias_selecionadas)]
    df_compras_filtrado = df_compras_filtrado[df_compras_filtrado['categoria'].isin(categorias_selecionadas)]

if len(produtos_selecionados) > 0:
    produtos_ids = df_produtos[df_produtos['nome_produto'].isin(produtos_selecionados)]['produto_id'].values
    df_estoque_filtrado = df_estoque_filtrado[df_estoque_filtrado['produto_id'].isin(produtos_ids)]
    df_vendas_filtrado = df_vendas_filtrado[df_vendas_filtrado['produto_id'].isin(produtos_ids)]
    df_compras_filtrado = df_compras_filtrado[df_compras_filtrado['produto_id'].isin(produtos_ids)]

if len(lojas_selecionadas) > 0:
    df_vendas_filtrado = df_vendas_filtrado[df_vendas_filtrado['loja_id'].isin(lojas_selecionadas)]

df_vendas_filtrado = df_vendas_filtrado[
    (df_vendas_filtrado['data_venda'] >= pd.to_datetime(data_inicio)) &
    (df_vendas_filtrado['data_venda'] <= pd.to_datetime(data_fim))
]

df_compras_filtrado = df_compras_filtrado[
    (df_compras_filtrado['data_compra'] >= pd.to_datetime(data_inicio)) &
    (df_compras_filtrado['data_compra'] <= pd.to_datetime(data_fim))
]


st.markdown("### Indicadores Principais")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    receita_total = df_vendas_filtrado['valor_total'].sum()
    st.metric("$ Receita Total", f"R$ {receita_total:,.2f}")

with col2:
    valor_estoque = df_estoque_filtrado['valor_total_estoque'].sum()
    st.metric("Valor do Estoque", f"R$ {valor_estoque:,.2f}")

with col3:
    gasto_compras = df_compras_filtrado['valor_total'].sum()
    st.metric("Gasto em Compras", f"R$ {gasto_compras:,.2f}")

with col4:
   
    estoque_por_produto = df_estoque_filtrado.groupby('produto_id').agg({
        'quantidade_estoque': 'sum',
        'estoque_minimo': 'sum'  
    }).reset_index()
    produtos_criticos = len(estoque_por_produto[estoque_por_produto['quantidade_estoque'] < estoque_por_produto['estoque_minimo']])
    st.metric("Produtos Críticos", produtos_criticos)

with col5:
    compras_entregues = df_compras_filtrado[df_compras_filtrado['status_compra'] == 'Entregue']
    if len(compras_entregues) > 0:
        prazo_medio = compras_entregues['prazo_entrega_dias'].mean()
        st.metric("Prazo Médio de Reposição", f"{prazo_medio:.1f} dias")
    else:
        st.metric("Prazo Médio de Reposição", "N/A")

st.markdown("---")

if len(produtos_selecionados) == 1:
    st.markdown("### Visão 360° do Produto")
elif len(produtos_selecionados) == 0 or len(produtos_selecionados) > 1:
    st.info("**Dica:** Selecione somente 1 produto no filtro na barra lateral   para visualizar a **Visão 360° do Produto** com detalhes completos.")
    st.markdown("---")

if len(produtos_selecionados) == 1:
    
    produto_id_sel = df_produtos[df_produtos['nome_produto'] == produtos_selecionados[0]]['produto_id'].values[0]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("Estoque")
        estoque_atual = df_estoque_filtrado['quantidade_estoque'].sum()
        estoque_minimo = df_estoque_filtrado['estoque_minimo'].mean()
        
        if estoque_atual < estoque_minimo:
            st.error(f"ALERTA: Estoque abaixo do mínimo!")
            st.metric("Estoque Atual", f"{estoque_atual:.0f} un")
            st.metric("Estoque Mínimo", f"{estoque_minimo:.0f} un")
        elif estoque_atual > estoque_minimo * 3:
            st.warning(f"Possível excesso de estoque")
            st.metric("Estoque Atual", f"{estoque_atual:.0f} un")
            st.metric("Estoque Mínimo", f"{estoque_minimo:.0f} un")
        else:
            st.success(f"✓ Estoque adequado")
            st.metric("Estoque Atual", f"{estoque_atual:.0f} un")
            st.metric("Estoque Mínimo", f"{estoque_minimo:.0f} un")
    
    with col2:
        st.markdown("Vendas")
        vendas_quantidade = df_vendas_filtrado['quantidade_vendida'].sum()
        vendas_valor = df_vendas_filtrado['valor_total'].sum()
        st.metric("Quantidade Vendida", f"{vendas_quantidade:.0f} un")
        st.metric("Receita Gerada", f"R$ {vendas_valor:,.2f}")
    
    with col3:
        st.markdown("Compras")
        compras_quantidade = df_compras_filtrado[df_compras_filtrado['status_compra'] == 'Entregue']['quantidade_comprada'].sum()
        compras_valor = df_compras_filtrado[df_compras_filtrado['status_compra'] == 'Entregue']['valor_total'].sum()
        
        if len(df_compras_filtrado) > 0:
            fornecedor_principal = df_compras_filtrado.groupby('fornecedor')['valor_total'].sum().idxmax()
            st.metric("Quantidade Comprada", f"{compras_quantidade:.0f} un")
            st.metric("Valor Investido", f"R$ {compras_valor:,.2f}")
            st.info(f"Fornecedor Principal: **{fornecedor_principal}**")
        else:
            st.metric("Quantidade Comprada", "0 un")
            st.metric("Valor Investido", "R$ 0,00")
    
    st.markdown("---")


st.markdown("### Indicadores Estratégicos")

tab1, tab2, tab3, tab4 = st.tabs(["Produtos Críticos", "Top 10 Vendas", "Maiores Gastos", "Fornecedores"])

with tab1:
    st.markdown("Produtos com Estoque Crítico (Abaixo do Mínimo)")
    
   
    estoque_agrupado = df_estoque_filtrado.groupby(['produto_id', 'nome_produto', 'categoria']).agg({
        'quantidade_estoque': 'sum',
        'estoque_minimo': 'sum'
    }).reset_index()
    
    df_criticos = estoque_agrupado[estoque_agrupado['quantidade_estoque'] < estoque_agrupado['estoque_minimo']].copy()
    df_criticos['deficit'] = df_criticos['estoque_minimo'] - df_criticos['quantidade_estoque']
    df_criticos = df_criticos.sort_values('deficit', ascending=False)
    
    if len(df_criticos) > 0:
        df_criticos_display = df_criticos[['nome_produto', 'categoria', 'quantidade_estoque', 'estoque_minimo', 'deficit']].head(20)
        df_criticos_display.columns = ['Produto', 'Categoria', 'Estoque Total', 'Estoque Mínimo', 'Déficit']
        
        st.dataframe(
            df_criticos_display,
            use_container_width=True,
            hide_index=True
        )
        
        fig = px.bar(
            df_criticos.head(10),
            x='nome_produto',
            y='deficit',
            title='Top 10 Produtos com Maior Déficit de Estoque',
            labels={'nome_produto': 'Produto', 'deficit': 'Déficit (unidades)'},
            color='deficit',
            color_continuous_scale=['#ff6b6b', '#ff0000']
        )
        fig.update_layout(
            plot_bgcolor='#2b2b2b',
            paper_bgcolor='#2b2b2b',
            font_color='#e0e0e0',
            title_font_color='#4da6ff',
            xaxis_title_font_color='#4da6ff',
            yaxis_title_font_color='#4da6ff'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("Nenhum produto com estoque crítico no momento!")

with tab2:
    st.markdown("Top 10 Produtos Mais Vendidos")
    
    top_vendas = df_vendas_filtrado.groupby(['produto_id', 'nome_produto', 'categoria']).agg({
        'quantidade_vendida': 'sum',
        'valor_total': 'sum'
    }).reset_index().sort_values('quantidade_vendida', ascending=False).head(10)
    
    if len(top_vendas) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                top_vendas,
                x='nome_produto',
                y='quantidade_vendida',
                title='Quantidade Vendida',
                labels={'nome_produto': 'Produto', 'quantidade_vendida': 'Quantidade'},
                color='quantidade_vendida',
                color_continuous_scale='Blues'
            )
            fig.update_layout(
                plot_bgcolor='#2b2b2b',
                paper_bgcolor='#2b2b2b',
                font_color='#e0e0e0',
                title_font_color='#4da6ff',
                xaxis_title_font_color='#4da6ff',
                yaxis_title_font_color='#4da6ff'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                top_vendas,
                x='nome_produto',
                y='valor_total',
                title='Receita Gerada',
                labels={'nome_produto': 'Produto', 'valor_total': 'Receita (R$)'},
                color='valor_total',
                color_continuous_scale='Blues'
            )
            fig.update_layout(
                plot_bgcolor='#2b2b2b',
                paper_bgcolor='#2b2b2b',
                font_color='#e0e0e0',
                title_font_color='#4da6ff',
                xaxis_title_font_color='#4da6ff',
                yaxis_title_font_color='#4da6ff'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        top_vendas_display = top_vendas[['nome_produto', 'categoria', 'quantidade_vendida', 'valor_total']].copy()
        top_vendas_display.columns = ['Produto', 'Categoria', 'Quantidade Vendida', 'Receita Total (R$)']
        st.dataframe(top_vendas_display, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma venda encontrada no período selecionado.")

with tab3:
    st.markdown("Produtos com Maior Gasto em Compras")
    
    maiores_gastos = df_compras_filtrado[df_compras_filtrado['status_compra'] == 'Entregue'].groupby(['produto_id', 'nome_produto', 'categoria']).agg({
        'valor_total': 'sum',
        'quantidade_comprada': 'sum'
    }).reset_index().sort_values('valor_total', ascending=False).head(10)
    
    if len(maiores_gastos) > 0:
        fig = px.bar(
            maiores_gastos,
            x='nome_produto',
            y='valor_total',
            title='Top 10 Produtos com Maior Investimento em Compras',
            labels={'nome_produto': 'Produto', 'valor_total': 'Valor Investido (R$)'},
            color='valor_total',
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            plot_bgcolor='#2b2b2b',
            paper_bgcolor='#2b2b2b',
            font_color='#e0e0e0',
            title_font_color='#4da6ff',
            xaxis_title_font_color='#4da6ff',
            yaxis_title_font_color='#4da6ff'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        maiores_gastos_display = maiores_gastos[['nome_produto', 'categoria', 'quantidade_comprada', 'valor_total']].copy()
        maiores_gastos_display.columns = ['Produto', 'Categoria', 'Quantidade Comprada', 'Valor Total (R$)']
        st.dataframe(maiores_gastos_display, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma compra entregue encontrada no período selecionado.")

with tab4:
    st.markdown("Análise de Fornecedores")
    
    if len(df_compras_filtrado) > 0:
        analise_fornecedores = df_compras_filtrado[df_compras_filtrado['status_compra'] == 'Entregue'].groupby('fornecedor').agg({
            'valor_unitario': 'mean',
            'prazo_entrega_dias': 'mean',
            'quantidade_comprada': 'sum',
            'valor_total': 'sum'
        }).reset_index()
        
        analise_fornecedores.columns = ['Fornecedor', 'Preço Médio', 'Prazo Médio (dias)', 'Volume Total', 'Gasto Total']
        analise_fornecedores = analise_fornecedores.sort_values('Gasto Total', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                analise_fornecedores.head(10),
                x='Fornecedor',
                y='Preço Médio',
                title='Preço Médio por Fornecedor',
                labels={'Preço Médio': 'Preço Médio (R$)'},
                color='Preço Médio',
                color_continuous_scale='Blues'
            )
            fig.update_layout(
                plot_bgcolor='#2b2b2b',
                paper_bgcolor='#2b2b2b',
                font_color='#e0e0e0',
                title_font_color='#4da6ff',
                xaxis_title_font_color='#4da6ff',
                yaxis_title_font_color='#4da6ff'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                analise_fornecedores.head(10),
                x='Fornecedor',
                y='Prazo Médio (dias)',
                title='Prazo Médio de Entrega por Fornecedor',
                labels={'Prazo Médio (dias)': 'Dias'},
                color='Prazo Médio (dias)',
                color_continuous_scale='Reds'
            )
            fig.update_layout(
                plot_bgcolor='#2b2b2b',
                paper_bgcolor='#2b2b2b',
                font_color='#e0e0e0',
                title_font_color='#4da6ff',
                xaxis_title_font_color='#4da6ff',
                yaxis_title_font_color='#4da6ff'
            )
            st.plotly_chart(fig, use_container_width=True)
    
        fig = px.scatter(
            analise_fornecedores.head(15),
            x='Prazo Médio (dias)',
            y='Preço Médio',
            size='Volume Total',
            color='Gasto Total',
            hover_name='Fornecedor',
            title='Matriz de Análise de Fornecedores',
            labels={'Prazo Médio (dias)': 'Prazo Médio (dias)', 'Preço Médio': 'Preço Médio (R$)'},
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            plot_bgcolor='#2b2b2b',
            paper_bgcolor='#2b2b2b',
            font_color='#e0e0e0',
            title_font_color='#4da6ff',
            xaxis_title_font_color='#4da6ff',
            yaxis_title_font_color='#4da6ff'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(analise_fornecedores, use_container_width=True, hide_index=True)
        
        prazo_medio_geral = analise_fornecedores['Prazo Médio (dias)'].mean()
        st.info(f"● Tempo Médio de Reposição: **{prazo_medio_geral:.1f} dias**")
    else:
        st.info("Nenhuma compra encontrada no período selecionado.")

st.markdown("---")

st.markdown("### Análises Avançadas")

tab1, tab2, tab3 = st.tabs(["Série Temporal", "Estoque vs Vendas vs Compras", "Análise por Loja"])

with tab1:
    st.markdown("Vendas vs Compras ao Longo do Tempo")
    
    df_vendas_mes = df_vendas_filtrado.copy()
    df_vendas_mes['mes'] = df_vendas_mes['data_venda'].dt.to_period('M').dt.to_timestamp()
    vendas_mes = df_vendas_mes.groupby('mes')['quantidade_vendida'].sum().reset_index()
    vendas_mes.columns = ['mes', 'quantidade']
    
    df_compras_mes = df_compras_filtrado[df_compras_filtrado['status_compra'] == 'Entregue'].copy()
    df_compras_mes['mes'] = df_compras_mes['data_compra'].dt.to_period('M').dt.to_timestamp()
    compras_mes = df_compras_mes.groupby('mes')['quantidade_comprada'].sum().reset_index()
    compras_mes.columns = ['mes', 'quantidade']
    
    if len(vendas_mes) > 0 or len(compras_mes) > 0:
        fig = go.Figure()
        
        if len(vendas_mes) > 0:
            fig.add_trace(go.Scatter(
                x=vendas_mes['mes'],
                y=vendas_mes['quantidade'],
                mode='lines+markers',
                name='Vendas',
                line=dict(color='#4da6ff', width=3),
                marker=dict(size=8)
            ))
        
        if len(compras_mes) > 0:
            fig.add_trace(go.Scatter(
                x=compras_mes['mes'],
                y=compras_mes['quantidade'],
                mode='lines+markers',
                name='Compras',
                line=dict(color='#ff6b6b', width=3),
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            title='Evolução Mensal: Vendas vs Compras',
            xaxis_title='Mês',
            yaxis_title='Quantidade',
            plot_bgcolor='#2b2b2b',
            paper_bgcolor='#2b2b2b',
            font_color='#e0e0e0',
            title_font_color='#4da6ff',
            xaxis_title_font_color='#4da6ff',
            yaxis_title_font_color='#4da6ff',
            legend=dict(font=dict(color='#e0e0e0'))
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Dados insuficientes para gerar o gráfico de série temporal.")

with tab2:
    st.markdown("Relação Estoque × Vendas × Compras por Produto")
    
    estoque_produto = df_estoque_filtrado.groupby(['produto_id', 'nome_produto'])['quantidade_estoque'].sum().reset_index()
    vendas_produto = df_vendas_filtrado.groupby('produto_id')['quantidade_vendida'].sum().reset_index()
    compras_produto = df_compras_filtrado[df_compras_filtrado['status_compra'] == 'Entregue'].groupby('produto_id')['quantidade_comprada'].sum().reset_index()
    
    analise_consolidada = estoque_produto.merge(vendas_produto, on='produto_id', how='left')
    analise_consolidada = analise_consolidada.merge(compras_produto, on='produto_id', how='left')
    analise_consolidada.fillna(0, inplace=True)
    
    analise_consolidada = analise_consolidada.sort_values('quantidade_vendida', ascending=False).head(20)
    
    if len(analise_consolidada) > 0:
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=analise_consolidada['nome_produto'],
            y=analise_consolidada['quantidade_estoque'],
            name='Estoque',
            marker_color='#4da6ff'
        ))
        
        fig.add_trace(go.Bar(
            x=analise_consolidada['nome_produto'],
            y=analise_consolidada['quantidade_vendida'],
            name='Vendas',
            marker_color='#66ff66'
        ))
        
        fig.add_trace(go.Bar(
            x=analise_consolidada['nome_produto'],
            y=analise_consolidada['quantidade_comprada'],
            name='Compras',
            marker_color='#ff6b6b'
        ))
        
        fig.update_layout(
            title='Top 20 Produtos: Estoque × Vendas × Compras',
            xaxis_title='Produto',
            yaxis_title='Quantidade',
            barmode='group',
            plot_bgcolor='#2b2b2b',
            paper_bgcolor='#2b2b2b',
            font_color='#e0e0e0',
            title_font_color='#4da6ff',
            xaxis_title_font_color='#4da6ff',
            yaxis_title_font_color='#4da6ff',
            legend=dict(font=dict(color='#e0e0e0'))
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Dados insuficientes para análise consolidada.")

with tab3:
    st.markdown("Análise de Vendas por Loja")
    
    if len(lojas_selecionadas) > 1:
        vendas_loja = df_vendas_filtrado.groupby('loja_id').agg({
            'valor_total': 'sum',
            'quantidade_vendida': 'sum',
            'venda_id': 'count'
        }).reset_index()
        vendas_loja.columns = ['Loja', 'Receita Total', 'Quantidade Vendida', 'Número de Vendas']
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                vendas_loja,
                values='Receita Total',
                names='Loja',
                title='Distribuição de Receita por Loja',
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            fig.update_layout(
                plot_bgcolor='#2b2b2b',
                paper_bgcolor='#2b2b2b',
                font_color='#e0e0e0',
                title_font_color='#4da6ff'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                vendas_loja,
                x='Loja',
                y='Quantidade Vendida',
                title='Quantidade Vendida por Loja',
                color='Quantidade Vendida',
                color_continuous_scale='Blues'
            )
            fig.update_layout(
                plot_bgcolor='#2b2b2b',
                paper_bgcolor='#2b2b2b',
                font_color='#e0e0e0',
                title_font_color='#4da6ff',
                xaxis_title_font_color='#4da6ff',
                yaxis_title_font_color='#4da6ff'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(vendas_loja, use_container_width=True, hide_index=True)
    elif len(lojas_selecionadas) == 1:
        st.info(f"Visualizando dados apenas da Loja {lojas_selecionadas[0]}. Selecione múltiplas lojas para comparação.")
    else:
        st.warning("Selecione ao menos uma loja para visualizar os dados.")

st.markdown("---")

st.markdown("### Recomendações Estratégicas")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Ações Urgentes**")
    
    produtos_ruptura = df_estoque_filtrado[df_estoque_filtrado['quantidade_estoque'] < df_estoque_filtrado['estoque_minimo']]
    if len(produtos_ruptura) > 0:
        st.error(f"**{len(produtos_ruptura)} produtos** em risco de ruptura de estoque")
        st.markdown("**Ação:** Realizar pedidos de reposição imediatamente")
        st.caption("_Justificativa: Produtos abaixo do estoque mínimo podem causar perda de vendas e insatisfação dos clientes._")
    else:
        st.success("✓ Nenhum produto em risco de ruptura")
    
    if len(df_vendas_filtrado) > 0:
        vendas_por_produto = df_vendas_filtrado.groupby('produto_id')['quantidade_vendida'].sum()
        estoque_alto = df_estoque_filtrado[df_estoque_filtrado['quantidade_estoque'] > df_estoque_filtrado['estoque_minimo'] * 2]
        
        produtos_parados = []
        for _, row in estoque_alto.iterrows():
            vendas = vendas_por_produto.get(row['produto_id'], 0)
            if vendas < row['quantidade_estoque'] * 0.1:
                produtos_parados.append(row)
        
        if len(produtos_parados) > 0:
            st.warning(f"**{len(produtos_parados)} produtos** com excesso de estoque e baixa venda")
            st.markdown("**Ação:** Considerar promoções ou descontos")
            st.caption("_Justificativa: Reduzir o capital imobilizado e liberar espaço físico no estoque._")
        else:
            st.success("✓ Estoque proporcional às vendas")

with col2:
    st.markdown("**Oportunidades**")
    
    if len(df_vendas_filtrado) > 0:
        top_5_vendas = df_vendas_filtrado.groupby(['produto_id', 'nome_produto'])['quantidade_vendida'].sum().sort_values(ascending=False).head(5)
        st.info(f"**Top 5 produtos** representam oportunidade de marketing")
        st.markdown("**Ação:** Investir em campanhas promocionais")
        st.caption("_Justificativa: Produtos com alta demanda têm maior potencial de retorno sobre investimento em marketing._")
        
        if len(df_compras_filtrado) > 0:
            fornecedores = df_compras_filtrado[df_compras_filtrado['status_compra'] == 'Entregue'].groupby('fornecedor').agg({
                'prazo_entrega_dias': 'mean',
                'valor_unitario': 'mean'
            })
            
            if len(fornecedores) > 0:
                melhor_prazo = fornecedores['prazo_entrega_dias'].idxmin()
                st.success(f"**Fornecedor recomendado:** {melhor_prazo}")
                st.markdown("**Ação:** Priorizar parcerias estratégicas")
                st.caption("_Justificativa: Menor prazo de entrega reduz tempo de reposição e risco de ruptura de estoque._")


st.markdown("### Análise por Categoria")
if len(df_vendas_filtrado) > 0:
    vendas_categoria = df_vendas_filtrado.groupby('categoria').agg({
        'valor_total': 'sum',
        'quantidade_vendida': 'sum'
    }).sort_values('valor_total', ascending=False)
    
    fig = px.bar(
        vendas_categoria,
        x=vendas_categoria.index,
        y='valor_total',
        title='Receita por Categoria',
        labels={'valor_total': 'Receita (R$)', 'index': 'Categoria'},
        color='valor_total',
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        plot_bgcolor='#2b2b2b',
        paper_bgcolor='#2b2b2b',
        font_color='#e0e0e0',
        title_font_color='#4da6ff',
        xaxis_title_font_color='#4da6ff',
        yaxis_title_font_color='#4da6ff'
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #808080;'>Super-Dashboard Integrado | Desenvolvido para a cadeira de Fundamentos em Ciência da Dados 2025.2</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #808080;'>2025 - Rafael Alves</p>", unsafe_allow_html=True)