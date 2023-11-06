"""--------------------------------------------------------------------

--------------------------------------------------------------------"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import numpy as np
from time import sleep
from pytrends.request import TrendReq
pytrend = TrendReq()

#--------------------------------------------------------------------
#Function to get google trend data for different countries in the world
#--------------------------------------------------------------------
def get_google_trends_International(daystart, dayend, keywords, countries):
    pytrend = TrendReq(hl='en-US', tz=360)
    kw_list = keywords
    df = pd.DataFrame()
    dates = pd.date_range(start=daystart, end=dayend, freq='MS')
    print(dates)
    print(countries)
    #make df uniquely identify each date and country
    for date in dates:
        for country in countries:
            df['country'] = country   
            df['date'] = date    
    #for each date include all countries
    df_word = pd.DataFrame()
    for keyword in keywords:
        sleep(5)
        for country in countries:
            sleep(5)
            pytrend.build_payload([keyword], cat=0, timeframe=daystart + ' ' + dayend, geo=country, gprop='')
            df_country = pytrend.interest_over_time()
            df_country['country'] = country
            #Add a date for each row
            for i in range(0, len(df_country)):
                df_country['country'] = country   
                df_country['date'] = df_country.index
            df_word = pd.concat([df_word, df_country], ignore_index=True)
        #merge each word into one dataframe
        df = pd.merge(df, df_word[['country', 'date', keyword]], on=['date', 'country'], how='right', copy = True)
        #define month-year variable
        df['date'] = pd.to_datetime(df['date'])
        df['monthly'] = df['date'].dt.strftime('%Y-%m')
        #convert to datetime
        df['monthly'] = pd.to_datetime(df['monthly'], format='%Y-%m')
    return df


#--------------------------------------------------------------------
#call the functions
#--------------------------------------------------------------------
def main():
    #set parameters
    daystart = '2022-03-01'
    dayend = '2022-04-01'
    keywords = ['unemployment', 'inflation', 'economy']
    
    #Define key graphing terms
    sns.set_style('darkgrid')
    sns.set_context('talk')
    sns.set_palette('dark')
    sns.set(font_scale=1.5)
    fig, ax = plt.subplots(figsize=(20, 20))
    
    oecd_country_codes = ['US', 'AU', 'UK', 'CA', 'NZ']
    US_code = ['US', 'UK']


    #Pull Google Trends Data
    trends_df = get_google_trends_International(daystart, dayend, keywords, US_code)
    #save trends data to csv
    trends_df.to_csv('international_trends.csv')
main()