# -*- coding: utf-8 -*-
"""forecasting and compare saham

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NTmeFCOF1Ez8EtvB3RpsXrpUz52snNIa
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import pandas_datareader.data as web
import datetime
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split

start = datetime.datetime(2019,1,1)
end = datetime.datetime(2019,11,29)

df = web.DataReader("TLKM.JK",'yahoo',start,end)

df.tail()

plt.plot(df['Adj Close']) # melihat Trend nilai sahamnya apakah lagi naik atau turun

# membuat rumus untuk menambahkan hasil perhitungan ke tabel
dfreg = df.loc[:,['Adj Close','Volume']]
# HL PCT adalah High & Low Percentage
dfreg['HL_PCT'] = (df['High'] - df['Low']) / df['Close'] * 100.0
# PCT CHange adalah perubahan persentase
dfreg['PCT_change'] = (df['Close'] - df['Open']) / df['Open'] *100.0

plt.plot(dfreg['HL_PCT'])

# drop missing value
dfreg = dfreg.dropna()

# forecasting perseminggu
forecast_out = 7  # 7 days

dfreg['label'] = dfreg['Adj Close'].shift(-forecast_out)
# akan muncul kolom baru bernama label merupakan hasil nilai saham 7 hari kedepan
dfreg.head(15)

X = np.array(dfreg.drop(['label'],1)) # X adalah nilai dfreg tanpa kolom label

X = preprocessing.scale(X)
X_lately = X[-forecast_out:]
X = X[:-forecast_out]

y = np.array(dfreg['label']) # y adalah nilai dfreg dengan kolom label
y = y[:-forecast_out]

# membuat data train
X_train = X
y_train = y

# split data
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size = 0.2, random_state = 20 )

# menggunakan linear regression
clfreg = LinearRegression()
clfreg.fit(X_train, y_train)

clf = clfreg

clf.predict(X_lately) # predict 7 periode kedepan

forecast_set = clf.predict(X_lately)
dfreg['Forecast'] = np.nan

last_date = dfreg.iloc[-1].name
last_unix = last_date
next_unix = last_unix + datetime.timedelta(days=1) # untuk nambah 1 hari (besoknya)

for i in forecast_set:
  next_date = next_unix
  next_unix += datetime.timedelta(days=1)
  dfreg.loc[next_date] = [np.nan for _ in range(len(dfreg.columns)-1)] + [i]

dfreg['Adj Close'].tail(50).plot()
dfreg['Forecast'].tail(50).plot()
plt.legend(loc=1)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

# moving average
close_px = df['Adj Close']
# window = days
mavg = close_px.rolling(window=30).mean()
mavg2 = close_px.rolling(window=100,center=True).mean()

close_px.plot()
mavg.plot()
mavg2.plot()

# return
rets = close_px / close_px.shift(1) - 1
rets.plot()

# membandingkan dengan nilai saham perusahaan lain
dfcomp = web.DataReader(['AALI.JK', 'BBCA.JK', 'AUTO.JK', 'BBRI.JK', 'KLBF.JK'], 'yahoo', start, end)['Adj Close']

dfcomp = dfcomp.dropna()  # untuk menghilangkan nilai yang tidak ada dari perhitungan
dfcomp.tail()

retscomp = dfcomp.pct_change() # perubahan nilai
corr = retscomp.corr() # korelasinya

corr

plt.imshow(corr, cmap='hot', interpolation=None)
plt.colorbar()
plt.xticks(range(len(corr)), corr.columns)
plt.yticks(range(len(corr)), corr.columns)

# stock prediction













