# Super-Dashboard Integrado

Dashboard interativo para análise consolidada de Estoque, Vendas e Compras.

## Tecnologias Utilizadas

- **Python 3.8+**
- **Streamlit** - Framework para interface web
- **Pandas** - Manipulação de dados
- **Plotly** - Visualizações interativas
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
├── dashboard.py          # Código principal do dashboard
├── requirements.txt     # Dependências do projeto
├── FCD_estoque.csv      # Dados de estoque
├── FCD_vendas.csv       # Dados de vendas
├── FCD_compras.csv      # Dados de compras
└── README.md            # Documentação
```

## Funcionalidades

### Filtros Interativos
- Categoria de produtos
- Produto específico
- Loja
- Período (data início/fim)

### Indicadores Principais
- Receita Total
- Valor do Estoque
- Gasto em Compras
- Produtos Críticos

### Visão 360° do Produto
- Estoque atual vs. estoque mínimo
- Vendas acumuladas
- Compras recebidas
- Fornecedor principal
- Alertas visuais

### Análises Estratégicas
- Produtos com estoque crítico
- Top 10 produtos mais vendidos
- Maiores gastos em compras
- Análise de fornecedores (preço, prazo, volume)

### Gráficos Avançados
- Série temporal: Vendas vs Compras
- Relação Estoque × Vendas × Compras
- Análise por loja
- Receita por categoria

### Recomendações Estratégicas
- Identificação de produtos em risco de ruptura
- Produtos com excesso de estoque
- Oportunidades de marketing
- Avaliação de fornecedores

## Como Usar

1. **Selecione os filtros** na barra lateral esquerda:
   - Escolha uma categoria ou produto específico
   - Selecione a loja de interesse
   - Defina o período de análise

2. **Visualize os indicadores principais** no topo:
   - Receita, valor do estoque, gastos e alertas críticos

3. **Explore as abas de análise**:
   - Produtos Críticos: identifique itens em risco
   - Top 10 Vendas: produtos mais lucrativos
   - Maiores Gastos: onde está o investimento
   - Fornecedores: análise de performance

4. **Analise os gráficos avançados**:
   - Evolução temporal de vendas e compras
   - Comparação entre estoque, vendas e compras
   - Distribuição por loja

5. **Revise as recomendações estratégicas** ao final

## Observações

- Os arquivos CSV devem estar no mesmo diretório do `dashboard.py`
- Os arquivos CSV utilizam ponto-e-vírgula (;) como separador
- O relacionamento entre dados é feito pelo campo `produto_id`
- Design: fundo cinza (#2b2b2b) com destaque azul (#4da6ff)
