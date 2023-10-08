"""--------------------------------------------------------------------
Description: This file uses the pytrends api to collect data on google 
             search interest in inflation and unemployment and generate
             a plot showing the relationship between the two terms. This 
             concept was originally demonstrated by Noah Williams on twitter:
            https://x.com/Bellmanequation/status/1516125998189842432?s=20.
            I hope this replication can serve as a jumping off place for 
            work using google trends data to estimate the relationship 
            between inflation expectations and political polarization.
--------------------------------------------------------------------"""

import pandas as pd   
import matplotlib.pyplot as plt
import seaborn as sns    
import statsmodels.api as sm
from pytrends.request import TrendReq
pytrend = TrendReq()

#--------------------------------------------------------------------
#Function to get google trend data for the country as a whole, collecting 
# each term separately and merging by date
#--------------------------------------------------------------------
def get_google_trends_US(daystart, dayend, keywords):
    pytrend = TrendReq(hl='en-US', tz=360)
    kw_list = keywords
    df = pd.DataFrame()
    dates = pd.date_range(start=daystart, end=dayend, freq='MS')
    print(dates)
    #make df uniquely identify each date
    for date in dates:
        df['date'] = date    
    #for each date include all states
    df_word = pd.DataFrame()
    for keyword in keywords:
        pytrend.build_payload([keyword], cat=0, timeframe=daystart + ' ' + dayend, geo='US', gprop='')
        df_temp = pytrend.interest_over_time()
        #Add a date for each row
        for i in range(0, len(df_temp)):
            df_temp['date'] = df_temp.index
        df_word = pd.concat([df_word, df_temp], ignore_index=True)
        #merge each word into one dataframe
        df = pd.merge(df, df_word[['date', keyword]], on=['date'], how='right', copy = True)
        #define month-year variable
        df['date'] = pd.to_datetime(df['date'])
        df['monthly'] = df['date'].dt.strftime('%Y-%m')
        #convert to datetime
        df['monthly'] = pd.to_datetime(df['monthly'], format='%Y-%m')
    return df

#--------------------------------------------------------------------
#Function to create a figure summarizing the relationship between the two terms
#--------------------------------------------------------------------
def scatter_plots(df): 
    fig, ax = plt.subplots(1, 2, figsize=(20, 10))
    sns.scatterplot(x='unemployment', y='inflation', data=df, ax=ax[0])
    sns.lineplot(x='date', y='inflation', data=df, ax=ax[1])
    sns.lineplot(x='date', y='unemployment', data=df, ax=ax[1])
    ax[0].set_title('US Scatter Plot')
    ax[0].set_ylabel('Inflation')
    ax[0].set_xlabel('Unemployment')
    ax[1].set_title('US Line Plot')
    ax[1].set_ylabel('Search Interest')
    plt.setp(ax[1].get_xticklabels(), rotation=45)
    ax[1].legend(['Inflation', '_', 'Unemployment'])
    fig.tight_layout()
    #title the figure 
    
    fig.suptitle('The Tradeoff in Salience of Inflation and Unemployment')
    #add a subtitle
    fig.text(0.5, 0.95, 'U.S.Google Trends Data: April 2020 to April 2022', ha='center', va='top')
    fig.subplots_adjust(top=0.9)    
    plt.show()
    #save the figure
    #fig.savefig('US_Tradeoff.png')


#call the functions
def main():
    #set parameters
    daystart = '2018-04-01'
    dayend = '2022-04-01'
    keywords = ['unemployment', 'inflation', 'economy']
    
    #Define key graphing terms
    sns.set_style('darkgrid')
    sns.set_context('talk')
    sns.set_palette('dark')
    sns.set(font_scale=1.5)
    fig, ax = plt.subplots(figsize=(20, 20))
    
    #Pull Google Trends Data
    trends_df = get_google_trends_US(daystart, dayend, keywords)
    #save trends data to csv
    trends_df.to_csv('trends.csv')

    #Create scatter plots
    scatter_plots(trends_df)
main()