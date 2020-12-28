# -*- coding: utf-8 -*-
"""
Class for ANAB Order analysis

Source EXCEL file name: 'C:/Users/tskdkim/
Current_Job/ANAB/ANAB_CAL_Worked_List.xlsx'
tab name: 'LOG'

column names:

['SO#', 'Model', 'Serial', 'Account', 'PL', 'Cal Date', 'Customer',
       'Tech #', 'Is_On_site', 'Traceability', 'Procedure', 'Cal_Due', 'LOG',
       'MU', 'Cats', 'Infoline', 'Error Note', 'R5_50G_511(KRW)',
       'Close Month', 'Close Fiscal Quarter']

1. Load as Pandas data frame
2. Add close month and fiscal quarter
3. Get order trend by month or by Fiscal Quarter

@author: tskdkim
"""


# Futures
from __future__ import print_function

# built-in/Generic Imports
# import sys
# import importlib

# Libs
# import os
# import re
# import decimal

# from datetime import datetime
# import numpy as np
# import matplotlib
# import matplotlib.pyplot as plt
# import pandas as pd

# Own modules
# Set Model path
# sys.path.insert(1,
# 'c:/Users/tskdkim/Python/Metrology_Work/my_python_funtions/src')
# sys.path.insert(2,
# 'c:/Users/tskdkim/Python/Metrology_Work/Measurement_uncertainty/src')

# from {path} import {class}
from myPackage.myFile import DF_Excel  # my python script file handling
from myPackage.myTime import My_timeDate

# […]


# Class help function
def add_datetime_column(df, col_str):
    """
    df: Python DataFrame of ANAB cal jobs
    col_str: string, column name of cal done date
    Add two column of Fiscal Close Quarter and Month on the Python DataFrame
    and Return it.
    """

    mytime = My_timeDate()  # Instance the DateTime class

    # Placeholder for close month and fiscal quarter

    close_month_list = []
    close_fiscal_quarter_list = []

    for date in df[col_str]:
        close_month_list.append(mytime.get_month_name_str(date))
        close_fiscal_quarter_list.append(mytime.get_fiscal_quarter_str(date))

    df['Close Month'] = close_month_list
    df['Close Fiscal Quarter'] = close_fiscal_quarter_list

    del mytime

    return df


def get_period_list(start, stop, is_month=True):
    """
    start and stop: Python pandas time stamp of start and stop
    is_month: boolean, If True return set as month,
              otherwise return as Fiscal Quarter
    """

    datetime_format_str = '%Y-%m'

    mytime = My_timeDate()  # Instance the DateTime class

    # Convert timeDate to string of fromat '%Y-%m'
    start_str = mytime.get_date_time_str(start,
                                         datetime_format_str)
    stop_str = mytime.get_date_time_str(stop,
                                        datetime_format_str)

    datetime_list = mytime.get_list_period_timedate(start_str,
                                                    stop_str,
                                                    datetime_format_str)

    rtn_list = []  # Placeholder for result return

    for datetime in datetime_list:
        if(is_month):
            # If monthly
            rtn_list.append(mytime.get_month_name_str(datetime))
        else:
            # If fiscal quarterly
            rtn_list.append(mytime.get_fiscal_quarter_str(datetime))

    del mytime

    if (not is_month):
        # If Fiscal Quarterly period
        # Remove duplicated
        rtn_list = list(set(rtn_list))

    return rtn_list


