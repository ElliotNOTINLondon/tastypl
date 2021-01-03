#!/usr/bin/python3
"""
This program is a Python implementation of the tastypl [Go](https://golang.org/) program that imports your
[tastyworks](https://tastyworks.com/) transactions and figures out some statistics to help you track your performance
and positions.  The main motivation behind it was to track the net credit after rolls.
"""

from re import sub
from sys import argv
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
sns.set(color_codes=True)
sns.set(palette="deep", font_scale=1.1, color_codes=True, rc={"figure.figsize": [16, 10]})

# Pass csv name as first argument
filename = argv[1]

if __name__ == "__main__":
    # Load portfolio data
    pldata = pd.read_csv(filename)

    # Parse all fees, deposits and withdrawals
    interest = sum(pldata.loc[pldata.Description == "INTEREST ON CREDIT BALANCE"]['Value'].astype(float))
    reg_fees = sum(pldata.loc[pldata.Description == "Regulatory fee adjustment"]['Value'].astype(float))

    deposits = 0
    for deposit_type in ["Wire Funds Received", "ACH DEPOSIT", "ACH DISBURSEMENT"]:
        for deposit in pldata.loc[pldata.Description == deposit_type]['Value']:
            deposits += float(sub(r'[^\d\-.]', '', deposit))
    total_transactions = round(interest + reg_fees + deposits, 2)

    # Read the different symbols
    symbols = []
    for trade in pldata.loc[pldata.Type == 'Trade'].Symbol:
        symbols.append(trade[:].split(' '))
    print(symbols)

    print()
