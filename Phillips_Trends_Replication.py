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
#Function to get google trend data for each state by month, collecting 
# each term separately and merging by date
#--------------------------------------------------------------------
def get_google_trends_separate(daystart, dayend, keywords, states):
    pytrend = TrendReq(hl='en-US', tz=360)
    kw_list = keywords
    df = pd.DataFrame()
    dates = pd.date_range(start=daystart, end=dayend, freq='MS')
    print(dates)
    print(states)
    #make df uniquely identify each date and state
    for date in dates:
        for state in states:
            df['state'] = state   
            df['date'] = date    
    #for each date include all states
    df_word = pd.DataFrame()
    for keyword in keywords:
        for state in states:
            pytrend.build_payload([keyword], cat=0, timeframe=daystart + ' ' + dayend, geo='US-' + state, gprop='')
            df_state = pytrend.interest_over_time()
            df_state['state'] = state
            #Add a date for each row
            for i in range(0, len(df_state)):
                df_state['state'] = state   
                df_state['date'] = df_state.index
            df_word = pd.concat([df_word, df_state], ignore_index=True)
        #merge each word into one dataframe
        df = pd.merge(df, df_word[['state', 'date', keyword]], on=['date', 'state'], how='right', copy = True)
        #define month-year variable
        df['date'] = pd.to_datetime(df['date'])
        df['monthly'] = df['date'].dt.strftime('%Y-%m')
        #convert to datetime
        df['monthly'] = pd.to_datetime(df['monthly'], format='%Y-%m')
    return df


#--------------------------------------------------------------------
#create a table of scatter plots by state, force all to have the same scale
#--------------------------------------------------------------------
def scatter_plots(df, states): 
    fig, ax = plt.subplots(2, 2, figsize=(20, 20))
    ax = ax.flatten()
    for i, state in enumerate(states):
        df_state = df[df['state'] == state]
        sns.scatterplot(x='unemployment', y='inflation', data=df_state, ax=ax[i])
        ax[i].set_title(state)
        ax[i].set_ylabel('Inflation')
        ax[i].set_xlabel('Unemployment')
    fig.tight_layout()
    plt.show()

    fig, ax = plt.subplots(1, 2, figsize=(20, 10))
    sns.scatterplot(x='unemployment', y='inflation', data=df, ax=ax[0])
    sns.lineplot(x='date', y='inflation', data=df, ax=ax[1])
    sns.lineplot(x='date', y='unemployment', data=df, ax=ax[1])
    #Add a key for the lineplot
    ax[1].legend(['Inflation', 'Unemployment'])
    ax[0].set_title('US Scatter Plot')
    ax[0].set_ylabel('Inflation')
    ax[0].set_xlabel('Unemployment')
    ax[1].set_title('US Line Plot')
    ax[1].set_ylabel('Inflation')
    ax[1].set_xlabel('Date')
    fig.tight_layout()
    #title the figure 
    
    fig.suptitle('The Tradeoff in Salience of Inflation and Unemployment')
    #add a subtitle
    fig.text(0.5, 0.95, 'U.S.Google Trends Data: April 2020 to April 2022', ha='center', va='top')
    fig.subplots_adjust(top=0.9)    
    plt.show()
    #save the figure
    #fig.savefig('US_Tradeoff.png')


#--------------------------------------------------------------------
#Create a line plot for the three series by state:
#--------------------------------------------------------------------
def line_plots(df, states):
    fig, ax = plt.subplots(2, 2, figsize=(20, 20))
    ax = ax.flatten()
    for i, state in enumerate(states):
        df_state = df[df['state'] == state]
        sns.lineplot(x='date', y='inflation', data=df_state, ax=ax[i])
        sns.lineplot(x='date', y='unemployment', data=df_state, ax=ax[i])
        sns.lineplot(x='date', y='economy', data=df_state, ax=ax[i])
        ax[i].set_title(state)
        ax[i].set_ylabel('Inflation')
        ax[i].set_xlabel('Date')
    #add a key to the plot
    ax[0].legend(['Inflation', 'Unemployment', 'Economy'])
    #rotate the x axis labels to 60 degrees
    for ax in fig.axes:
        plt.sca(ax)
        plt.xticks(rotation=60)
    fig.tight_layout()
    plt.show()

#--------------------------------------------------------------------
#A function to divide inflation and unemployment data by economy interest data
#--------------------------------------------------------------------
def divide_by_economy(df):
    df['inflation'] = df['inflation'] / df['economy']
    df['unemployment'] = df['unemployment'] / df['economy']
    return df

#call the functions
def main():
    #set parameters
    daystart = '2018-01-01'
    dayend = '2022-01-01'
    keywords = ['unemployment', 'inflation', 'economy']
    interestingstates = ['AL', 'CA', 'WV', 'IL']

    #Define key graphing terms
    sns.set_style('darkgrid')
    sns.set_context('talk')
    sns.set_palette('dark')
    sns.set(font_scale=1.5)
    fig, ax = plt.subplots(figsize=(20, 20))
    
    #Pull Google Trends Data
    trends_df = get_google_trends_separate(daystart, dayend, keywords, interestingstates)
    #save trends data to csv
    trends_df.to_csv('trends.csv')
    trends_df = divide_by_economy(trends_df)
    
    #drop the observation if the economy variable is missing    
    df_merged = df_merged.dropna(subset=['economy'])

    #Create scatter plots
    scatter_plots(df_merged, interestingstates)
main()