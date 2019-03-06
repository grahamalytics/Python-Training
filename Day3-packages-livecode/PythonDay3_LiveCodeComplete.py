# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 15:53:49 2017

@author: glandry
"""

# these are the packages we will be using
import os
import pandas as pd
import numpy as np

# TO DO ... READ DATA__________________________________________________________
# 
## we're reading in a .CSV file, and Pandas has some helpful I/O functions
txnDetail = pd.read_csv('AEO_Data_Decile.csv')


# TO DO ... INSPECT DATA_______________________________________________________
#
## look at the contents of the df: column names, data types,  values?
## just the perfect function for this was demonstrated during Day 2!
txnDetail.info()

## preview the first 10 rows of the df
txnDetail.head(10)

## return some basic summary statistics to the console
## HINT: this is another one of those 'meta' functions
txnDetail.describe()


# TO DO ... AGGREGATE DATA____________________________________________________
#
## before quintiling our customers based upon their total spend, we first need
## to aggregate the txnDetail data at the customer level
## create a new df which contains the 'member_key' and 'total_spend' columns
## retain ''member_key' as a column and rename 'sale_amnt' to 'total_spend'
memberSpend = txnDetail[['member_key', 'sale_amnt']].groupby('member_key', as_index = False).sum().rename(columns = {'sale_amnt': 'total_spend'})

## sort memberSpend by 'total_spend' descending
memberSpend = memberSpend.sort_values('total_spend', ascending = False)


# TO DO ... CALCULATE QUINTILE CUTOFF POINTS___________________________________
# Is there a quantile method for Pandas df?
# HINT: look at the Numpy arange() function and see if you can calculate all
# the quintile cutoff points in one line of code
quintiles = memberSpend['total_spend'].quantile(q = np.arange(start = 0.2, stop = 1.0, step = 0.2))


# TO DO ... LABEL CUSTOMERS BASED UPON QUINTILE GROUP__________________________
# let's assume we'll need to perform this operation time and time again
# a great opportunity to define a function! Assign a quintile label
# to each customer based upon customers' total spend
# think about how you will use/extract elements from the 'quintiles' object
def quintile_label(x):
    if x <= quintiles.iloc[0]:
        return '1'
    elif x <= quintiles.iloc[1]:
        return '2'
    elif x <= quintiles.iloc[2]:
        return '3'
    elif x <= quintiles.iloc[3]:
        return '4'
    else:
        return '5'
    
# apply your new function to the 'total_spend' column of the memberSpend df
# HINT: the first word of the comment above might be a useful method to use
memberSpend['quintile'] = memberSpend['total_spend'].apply(quintile_label)


# TO DO ... WRITE REULTS_______________________________________________________
# now that we have aggregated total spend at the customer level and assigned a
# quintile label to each customer, write the results back to disk
# for the sake of cleanliness, drop the df index when you write results
# might this be an argument to the file write method?
memberSpend.to_csv('memberQunitiles.csv', index = False)


# TO DO ... CHECK YOUR WORK____________________________________________________
#
## return the average spend per customer per quintile in order to verify
## that your program is working correctly
memberSpend.groupby('quintile').mean()['total_spend']