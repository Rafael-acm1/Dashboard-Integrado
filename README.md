# Super-Dashboard Integrado 📊

Dashboard interativo para análise consolidada de **Estoque**, **Vendas** e **Compras** de peças automotivas.

Sistema desenvolvido para gerenciamento estratégico de inventário multi-loja (Loja 1, Loja 2 e Depósito Central), oferecendo visão 360° de produtos, análise de fornecedores e recomendações estratégicas baseadas em dados.

## 🚀 Tecnologias Utilizadas

- **Python 3.8+**
- **Streamlit** - Framework para interface web interativa
- **Pandas** - Manipulação e análise de dados
- **Plotly Express & Graph Objects** - Visualizações interativas avançadas
- **NumPy** - Operações numéricas

## Instalação

### 1. Instalar Python
Certifique-se de ter o Python 3.8 ou superior instalado.

### 2. Instalar Dependências

**Opção 1 - Usando requirements.txt:**
```powershell
pip install -r requirements.txt
```

**Opção 2 - Instalação manual:**
```powershell
pip install streamlit pandas plotly numpy
```

## Execução

No diretório do projeto, execute:

```powershell
streamlit run dashboard.py
```

O dashboard será aberto automaticamente no navegador em `http://localhost:8501`

Para encerrar, pressione `Ctrl+C` no terminal.

## Estrutura de Arquivos

```
DashboardIntegrado/
├── dashboard.py         # Código principal do dashboard
├── requirements.txt     # Dependências do projeto
├── FCD_estoque.csv      # Dados de estoque
├── FCD_vendas.csv       # Dados de vendas
├── FCD_compras.csv      # Dados de compras
├── FCD_produtos.csv     # Dados dos produtos
└── README.md            # Documentação
```

## ✨ Funcionalidades

### 🎯 Filtros Interativos Multi-Seleção
- **Categorias**: Selecione múltiplas categorias (Motor, Freios, Suspensão, Elétrica, Transmissão, Pneus, Acessórios)
- **Produtos**: Multiselect inteligente com contador (deixe vazio para incluir todos)
- **Lojas**: Loja 1, Loja 2 e Depósito Central (seleção múltipla)
- **Período**: Filtro por intervalo de datas (início/fim)

### 📈 Indicadores Principais
- **💰 Receita Total**: Soma de todas as vendas no período
- **📦 Valor do Estoque**: Valorização do estoque atual (data mais recente de cada produto/localização)
- **🛒 Gasto em Compras**: Total investido em compras no período
- **⚠️ Produtos Críticos**: Quantidade de produtos abaixo do estoque mínimo (somando todas as localizações)
- **⏱️ Prazo Médio de Reposição**: Tempo médio de entrega dos fornecedores

### 🎯 Visão 360° do Produto
**Disponível ao selecionar apenas 1 produto**
- **Estoque**: Quantidade atual vs. mínimo com alertas coloridos (crítico/adequado/excesso)
- **Vendas**: Quantidade vendida e receita gerada no período
- **Compras**: Quantidade comprada, valor investido e fornecedor principal
- **Alertas visuais**: Indicadores de risco automáticos

### 📊 Indicadores Estratégicos (4 Abas)

#### 1. Produtos Críticos
- Listagem de produtos abaixo do estoque mínimo
- Cálculo de déficit (estoque mínimo - estoque atual)
- Gráfico de barras dos Top 10 produtos com maior déficit
- **Obs**: Soma estoque de todas as localizações por produto

#### 2. Top 10 Vendas
- Produtos mais vendidos por quantidade e receita
- Gráficos comparativos lado a lado
- Tabela detalhada com categoria

#### 3. Maiores Gastos
- Top 10 produtos com maior investimento em compras
- Análise de quantidade comprada vs. valor total
- Foco em compras com status "Entregue"

#### 4. Fornecedores
- Preço médio por fornecedor
- Prazo médio de entrega por fornecedor
- Matriz de análise (scatter plot): Prazo vs. Preço vs. Volume
- Tempo médio geral de reposição

