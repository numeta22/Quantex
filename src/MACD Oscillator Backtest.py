import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf


#moving averages
ma1 = 12
ma2 = 26


#simple moving average
def macd(signals):

    signals['ma1']=signals['Close'].rolling(window=ma1,min_periods=1,center=False).mean()
    signals['ma2']=signals['Close'].rolling(window=ma2,min_periods=1,center=False).mean()

    return signals


#signal generation
def signal_generation(df,method):

    signals=method(df)
    signals['positions']=0

    #positions becomes and stays one once short moving average crosses above long moving average
    signals['positions'][ma1:]=np.where(signals['ma1'][ma1:]>=signals['ma2'][ma1:],1,0)

    #take the difference to generate real trade signal
    signals['signals']=signals['positions'].diff()

    #oscillator is difference between two movign averages
    signals['oscillator']=signals['ma1']-signals['ma2']
    return signals


#plotting the backtesting result
def plot(new, ticker):
    
    fig=plt.figure()
    ax=fig.add_subplot(111)

    new['Close'].plot(label=ticker)
    ax.plot(new.loc[new['signals']==1].index,new['Close'][new['signals']==1],label="LONG",lw=0,marker='^',c='g')
    ax.plot(new.loc[new['signals']==-1].index,new['Close'][new['signals']==-1],label="SHORT",lw=0,marker='v',c='r')

    plt.legend(loc='best')
    plt.grid(True)
    plt.title('Positions')
    
    plt.show()

    #the second plot is long/short moving average with oscillator
    #we are using a bar chart for oscillator

    fig=plt.figure()
    cx=fig.add_subplot(211)

    new['oscillator'].plot(kind='bar',label='oscillator',color='r')

    plt.legend(loc='best')
    plt.grid(True)
    plt.xticks([])
    plt.xlabel('')
    plt.title('MACD Oscillator')

    bx=fig.add_subplot(212)

    new['ma1'].plot(label='ma1')
    new['ma2'].plot(label='ma2',linestyle=':')

    plt.legend(loc='best')
    plt.grid(True)
    plt.show()

def main():

#input the long moving average and short moving average period
#for the classic MACD, it is 12 and 26
#define the global variables

    global ma1,ma2,stdate,eddate,ticker,slicer

    ma1=int(input('ma1:'))
    ma2=int(input('ma2:'))
    stdate=input('start date in format yyyy-mm-dd:')
    eddate=(input('end date in format yyyy-mm-dd:'))
    ticker=input('ticker:')



    #slicing the downloaded dataset
    slicer=int(input('slicing:'))

# 
#downloading the data
    df=yf.download(ticker,start=stdate,end=eddate)

    new=signal_generation(df,macd)
    new=new[slicer:]
    plot(new, ticker)


if __name__ == '__main__':
    main()

## Reference:
'https://github.com/je-suis-tm/quant-trading/blob/master/MACD%20Oscillator%20backtest.py'
