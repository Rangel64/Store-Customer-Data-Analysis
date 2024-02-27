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

x_train, x_test, y_train, y_test = train_test_split(x, y_norm, test_size=0.2)

earlyStopping = callbacks.EarlyStopping(
            monitor='loss', mode='min', patience=2000, restore_best_weights=True, verbose=1)

rede = Sequential()
rede.add(Dense(units=16, activation='relu', input_dim=1))
rede.add(Dense(units=64, activation='relu'))
rede.add(Dense(units=128, activation='relu'))
rede.add(Dense(units=256, activation='relu'))
rede.add(Dense(units=256, activation='relu'))
rede.add(Dense(units=128, activation='relu'))
rede.add(Dense(units=64, activation='relu'))
rede.add(Dense(units=16, activation='relu'))
rede.add(Dense(units=1, activation='relu'))
rede.compile(optimizer='rmsprop', loss='mse')

rede.fit(x_train,y_train,epochs=20000,validation_data = (x_test, y_test),callbacks=[earlyStopping])

y_pred = rede.predict(x_test)

plt.figure(figsize=(12, 6))
plt.scatter(range(len(y_test)), y_test.values, label='Valor Real', c='blue')
plt.scatter(range(len(y_pred)), y_pred, label='Valor Previsto', c='red')
plt.title('Comparação entre Valor Real e Previsto')
plt.xlabel('Índice')
plt.ylabel('Valor Normalizado')
plt.legend()
plt.show()

y_pred_all_n = rede.predict(x_all)
y_pred_all =  (y_pred_all_n*(y_max-y_min))+y_min
plt.figure(figsize=(12, 6))
plt.plot(y.values, label='Valor Real', c='blue')
plt.plot(y_pred_all, label='Valor Previsto', c='red')
plt.title('Comparação entre Valor Real e Previsto')
plt.xlabel('Índice')
plt.ylabel('Valor Normalizado')
plt.legend()
plt.show()

rede.save('model/model4.h5')
