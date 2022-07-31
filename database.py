import pandas as pd

import datetime

start_date = datetime.datetime(2016,10,1)
end_date = datetime.datetime(2022,7,1)
freq = pd.offsets.MonthBegin(1)

date_range = pd.date_range(
    start = start_date, 
    end = end_date + freq, 
    freq='M'
  ) - freq

def load_exog_covid_month(): 
  start_covid = datetime.datetime(2020, 3, 1)
  covid_dummy = []
  for date in date_range: 
    if(start_covid < date):
      covid_dummy.append(1)
    else:
      covid_dummy.append(0)
  return (covid_dummy)


def load_exog_petroleum_database_month():
  # https://br.investing.com/currencies/usd-brl-historical-data
  petroleo = pd.read_csv('Petróleo Brent Futuros Dados Históricos-desde-out-2016.csv')
  
  petroleo['Último'] = petroleo['Último'].str.replace(',', '.').astype(float)
  data_aux = pd.DataFrame({'date': date_range, 'price': reversed(petroleo['Último'].values) })
  return data_aux

def load_exog_dolar_database_month():
  # https://br.investing.com/currencies/usd-brl-historical-data
  dolar = pd.read_csv('USD_BRL Dados Históricos-desde-out2016.csv')

  dolar['Último'] = dolar['Último'].str.replace(',', '.').astype(float)
  data_aux = pd.DataFrame({'date': date_range, 'price': reversed(dolar['Último'].values) })
  return (data_aux)


def load_database_month(): 
  filename = 'mensal-estados-desde-jan2013-ate-jul2022.xlsx'
  #file_url = "https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/precos-revenda-e-de-distribuicao-combustiveis/shlp/semanal/semanal-regioes-desde-2013.xlsx"
  database = pd.read_excel(filename, skiprows=16)
  ## Excluir colunas desnecessárias
  database = database.drop([
    'NÚMERO DE POSTOS PESQUISADOS', 
    'UNIDADE DE MEDIDA',
    'DESVIO PADRÃO REVENDA',
    'PREÇO MÍNIMO REVENDA',
    'PREÇO MÁXIMO REVENDA',
    'MARGEM MÉDIA REVENDA',
    'COEF DE VARIAÇÃO REVENDA',
    'PREÇO MÉDIO DISTRIBUIÇÃO',
    'DESVIO PADRÃO DISTRIBUIÇÃO',
    'PREÇO MÍNIMO DISTRIBUIÇÃO',
    'PREÇO MÁXIMO DISTRIBUIÇÃO',
    'COEF DE VARIAÇÃO DISTRIBUIÇÃO'], 
    axis=1
  )
  ## Renomear colunas
  database = database.rename(columns={
      'MÊS': 'date',
      'REGIÃO': 'region',
      'ESTADO': 'state',
      'PRODUTO': 'product',
      'PREÇO MÉDIO REVENDA': 'price'
  })

  return(database)


def create_time_series(data_frame, start_date, end_date, var, freq):
  # time series
  time_series = pd.Series(
      data = data_frame[var].values,
      index = pd.date_range(start = start_date, end = end_date, freq = freq)
    )

  return(time_series)


##  Converter o dataframe em uma serie temporal
def case_treatment(data): 
  data_aux = pd.DataFrame({'date': date_range })

  data = pd.merge(data_aux, data, on='date', how='left')

  data = data.set_index(["date"], drop=True)  
  data.interpolate(method='linear', inplace=True)

  time_series = create_time_series(
    data, 
    start_date, 
    end_date, 
    var="price", 
    freq=freq
  )
  return time_series
