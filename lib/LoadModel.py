#%%

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras.optimizers import SGD
from keras import callbacks
from sklearn.metrics import r2_score
from tensorflow import keras

df = pd.read_csv("C:/Users/range/Desktop/testeTecnicoGrao/work/commerce_dataset.csv")

# Converter a coluna 'dtme' para datetime
df['dtme'] = pd.to_datetime(df['dtme'])

total_vendas_por_dia = df.groupby('dtme')['total'].sum().reset_index()

# Crie um intervalo de datas entre 2019-04-01 e 2019-06-30
dates = pd.date_range(start='2019-04-01', end='2019-06-30')

# Crie um DataFrame com as datas e uma coluna de valores total zerados
df_new_dates = pd.DataFrame({'dtme': dates, 'total': 0})

# Concatene o DataFrame existente com as novas datas
df_concatenated = pd.concat([total_vendas_por_dia, df_new_dates], ignore_index=True)

# Ordene o DataFrame por data
df_concatenated.sort_values('dtme', inplace=True)

# Reset o índice
df_concatenated.reset_index(drop=True, inplace=True)

all_dates = df_concatenated['dtme'].values

#Criando os objetos label encoder e scaller
le = LabelEncoder()
scaler = MinMaxScaler(feature_range=(-1, 1))

df_concatenated['dtme'] = scaler.fit_transform(le.fit_transform(df_concatenated['dtme']).reshape(-1, 1))

x_all = df_concatenated.drop(['total'], axis=1)

x = df_concatenated.iloc[0:89].drop(['total'], axis=1)

y = df_concatenated.iloc[0:89].drop(['dtme'], axis=1)

y_max = y['total'].max()
y_min = y['total'].min()

y_norm = (y - y_min) / (y_max - y_min)


rede = keras.models.load_model('model/model4.h5')

y_pred_q1_n = rede.predict(x)

y_pred_q1 = (y_pred_q1_n*(y_max-y_min))+y_min

mean = y_pred_q1.mean()
std = y_pred_q1.std()

r2 = r2_score(y, y_pred_q1)

y_pred_q1 = y_pred_q1.reshape(-1)
df_pred = pd.DataFrame({'data': total_vendas_por_dia['dtme'],'total':y_pred_q1})

df_pred['data'] = pd.to_datetime(df_pred['data'])

# Definir a janela de 15 dias e calcular a média e desvio padrao
df_pred_mean = df_pred.rolling(window=15, on='data')['total'].mean()
df_pred_std = df_pred.rolling(window=15, on='data')['total'].std()

# transformando em dataframes
df_mean = pd.DataFrame({'data': df_pred['data'], 'mean_total': df_pred_mean.values})
df_std = pd.DataFrame({'data': df_pred['data'], 'std_total': df_pred_std.values})

# Definir o estilo do seaborn
sns.set_style("whitegrid")

# Criar o gráfico
plt.figure(figsize=(12, 6))
sns.lineplot(x='dtme', y='total', data=total_vendas_por_dia, marker='o')
sns.lineplot(x='data', y='total', data=df_pred, marker='o')

# Adicionar título e rótulos dos eixos
plt.title('Total de Vendas por Dia', fontsize=16)
plt.xlabel('Data', fontsize=12)
plt.ylabel('Total de Vendas', fontsize=12)

# Adicionar informações sobre o modelo
info_text = f'Média: {mean:.2f}\nDesvio Padrão: {std:.2f}\nR²: {r2:.2f}'
plt.text(0.02, 0.95, info_text, transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')

# Rotacionar os rótulos do eixo x para facilitar a leitura
plt.xticks(rotation=45)

# Exibir o gráfico
plt.tight_layout()
plt.show()


#%%

y_pred_q1q2_n = rede.predict(x_all)

y_pred_q1q2 = (y_pred_q1q2_n*(y_max-y_min))+y_min

mean_q1q2 = y_pred_q1q2.mean()
std_q1q2 = y_pred_q1q2.std()


y_pred_q1q2 = y_pred_q1q2.reshape(-1)
df_pred_q1q2 = pd.DataFrame({'data': all_dates,'total':y_pred_q1q2})

df_pred_q1q2['data'] = pd.to_datetime(df_pred_q1q2['data'])

# Definir o estilo do seaborn
sns.set_style("whitegrid")

# Criar o gráfico
plt.figure(figsize=(12, 6))
sns.lineplot(x='dtme', y='total', data=total_vendas_por_dia, marker='o')
sns.lineplot(x='data', y='total', data=df_pred_q1q2, marker='o')

# Adicionar título e rótulos dos eixos
plt.title('Total de Vendas por Dia', fontsize=16)
plt.xlabel('Data', fontsize=12)
plt.ylabel('Total de Vendas', fontsize=12)

# Adicionar informações sobre o modelo
info_text = f'Média: {mean_q1q2:.2f}\nDesvio Padrão: {std_q1q2:.2f}\n'
plt.text(0.02, 0.95, info_text, transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')

# Rotacionar os rótulos do eixo x para facilitar a leitura
plt.xticks(rotation=45)

# Exibir o gráfico
plt.tight_layout()
plt.show()