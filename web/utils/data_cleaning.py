import pandas as pd
import numpy as np

def read_rents():
    columns =['Commune', '# Offers Rent', 'Avg. Price Rent', 'Avg. Price per m2 Rent']

    rents_all = []

    for year in range(2009,2021):
        result = pd.read_excel(
            './data/loyers/loyers-annonces-apparts-2009-2020.xls', 
            skiprows=11, 
            usecols='C:F', 
            skipfooter=6, 
            sheet_name=str(year)).set_axis(columns, axis=1).replace('*', 0)
        result['Year'] = year
        rents_all.append(result) 
    
    return pd.concat(rents_all)

def read_sells():
    columns = [
        'Commune',
        '# Offers Constructed',
        'Avg. Price per m2 Constructed', 
        'Price Range per m2 Constructed', 
        '# Offers VEFA',
        'Avg. Price per m2 VEFA', 
        'Price Range per m2 VEFA', 
    ]

    prices = []

    for year in range(2009,2021):
        result = pd.read_excel(
            './data/prix-vende/prix-moyen-au-metre-carre-enregistre-par-commune-'+str(year)+'.xls',
            skiprows=13,
            usecols='B:H', 
            skipfooter=6
        ).replace('*', 0).set_axis(columns, axis=1)

        result['Year'] = year

        prices.append(result)
        
    return pd.concat(prices)

def read_communes():
    result = pd.read_excel(
        './data/Liste_des_codes_et_designations_des_communes_et_sections_2018.xlsx',
        skiprows=5,
        usecols='A:C'
    ).set_axis(['Commune ID', 'Commune', 'Administrative Commune'], axis=1)

    return result

def filter_sells(sell):

    sell['Price Range per m2 Constructed'] = sell['Price Range per m2 Constructed'].str.replace(' ','').str.replace('€', '')
    sell['Price Range per m2 VEFA'] = sell['Price Range per m2 VEFA'].str.replace(' ','').str.replace('€', '')

    #Transform Columns of price range
    sell[['Lower price per m2 VEFA','Highest price per m2 VEFA']] = sell['Price Range per m2 VEFA'].str.split('-', expand=True,)
    sell = sell.drop(columns=['Price Range per m2 VEFA']).replace(np.nan, 0)

    sell[['Lower price per m2 Constructed','Highest price per m2 Constructed']] = sell['Price Range per m2 Constructed'].str.split('-', expand=True,)
    sell = sell.drop(columns=['Price Range per m2 Constructed']).replace(np.nan, 0)

    return sell   

def merge_data(cc, re, se):
    ##Merging rents and sells
    df = pd.merge(re, se, on=['Commune', 'Year'], how="outer").fillna(0)

    ##Merging Rent/Sell with Commune Info
    df_final = pd.merge(df, cc, on=['Commune'], how='outer')
    df_final['Administrative Commune'] = df_final['Administrative Commune'].fillna('N/A')
    df_final.fillna(0, inplace=True)

    return df_final

def change_data_types(df):
    float_columns = [
        'Avg. Price Rent', 'Avg. Price per m2 Rent', 'Avg. Price per m2 Constructed', 
        'Avg. Price per m2 VEFA', 'Lower price per m2 VEFA', 'Highest price per m2 VEFA', 
        'Lower price per m2 Constructed', 'Highest price per m2 Constructed']
    df[float_columns] = df[float_columns].astype('float64')

    int_columns = ['# Offers Rent', '# Offers VEFA', '# Offers Constructed', 'Commune ID', 'Year']
    df[int_columns] = df[int_columns].astype(np.int16)

    return df

def get_data():
    communes = read_communes().drop_duplicates()

    sells = filter_sells(
        read_sells()
    )

    rents = read_rents()

    data = merge_data(communes, rents, sells)

    return change_data_types(data)
