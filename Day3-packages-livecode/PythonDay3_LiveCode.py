# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 15:53:49 2017

@author: glandry
"""

# these are the packages we will be using
import os
import pandas as pd
import numpy as np

# TO DO ... SETUP______________________________________________________________
#
## check the working directory (HINT: is there a function within the os module?)


## create a variable named 'path' containing filepath to 'AEO_Data_Decile.csv'
## as a character string


## now set your working directory to the location represented in 'path' variable



# TO DO ... READ DATA__________________________________________________________
# 
## we're reading in a .CSV file, and Pandas has some helpful I/O functions



# TO DO ... INSPECT DATA_______________________________________________________
#
## look at the contents of the df: column names, data types,  values?
## just the perfect function for this was demonstrated during Day 2!


## preview the first 10 rows of the df


## return some basic summary statistics to the console
## HINT: this is another one of those 'meta' functions



# TO DO ... AGGREGATE DATA____________________________________________________
#
## before quintiling our customers based upon their total spend, we first need
## to aggregate the txnDetail data at the customer level
## create a new df which contains the 'member_key' and 'total_spend' columns
## retain ''member_key' as a column and rename 'sale_amnt' to 'total_spend'


## sort memberSpend by 'total_spend' descending



# TO DO ... CALCULATE QUINTILE CUTOFF POINTS___________________________________
# Is there a quantile method for Pandas df?
# HINT: look at the Numpy arange() function and see if you can calculate all
# the quintile cutoff points in one line of code



# TO DO ... LABEL CUSTOMERS BASED UPON QUINTILE GROUP__________________________
# let's assume we'll need to perform this operation time and time again
# a great opportunity to define a function! Assign a quintile label
# to each customer based upon customers' total spend
# think about how you will use/extract elements from the 'quintiles' object



    
# apply your new function to the 'total_spend' column of the memberSpend df
# HINT: the first word of the comment above might be a useful method to use



# TO DO ... WRITE REULTS_______________________________________________________
# now that we have aggregated total spend at the customer level and assigned a
# quintile label to each customer, write the results back to disk
# for the sake of cleanliness, drop the df index when you write results
# might this be an argument to the file write method?



# TO DO ... CHECK YOUR WORK____________________________________________________
#
## return the average spend per customer per quintile in order to verify
## that your program is working correctly
