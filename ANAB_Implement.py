# -*- coding: utf-8 -*-
"""
Created on Dec 27 2020

@author: tskdkim
"""

# Futures
from __future__ import print_function
# […]

# Built-in/Generic Imports
# import sys
# import importlib

# Libs
# import os
# import re
# import decimal

# from datetime import datetime
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd

# Own modules
# from {path} import {class}
from Cap_class import ANAB_CAP
from Order_class import Orders
from plot import plot_dist_pie
from plot import plot_order_trends
from plot import plot_jobs_trends
from plot import plot_quality
from plot import plot_distribution


__author__ = 'KD Kim'
__copyright__ = 'Copyright 2020, ANAB Implemented'
__credits__ = ['KD, Kim']
__license__ = 'GPL'
__version__ = '{0}.{0}.{9}'
__maintainer__ = '{KD, Kim}'
__email__ = 'kissme2020@gmail.com'
__status__ = '{Work on}'


def get_ANAB_cap():
    """
    Get ANAB Local capability
    """

    # Set initial path for load excel and figure save
    path = 'C:/Users/tskdkim/Current_Job/ANAB/ANAB_Capability'
    fig_save_path = path + '/Python_Output/Figs'

    cap = ANAB_CAP(path)
    print(cap)

    # Plot pie chart for Model local capability
    c_map_str = 'Reds'
    fn = 'K_ANAB_MODEL_CAP_PIE'  # Save file name
    plot_dist_pie(cap.pl_models_list,
                  cap.get_pl_total_vol(),
                  c_map_str,
                  fig_save_path,
                  fn)

    # Plot PIE  chart for PL Volume
    c_map_str = 'YlGnBu'
    fn = 'K_ANAB_VOLUME_CAP_PIE'  # Save file name
    plot_dist_pie(cap.pl_vol_list,
                  cap.get_pl_total_vol(),
                  c_map_str,
                  fig_save_path,
                  fn)

    return


def get_Order_trend():
    """
    Get ANAB Order Trend
    """
    path = 'C:/Users/tskdkim/Current_Job/ANAB/ANAB_jobs'
    source_path = path + '/Meta_data'
    fn = 'ANAB_CAL_Job_Log'
    tab_name = 'LOG'

    fig_path = path + '/python_output/Figs'
    order = Orders(source_path, fn, tab_name)
    print(order)

    # Plot Jobs trend
    total, external, on_site = order.get_order_num_trend()
    plot_jobs_trends(total, external, on_site,
                     fig_path)

    # Plot order trend
    plot_order_trends(order.get_order_amount_trend(False), fig_path)

    # Plot Quality Trend
    col_names, quality = order.get_quality_list()
    plot_quality(col_names, quality, fig_path)

    # print out PL distribution, Model in PL, and account list
    pls, pl_dic = order.get_pl_dist()
    # models = my_order.get_model_dist()
    accounts = order.get_account_dist()

    alist = [['PL', pls],
             ['Account', accounts]]

    plot_distribution(alist, fig_path)

    return


def get_Hub_support(tab_name):
    """
    tab_name: String Excel tab name to Mass update
    Return two df  with two tabs names
           'Support_Strategy_Template'
           'Model_Skills'
    """

    path = 'C:/Users/tskdkim/Current_Job/ANAB/ANAB_Capability'

    cap = ANAB_CAP(path)
    cap.save_df_Hub_support_Strategy(tab_name)

    return


def main():
    """
    Main Function
    """

    get_ANAB_cap()

    # tab_name = 'Test'
    # get_Hub_support(tab_name)

    # get_order_trend()

    return


# Code execution
main()
