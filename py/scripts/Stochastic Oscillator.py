import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
import statsmodels.api as sm

#use the Engle-Granger method to test cointegration
#underlying method is straight forward, easy to implement

#estimate the long-run equilibrium

def EG_Method(X,Y,show_summary=False):

    #step1
    #estimate the long-run equilibrium

    model1=sm.OLS(Y,X).fit()
    epsilon=model1.resid

    if show_summary:
        print('\nStep1\n')
        print(model1.summary())

    #check p value of augumented dickey fuller test
    #if p value < 0.05, stationary test is passed
    if sm.tsa.stattools.adfuller(epsilon)[1]<0.05:
        return False,model1
    
    #take first order difference of X and Y plus lagged residuals from step 1
    X_dif=sm.add_constant(pd.concat([X.diff(),epsilon.shift(1)],axis=1).dropna())
    Y_dif=Y.diff().dropna()

    #step 2
    #estimate error correction model
    model2=sm.OLS(Y_dif,X_dif).fit()

    if show_summary:
        print('\nStep2\n')
        print(model2.summary())

    # adjustment coefficient must be negative
    if list(model2.params)[-1]>0:
        return False,model
    else:
        return True,model
    

#verofy status of cointegration by observing historical datasets
#bandwith=number of data points for consideration
#bandwidth is 250 by default
#when z-stat crosses above the upper bound
#we long the bearish one, and short the bullish one, vice versa
def signal_generation(asset1,asset2,method,bandwidth=250):

    signals=pd.DataFrame()
    signals['asset1']=asset1['Close']
    signals['asset2']=asset2['Close']

    #signals only imply holding
    signals['signals1']=0
    signals['signals2']=0

    #initialize
    prev_status=False
    signals['z']=np.nan
    signals['z upper limit']=np.nan
    signals['z lower limit']=np.nan
    signals['fitted']=np.nan
    signals['residual']=np.nan

    #signal processing
    for i in range(bandwidth,len(signals)):
        
        #cointegration test
        coint_status,model=method(signals['asset1'].iloc[i-bandwidth],
                                  signals['asset2'].iloc[i-bandwidth])
        
        
        #cointegration breaks
        #clear existing positions
        if prev_status and not coint_status:
            if signals.at[signals.index[i-1],'signals1']!=0:
                signals.at[signals.index[i],'signals1']=0
                signals.at[signals.index[i],'signals2']=0
                signals['z'].iloc[i:]=np.nan
                signals['z upper limit'].iloc[i:]=np.nan
                signals['z lower limit'].iloc[i:]=np.nan
                signals['fitted'].iloc[i:]=np.nan
                signals['residual'].iloc[i:]=np.nan

        #cointegration starts
        #set the trigger conditions
        #performed to minimize calculation performed in pandas
        if not prev_status and coint_status:

            #predict the price to compute the residual
            signals['fitted'].iloc[i:]=model.predict(sm.add_constant(signals['asset1'].iloc[i:]))
            signals['residual'].iloc[i:]=signals['asset2'].iloc[i:]-signals['fitted'].iloc[i:]

            #normalize residual to get z stat
            signals['z'].iloc[i:]=(signals['residual'].iloc[i:]-np.mean(model.resid))/np.std(model.resid)

            #create thresholds
            #one sigma is conventional threshold for trading
            #two sigma reaches 95%, difficult to trigger typically
            signals['z upper limit'].iloc[i:]=signals['z'].iloc[i]+np.std(model.resid)
            signals['z lower limit'].iloc[i:]=signals['z'].iloc[i]-np.std(model.resid)

            #z stat cannot exceed upper and lower thresholds at same time
            #line below hold

            if coint_status and signals['z'].iloc[i]>signals['z upper limit'].iloc[i]:
                signals.at[signals.index[i],'signals1']=1
            if coint_status and signals['z'].iloc[i]<signals['z lower limit'].iloc[i]:
                signals.at[signals.index[i],'signals1']=-1

            prev_status=coint_status

        #signals only imply holding
        #we take the first order difference to obtain execution signal
        signals['positions1']=signals['signals1'].diff()

        #only need to generate trading signal of one asset
        #other one should move in the opposite direction
        signals['signals2']=-signals['signals1']
        signals['postions2']=signals['signals2'].diff()
    
        return signals 