import pandas as pd


df = pd.read_csv("raw/commerce_dataset.csv",delimiter=';')

columns = df.columns

num_nulls = df.isnull().sum()

df = df.map(lambda s: s.lower() if type(s) == str else s)

df.to_csv('work/commerce_dataset.csv', index=False)

#%%

df = pd.read_csv("work/commerce_dataset.csv")

date_list = df['dtme'].values.tolist()

#Total de vendas no período.
#==================================================================================
numero_total_vendas = len(date_list)
#==================================================================================

#Número total de produtos vendidos.
#==================================================================================
total_produtos_vendidos = df['quantity'].values.sum()
#==================================================================================

#Média de preço unitário de linha de produtos.
#==================================================================================
# Calcular a contagem de 'product_line'
product_line_quant = df['product_line'].value_counts().reset_index()
product_line_quant.columns = ['product_line', 'quant']

# Calcular a soma de 'unit_price' agrupada por 'product_line'
product_line_unit_price = df.groupby('product_line')['unit_price'].sum().reset_index()

# Juntar as duas tabelas
merged_product_line_unit_price  = pd.merge(product_line_quant, product_line_unit_price, on='product_line')

merged_product_line_unit_price ['unit_price_mean'] = merged_product_line_unit_price ['unit_price'] / merged_product_line_unit_price ['quant']
#==================================================================================

#Linha de produto mais vendido (em termos de quantidade).
#==================================================================================
best_selling_product_line = product_line_quant.loc[product_line_quant['quant'].idxmax(), 'product_line']
#==================================================================================

#As 5 linhas de produtos mais bem avaliados (média de rating mais alta).
#==================================================================================
product_line_quant = df['product_line'].value_counts().reset_index()
product_line_quant.columns = ['product_line', 'quant']

product_line_rate = df.groupby('product_line')['rating'].sum().reset_index()
merged_product_rate_mean = pd.merge(product_line_quant, product_line_rate, on='product_line')
merged_product_rate_mean['rating_mean'] = merged_product_rate_mean['rating']/merged_product_rate_mean['quant']
five_best_selling_product_line_per_rating = merged_product_rate_mean.sort_values(by='rating_mean',ascending=False).head(5)
#==================================================================================

#Loja com o maior volume de vendas.
#==================================================================================
count_selling_branchs = df['branch'].value_counts().reset_index().sort_values(by='count',ascending=False).head(1)
#==================================================================================

#Método de pagamento mais popular por loja e mês.
#==================================================================================

#==================================================================================