class Orders:
    """
    Class related to ANAB Closed Order
    """

    def __init__(self, path, fn, tab):
        """
        path: String, path name
        source_file: String, excel file name
        tab: string, tab name
        """
        self.path = path
        self.fn = fn
        self.tab = tab
        self.price_ratio = 1.585
        # ['Traceability','Procedure','Cal_Due','LOG','MU','Cats','Infoline']
        self.quality_list = ['Traceability', 'Procedure',
                             'Cal_Due', 'MU', 'Cats', 'Infoline']

        self.set_df()

    def set_df(self):
        '''
        source_file: string, excel file name
        tab: string, tab name
        Load DF from excel
        Add column for 'ClosedMonth' and 'ClosedFiscalQuarter'
        '''

        # col_name = 'Cal Date'

        # Load excel file to DF
        f = DF_Excel()
        df = f.get_df(self.path, self.fn, self.tab)
        # df = FU.Create_DF_from_excel(self.source_f,
        #                              self.tab_name)
        del f
        # Add close month and close fiscal quarter columns
        self.df = add_datetime_column(df, 'Cal Date')

        # Sort by Cal Date
        self.df.sort_values(by=['Cal Date'], inplace=True)

        return

    def get_num_total(self):
        """
        Return number of total order
        """
        return len(self.df)

    def get_num_extrnal(self):
        """
        Return number of external order
        """

        return (self.df.Customer != 'Internal').sum()

    def get_num_on_site(self):
        """
        Return number of on-site jobs
        """

        return (self.df['Is_On_site'].sum())

    def get_order_num_trend(self, is_monthly=True):
        """
        is_monthly: boolean, if True, get monthly trend,
                    otherwise Fiscal Quarterly Trend
        Return external and internal list of tuple
        [(month string, num of order in month), (), ....]
        """

        period_list = get_period_list(self.df['Cal Date'][0],
                                      self.df['Cal Date'][len(self.df)-1],
                                      is_monthly)

        total = []
        external = []
        on_site = []

        # Select column name by is_monthly
        col_name = ''
        if(is_monthly):
            col_name = 'Close Month'
        else:
            col_name = 'Close Fiscal Quarter'

        for period in period_list:
            # Iterate period_list
            col = 'Customer'
            col_con = 'Internal'

            # Append total Job
            total.append((period,
                          len(self.df.loc[(self.df[col_name] == period)])))

            # Append External Job
            external.append((period,
                             len(self.df.loc[(self.df[col_name] == period) &
                                             (self.df[col] != col_con)])))

            # Append On-site Job
            on_site.append((period, len((self.df.loc[
                (self.df[col_name] == period) &
                (self.df['Is_On_site'] == 1)]))))

        # print(period_list)
        return total, external, on_site

    def get_order_amount_trend(self, is_monthly=True):
        """
        is_monthly: boolean, if True, get monthly trend,
                    otherwise Fiscal Quarterly Trend
        Return external order amount
        [(month string, order_amount), (), ....]
        """

        period_list = get_period_list(self.df['Cal Date'][0],
                                      self.df['Cal Date'][len(self.df)-1],
                                      is_monthly)

        # print(period_list)

        order_amount = []

        # Select column name by is_monthly
        col_name = ''
        if(is_monthly):
            col_name = 'Close Month'
        else:
            col_name = 'Close Fiscal Quarter'

        for period in period_list:
            col = 'R5_50G_511(KRW)'
            order_amount.append((period,
                                 self.df.loc[
                                     (self.df[col_name] == period) &
                                     (self.df['Customer'] != 'Internal'),
                                     col].sum() * self.price_ratio))
        return order_amount

    def get_pl_dist(self):
        """
        Return # of order by PL
        and models in PL of external customer.
        """

        # Get list of PL
        pls = set(self.df.loc[(self.df['Customer'] != 'Internal'),
                              'PL'].to_list())

        pl_models_dic = {}
        pl_num_list = []
        for pl in pls:
            # Iterate PL on df

            # Get number of order in PL
            pl_num_list.append((pl,
                                len(self.df.loc[(self.df['Customer'] !=
                                                 'Internal') &
                                                (self.df['PL'] == pl)])))
            # Get models in PL
            pl_models_dic[pl] = set(self.df.loc[(self.df['PL'] == pl) &
                                                (self.df['Customer']
                                                 != 'Internal'),
                                                'Model'].to_list())

        return pl_num_list, pl_models_dic

    def get_account_dist(self):
        """
        Return # of order by account
        """

        # Get account of PL
        accounts = set(self.df.loc[(self.df['Customer'] != 'Internal'),
                                   'Account_2'].to_list())

        rtn_list = []

        for account in accounts:
            # Iterate account_list on df

            # Get # of account
            rtn_list.append((account,
                             len(self.df.loc[(self.df['Customer']
                                              != 'Internal') &
                                             (self.df['Account_2']
                                              == account)])))

        return rtn_list

    def get_model_dist(self):
        """
        Return # of order by model
        """

        # Get model
        models = set(self.df.loc[(self.df['Customer'] != 'Internal'),
                                 'Model'].to_list())

        rtn_list = []

        for model in models:
            # Iterate account_list on df

            # Get # of model
            rtn_list.append((model,
                             len(self.df.loc[(self.df['Customer']
                                              != 'Internal') &
                                             (self.df['Model'] == model)])))

        return rtn_list

    def get_quality_list(self, is_monthly=True):
        """
        Return Quality Error
        """

        period_list = get_period_list(self.df['Cal Date'][0],
                                      self.df['Cal Date'][len(self.df)-1],
                                      is_monthly)

        rtn_list = []

        # Select column name by is_monthly
        col_name = ''
        if(is_monthly):
            col_name = 'Close Month'
        else:
            col_name = 'Close Fiscal Quarter'

        for period in period_list:
            # Iterate by period
            tmp_list = [period]
            for val in self.quality_list:
                # Iterate quality list, append # Job violated quality
                tmp_list.append(self.df.loc[(self.df[col_name] == period),
                                            val].sum())

            # Append Total # of job on period
            tmp_list.append(len(self.df.loc[(self.df[col_name] == period)]))
            rtn_list.append(tmp_list)

        # Add total in quality_list
        col_names = self.quality_list + ['Total']

        return col_names, rtn_list

    def __str__(self):
        """
        Return self.df information
        Print summarize report.
        """

        # # of Jobs
        rtn_str = f"Period From {self.df['Close Month'][0]} To \
                    {self.df['Close Month'][len(self.df)-1]} \n"
        rtn_str += '\n'
        rtn_str += f"Total ANAB Cal Jobs: {len(self.df)} \n"

        # By  Internal / external order
        a_set = set(self.df['Customer'])
        for customer in a_set:
            rtn_str += f"{customer}:  \
                         {(self.df.Customer == customer).sum()} \n"

        # On-site job Ratio on external job
        num = self.df.Is_On_site.sum() / (self.df.Customer != 'Internal').sum()
        rtn_str += f"Ratio On Site Job: {num:0.1f}\n"

        # Order
        rtn_str += '\n'
        num_external_orders = (self.df.Customer != 'Internal').sum()
        total_order_amount = self.df['R5_50G_511(KRW)'].sum()
        total_order_amount *= self.price_ratio
        price_per_unit = total_order_amount / num_external_orders
        rtn_str += f"Price Rate: {self.price_ratio}\n"
        rtn_str += f"Total order amount: {total_order_amount:.0f} KRW\n"
        rtn_str += f"Price per Unit: {price_per_unit:.0f} KRW\n"

        rtn_str += '\n'
        a_set = set(self.df['Account'])
        for account in a_set:
            rtn_str += f"{account}:  {(self.df.Account == account).sum()} \n"

        # Error Rate
        rtn_str += '\n'
        num = (self.df.Is_Error == 'Y').sum()
        rtn_str += f"Quality Error Ratio: {num/len(self.df):.1f} \n"

        return rtn_str

    def __del__(self):
        print("Destructor called, Orders deleted.")


"""
Test Code
"""
# main()

# # Reload Model
# importlib.reload(myT)
# importlib.reload(myF)

# path = 'C:/Users/tskdkim/Current_Job/ANAB/ANAB_jobs'
# source_path = path + '/Meta_data'
# fn = 'ANAB_CAL_Job_Log'
# tab_name = 'LOG'

# fig_path = path + '/python_output/Figs'

# my_order = Orders(source_path, fn, tab_name)

# # Plot Jobs trend
# total, external, on_site = my_order.get_order_num_trend()
# plot_jobs_trends(total, external, on_site,
#                  fig_path)

# # Plot order trend
# plot_order_trends(my_order.get_order_amount_trend(False), fig_path)

# # Plot Quality Trend
# col_names, quality = my_order.get_quality_list()
# plot_quality(col_names, quality, fig_path)

# # print out PL distribution, Model in PL, and account list
# pls, pl_dic = my_order.get_pl_dist()
# models = my_order.get_model_dist()
# accounts = my_order.get_account_dist()

# alist = [['PL', pls],
#          ['Account', accounts]]

# plot_distribution(alist, fig_path)

# # # Print summary information
# print('\n'*20)
# print(my_order)
# del my_order
