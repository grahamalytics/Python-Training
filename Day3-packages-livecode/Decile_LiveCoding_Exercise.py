# -*- coding: utf-8 -*-
"""
Created on Sun Aug 06 18:15:37 2017

@author: glandry
"""

import os
import datetime as dt
import numpy as np
import pandas as pd
import xlsxwriter

## FOOD FOR THOUGHT
# 2. should we insert NA values randomly into the dataset to show how to deal
# 

# let's check the working directory and point it to where our file sits
os.getcwd()

path = 'C:/Users/glandry/Desktop/Python Training'

os.chdir(path)

# read in the our transaction detail file using Panda's read.csv function
# to show off some of Panda's convenience functions, we're going to skip the
# header row and assign column names explicitly
txnDetail = pd.read_csv('AEO_Data_Decile.csv')

# check the data types of each column
txnDetail.dtypes

# there are a few columns containing product-level info that are either 
# too general (i.e. division_descr) , or too granular (i.e. style_descr)
# Since we won't need them, let's drop those columns!
txnDetailSml = txnDetail.drop(['store_key', 'style_cd', 'style_descr', 'division_cd',
                               'division_descr', 'class_cd', 'class_descr',
                               'dept_cd', 'dept_descr'], axis = 1)

# we can rename column names and drop the underscores
txnDetailSml.columns =  ['memberKey', 'txnDate', 'txnHeaderID', 
                         'txnDetailID', 'productKey', 'purchasedQty', 
                         'saleAmnt', 'discAmnt']
                         
# check the structure, description, and first rows of the new txnDetailSml object
txnDetailSml.dtypes
txnDetailSml.describe()
txnDetailSml.head()

# The txnDate is currently stored as a string in the traditional timstamp format
# The time attribute is superfluous, so let's convert the string to a timestamp
# and then strip the timestamp down to date format
txnDetailSml['txnDate'] = pd.to_datetime(txnDetailSml['txnDate'], 
                                         format = '%Y-%m-%d %H:%M:%S').dt.date

# before deciling our customers by total spend, we need to aggregate our 
# txnDetail data at the customer level. Let's do it for each RFM variable

# start by defining function to calculate recency
def recency(df):
    # define the 'anchor date' for calculating recency as max(txnDate) + 1
    anchorDate = df['txnDate'].max() + dt.timedelta(days = 1)
    
    result = (anchorDate- df['txnDate'])
    
    return(result)

# append a txnRecency column to txnDetailSml and convert from timedelta to days
txnDetailSml['txnRecency'] = recency(txnDetailSml)
txnDetailSml['txnRecency'] = txnDetailSml['txnRecency'].dt.days
    
# create RFMdf to store customer aggregations
RFMdf = pd.DataFrame(txnDetailSml[['memberKey', 'txnRecency', 'txnHeaderID',
                                  'saleAmnt', 'discAmnt']])

# Aggregate at customer level, calculating each RFM variable + Discount
# RECENCY
RFMdf['recency'] = RFMdf.groupby(['memberKey'])['txnRecency'].transform('min')

# FREQUENCY
RFMdf['frequency'] = RFMdf.groupby(['memberKey'])['txnHeaderID'].transform('nunique')

# MONETARY
RFMdf['monetary'] = RFMdf.groupby(['memberKey'])['saleAmnt'].transform('sum')

# DISCOUNT
RFMdf['discount'] = RFMdf.groupby(['memberKey'])['discAmnt'].transform('sum')

# now that we've aggregate our RFM + Discount variables, let's keep only
# the columns that we need and drop the rest
RFMdf = RFMdf.drop(['txnRecency', 'txnHeaderID', 'saleAmnt', 'discAmnt'], axis = 1)

# we still have duplicate rows per member and need to keep only unique rows
RFMdf = RFMdf.drop_duplicates()

# Now let's calculate the cutoff points along Monetary before
# assigning value deciles to each customer
deciles = list(RFMdf['monetary'].quantile(q = np.arange(0.1, 1, 0.1), interpolation = 'linear'))

# create a column for decile assignment
RFMdf['decile'] = np.nan

RFMdf = RFMdf.sort_values(['monetary'])

# TO DO make function take two parameters (x, tiles) and then applt
#
def decile_label(x):
    
    # assign values based upon Monetary
    if x < deciles[0]:
        return 1
    elif x < deciles[1]:
        return 2
    elif x < deciles[2]:
        return 3
    elif x < deciles[3]:
        return 4
    elif x < deciles[4]:
        return 5
    elif x < deciles[5]:
        return 6
    elif x < deciles[6]:
        return 7
    elif x < deciles[7]:
        return 8
    elif x < deciles[8]:
        return 9
    else:
        return 10
        
RFMdf['decile'] = RFMdf['monetary'].apply(decile_label)

#       
decileDF = RFMdf[['decile', 'frequency', 'monetary', 'discount']].groupby('decile').sum().reset_index()

decileDF['avgRecency'] = RFMdf[['decile', 'recency']].groupby('decile').mean()

# TO DO ...
# calculate the averaage spend and discount for each decile group


# Write data to Excel file and in the process create a bar chart
# create XLSX writer via Pandas functionality
writer = pd.ExcelWriter('decile_results.xlsx', engine = 'xlsxwriter')

# convert dataframe to XLSLWriter Excel Object
RFMdf.to_excel(writer, sheet_name = 'Deciles', index = False)

# Get workbook and worksheet objects
workbook = writer.book
worksheet = writer.sheets['Deciles']

# add chart to workbook
chart = workbook.add_chart({'type': 'column'})

chart.add_series({
                  'categories': 'distinct()})

worksheet.insert_chart('H3', chart)

# cloase Pandas Excel writer and output info to Excel
writer.save()







