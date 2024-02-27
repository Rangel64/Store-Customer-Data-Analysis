import pandas as pd

df = None
sales_per_month = None
product_sales_per_month = None
merged_product_line_unit_price = None
best_selling_product_line_df = None
five_best_selling_product_line_per_rating = None
count_selling_branchs = None
popular_payment_methods = None
top3_by_gender = None
most_profitable_by_branch = None
most_profitable_by_quarter = None
day_period_with_most_sales = None
sales_by_quarter_region_category = None
# sales_per_product_per_month = None


df_zeros = []

def main():
    
    global sales_per_month, product_sales_per_month, merged_product_line_unit_price
    global best_selling_product_line_df, five_best_selling_product_line_per_rating, count_selling_branchs 
    global popular_payment_methods, top3_by_gender, most_profitable_by_branch 
    global most_profitable_by_quarter, day_period_with_most_sales, sales_by_quarter_region_category
    global df_zeros,df
    
    #carregando os dados
    df = pd.read_csv("C:/Users/range/Desktop/testeTecnicoGrao/raw/commerce_dataset.csv",delimiter=';')
    
    #verificado se existe algum valor faltante
    num_nulls = df.isnull().sum()
    
    # Convertendo a coluna dtme para o formato de data
    df['dtme'] = pd.to_datetime(df['dtme'])
    
    # Criando uma nova coluna com o número do mês
    df['month_num'] = df['dtme'].dt.month
    
    print(num_nulls)
    
    columns = ['unit_price','quantity','vat','total','cogs','gross_margin_pct','gross_income','rating']
    
    for column in columns:
            tabela_valores_negativos = df.loc[df[column] < 0]
            df_zeros.append(tabela_valores_negativos)
    
    # Calcular a receita (gross_income) para cada linha
    df['gross_income'] = df['cogs']/(1-df['gross_margin_pct']/100)
    
    df.to_csv('work/commerce_dataset.csv', index=False)
    #============================================================================================================================

    #============================================================================================================================
    df = pd.read_csv("work/commerce_dataset.csv")
    
    #Total de vendas no período.
    #==================================================================================
    # numero_total_vendas = len(date_list)
    sales_per_month = df.groupby(['month_name','month_num'])['month_name'].value_counts().reset_index()
    #==================================================================================
    
    #Número total de produtos vendidos.
    #==================================================================================
    product_sales_per_month = df.groupby(['month_name','month_num'])['quantity'].sum().reset_index()
    #==================================================================================
    
    #Média de preço unitário de linha de produtos.
    #==================================================================================
    # calculando a quantidade de repeticoes para cada product_line
    product_line_quant = df['product_line'].value_counts().reset_index()
    product_line_quant.columns = ['product_line', 'count']
    
    # Calculo da soma de 'unit_price' agrupada por 'product_line'
    product_line_unit_price = df.groupby('product_line')['unit_price'].sum().reset_index()
    
    # Juntar as duas tabelas anteriores
    merged_product_line_unit_price = pd.merge(product_line_quant, product_line_unit_price, on='product_line')
    
    #calculando a media de unit_price 
    merged_product_line_unit_price ['unit_price_mean'] = merged_product_line_unit_price ['unit_price'] / merged_product_line_unit_price ['count']
    
    #==================================================================================
    
    #Linha de produto mais vendido (em termos de quantidade).
    #==================================================================================
    sales_per_product_per_month = df.groupby(['product_line', 'month_name','month_num'])['quantity'].sum().reset_index()
    max_quantity_product_line = sales_per_product_per_month.groupby('product_line')['quantity'].sum().idxmax()
    print(sales_per_product_per_month)
    best_selling_product_line_df = sales_per_product_per_month[sales_per_product_per_month['product_line'] == max_quantity_product_line]
    # best_selling_product_line = df.groupby('product_line')['quantity'].sum().idxmax()
    #==================================================================================
    
    #As 5 linhas de produtos mais bem avaliados (média de rating mais alta).
    #==================================================================================
    product_line_quant = df['product_line'].value_counts().reset_index()
    product_line_quant.columns = ['product_line', 'count']
    
    product_line_rate = df.groupby('product_line')['rating'].sum().reset_index()
    merged_product_rate_mean = pd.merge(product_line_quant, product_line_rate, on='product_line')
    merged_product_rate_mean['rating_mean'] = merged_product_rate_mean['rating']/merged_product_rate_mean['count']
    five_best_selling_product_line_per_rating = merged_product_rate_mean.sort_values(by='rating_mean',ascending=False).head(5)
    #==================================================================================
    
    #Loja com o maior volume de vendas.
    #==================================================================================
    count_selling_branchs = df['branch'].value_counts().reset_index().sort_values(by='count',ascending=False).head(1)
    
    #==================================================================================
    
    #Método de pagamento mais popular por loja e mês.
    #==================================================================================
    payment_counts = df.groupby(['branch', 'month_name', 'payment_method','month_num']).size().reset_index(name='count')
    idx = payment_counts.groupby(['branch', 'month_name'])['count'].transform(max) == payment_counts['count']
    popular_payment_methods = payment_counts[idx]
    #==================================================================================
    
    #As 3 linhas de produtos com mais quantidades vendidas por gênero do cliente.
    #==================================================================================
    grouped = df.groupby(['gender'])['product_line'].value_counts().reset_index()
    top3_by_gender = grouped.groupby('gender').apply(lambda x: x.nlargest(3, 'count')).reset_index(drop=True)
    #==================================================================================
    
    #Produto mais lucrativo (maior receita gross_income) por filial (branch)
    #==================================================================================
    most_profitable_by_branch = df.groupby(['branch', 'product_line'])['gross_income'].sum().reset_index()
    most_profitable_by_branch = most_profitable_by_branch.loc[most_profitable_by_branch.groupby('branch')['gross_income'].idxmax()]
    #==================================================================================
    
    # Produto mais lucrativo (maior receita gross_income) por quarter.
    #==================================================================================
    df['dtme'] = pd.to_datetime(df['dtme'])
    # Extraindo o trimestre (quarter)
    df['quarter'] = df['dtme'].dt.to_period('Q')
    
    # Encontrar o produto mais lucrativo por quarter
    most_profitable_by_quarter = df.groupby(['quarter', 'product_line'])['gross_income'].sum().reset_index()
    most_profitable_by_quarter = most_profitable_by_quarter.loc[most_profitable_by_quarter.groupby('quarter')['gross_income'].idxmax()]
    #==================================================================================
    
    #Período do dia em que ocorre o maior número de vendas.
    #==================================================================================
    # Contar o número de vendas em cada período do dia
    # sales_by_time_of_day = df['time_of_day'].value_counts()
    
    # Encontrar o período do dia com o maior número de vendas
    # day_period_with_most_sales = sales_by_time_of_day.idxmax()
    day_period_with_most_sales = df.groupby(['time_of_day'])['time_of_day'].value_counts().reset_index()
    #==================================================================================
    
    # Agrupar os dados por quarter, city e product_line e somar a receita para cada combinação
    #==================================================================================
    sales_by_quarter_region_category = df.groupby(['quarter', 'city', 'product_line'])['gross_income'].sum().reset_index()
    #==================================================================================

    df.to_csv("C:/Users/range/Desktop/testeTecnicoGrao/work/commerce_dataset.csv",index=False)
    sales_per_month.to_csv("C:/Users/range/Desktop/testeTecnicoGrao/work/sales_per_month.csv",index=False)
    product_sales_per_month.to_csv("C:/Users/range/Desktop/testeTecnicoGrao/work/product_sales_per_month.csv",index=False)
    merged_product_line_unit_price.to_csv("C:/Users/range/Desktop/testeTecnicoGrao/work/mean_product_line_unit_price.csv",index=False)
    best_selling_product_line_df.to_csv("C:/Users/range/Desktop/testeTecnicoGrao/work/best_selling_product_line_df.csv",index=False)
    five_best_selling_product_line_per_rating.to_csv("C:/Users/range/Desktop/testeTecnicoGrao/work/five_best_selling_product_line_per_rating.csv",index=False)
    count_selling_branchs.to_csv("C:/Users/range/Desktop/testeTecnicoGrao/work/count_selling_branchs.csv",index=False)
    popular_payment_methods.to_csv("C:/Users/range/Desktop/testeTecnicoGrao/work/popular_payment_methods.csv",index=False)
    top3_by_gender.to_csv("C:/Users/range/Desktop/testeTecnicoGrao/work/top3_by_gender.csv",index=False)
    most_profitable_by_branch.to_csv("C:/Users/range/Desktop/testeTecnicoGrao/work/most_profitable_by_branch.csv",index=False)
    most_profitable_by_quarter.to_csv("C:/Users/range/Desktop/testeTecnicoGrao/work/most_profitable_by_quarter.csv",index=False)
    day_period_with_most_sales.to_csv("C:/Users/range/Desktop/testeTecnicoGrao/work/day_period_with_most_sales.csv",index=False)
    sales_by_quarter_region_category.to_csv("C:/Users/range/Desktop/testeTecnicoGrao/work/sales_by_quarter_region_category.csv",index=False)
        
if __name__ == "__main__":
    main();