### 📉 Análises Avançadas (3 Abas)

#### 1. Série Temporal
- Evolução mensal: Vendas vs Compras
- Gráfico de linhas interativo

#### 2. Estoque vs Vendas vs Compras
- Top 20 produtos em gráfico de barras agrupadas
- Comparação visual de três métricas

#### 3. Análise por Loja
- Distribuição de receita (gráfico de pizza)
- Quantidade vendida por loja (gráfico de barras)
- Comparativo entre múltiplas lojas

### 💡 Recomendações Estratégicas com Justificativas

#### Ações Urgentes
- **Produtos em risco de ruptura**: Identificação + justificativa (evitar perda de vendas)
- **Produtos parados**: Excesso de estoque + baixa venda + sugestão de promoções

#### Oportunidades
- **Top 5 produtos**: Oportunidades de marketing com ROI elevado
- **Fornecedor recomendado**: Menor prazo de entrega para reduzir tempo de reposição

### 📊 Análise por Categoria
- Receita total por categoria
- Gráfico de barras interativo
- Ordenação por valor

## 📖 Como Usar

### 1. Configure os Filtros (Barra Lateral)
- **Categoria**: Selecione uma ou múltiplas categorias (padrão: todas)
- **Produto**: Deixe vazio para todos, ou selecione produtos específicos
  - 💡 *Dica*: Selecione apenas 1 produto para visualizar a **Visão 360°**
- **Loja**: Escolha Loja 1, Loja 2, Depósito Central ou combinações
- **Período**: Defina data de início e fim

### 2. Analise os Indicadores Principais
Veja métricas consolidadas no topo:
- Receita Total, Valor do Estoque, Gastos
- Produtos Críticos e Prazo Médio de Reposição

### 3. Explore os Indicadores Estratégicos
Navegue pelas 4 abas:
- **Produtos Críticos**: Identifique riscos de ruptura
- **Top 10 Vendas**: Produtos mais lucrativos
- **Maiores Gastos**: Onde está o investimento
- **Fornecedores**: Performance de prazo e preço

### 4. Visualize Análises Avançadas
Gráficos interativos de:
- Evolução temporal
- Comparação Estoque × Vendas × Compras
- Distribuição por loja

### 5. Consulte as Recomendações
Ações sugeridas com justificativas estratégicas

## ⚙️ Regras de Negócio

### Cálculo de Estoque
- **Lógica**: Considera apenas a **data mais recente** de cada produto em cada localização
- **Agrupamento**: Soma as quantidades de todas as localizações para cálculo de produtos críticos
- **Valorização**: Utiliza `preco_unitario` do cadastro de produtos

### Produtos Críticos
- **Critério**: Estoque Total < Estoque Mínimo Total (somando todas as localizações)
- **Exemplo**: Se produto tem 10un na Loja 1 (mín: 15) e 20un na Loja 2 (mín: 15)
  - Total: 30un, Mínimo: 30un → **NÃO é crítico**

### Gastos em Compras
- **Incluídos**: Todas as compras no período, independente do status
- **Filtro**: Apenas para análise de fornecedores usa-se status "Entregue"

## 🎨 Design

- **Tema**: Dark mode com fundo cinza escuro (#2b2b2b)
- **Destaque**: Azul (#4da6ff) para títulos e elementos interativos
- **Alertas**: Vermelho (crítico), Amarelo (atenção), Verde (sucesso)
- **Responsivo**: Layout em colunas adaptável

## 📝 Observações Técnicas

- **Separador CSV**: Ponto-e-vírgula (;)
- **Encoding**: UTF-8
- **Chave de relacionamento**: `produto_id`
- **Cache**: Função `carregar_dados()` usa `@st.cache_data` para performance
- **Formato de datas**: 
  - Estoque: já em formato datetime
  - Vendas/Compras: `%d/%m/%Y` (ex: 18/01/2024)
