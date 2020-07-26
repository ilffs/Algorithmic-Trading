#Uploading relevant libriaries 
import pandas as pd
import matplotlib.pyplot as plt
import quandl
#Downloading dataset from quandl.com
df = quandl.get("BCB/UDJIAD1", authtoken="s3ooaf8znnoVydHSMYYx")
df.head(-1)
df['% change'] = df['Value'].pct_change()
df['200 sma'] = df['Value'].rolling(window=200).mean().round(5)
df['50 sma'] = df['Value'].rolling(window=50).mean().round(5)
df['Criteria 1'] = df['Value'] >= df['200 sma']
df['Criteria 2'] = (df['50 sma'] >= df['200 sma']) | df['Criteria 1'] == True
df.head(200)
df['Buy and hold'] = (1+df['% change']).cumprod()
df['200 sma model'] = (1+df['Criteria 1'].shift(1)*df['% change']).cumprod()
df['200 sma + crossover model'] = (1+df['Criteria 2'].shift(1)*df['% change']).cumprod()
df.head(-1)
#200 sma model's returns
start_model1 = df['200 sma model'].iloc[200]
end_model = df['200 sma model'].iloc[-1]
years = (df['200 sma model'].count()+1-200)/252 
model1_average_return = (end_model/start_model1)**(1/years)-1
print('200 sma model yields an average of', round(model1_average_return*100, 3), '% per year')
#200 sma + crossover model's returns
start_model2 = df['200 sma + crossover model'].iloc[200]
end_model2 = df['200 sma + crossover model'].iloc[-1]
model2_average_return = (end_model2/start_model2)**(1/years)-1
print('200 sma + crossover model yields an average of', round(model2_average_return*100, 3), '% per year')
#Buy and hold's returns
start_spx = df['Value'].iloc[200]
end_spx = df['Value'].iloc[-1]
spx_average_return = (end_spx/start_spx)**(1/years)-1
print('Buy and hold yields an average of', round(spx_average_return, 3), '% per year')
#Visualizing and compering the results
df[['Buy and hold', '200 sma model', '200 sma + crossover model']].plot(grid=True, kind='line', title='Different models', logy=False)
plt.ylabel('Percente change')

