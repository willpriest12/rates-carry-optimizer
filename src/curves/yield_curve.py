# -*- coding: utf-8 -*-
"""
Created on Mon Sep  1 17:56:35 2025

@author: willp
"""

import matplotlib.pyplot as plt

class YieldCurve:
    '''Object to represent a single treasury yield curve at a point in time'''
    
    def __init__(self,date,data):
        '''parameters: 
            date: pd.Timestamp - the date of the curve
            data: pd.Series - a pandas Series where index = maturities (eg '2Y', '10Y') and values = yields in %'''
        self.date = date
        self.data = data
        
    def __repr__(self):
        '''overwritten repr method'''
        return f"YieldCurve(date={self.date.date()}, tenors={list(self.data.index)})"
    
    def get_rate(self, tenor: str):
        '''return yield for given tenor'''
        return self.data.get(tenor, None)
    
    def plot(self, ax=None):
        '''Plot the curve with maturities on x-axis and yields on y=axis'''
        if ax is None:
            fig, ax = plt.subplots()
        self.data.plot(marker='o', ax=ax)
        ax.set_title(f"Treasury Yield Curve - {self.date.date()}")
        ax.set_ylabel("Yield (%)")
        ax.set_xlabel("Maturity")
        ax.grid(True)
        return ax