# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 2020

Script about time Date conversion

@author: tskdkim
"""


# Futures
from __future__ import print_function

# Built-in/Generic Imports
# import sys

# Libs
# import os
# import re
# import decimal

from datetime import datetime
# import numpy as np

# Own modules
# import fileUtility as FU  # my python script file handling
# from {path} import {class}
# […]

__author__ = '{author}'
__copyright__ = 'Copyright {year}, {project_name}'
__credits__ = ['{credit_list}']
__license__ = 'GPL'
__version__ = '{mayor}.{minor}.{rel}'
__maintainer__ = '{maintainer}'
__email__ = 'kissme2020@gmail.com'
__status__ = '{dev_status}'


class My_timeDate:
    """
    Class related to Datetime
    datetime or time stamp to string
    Or string to datetime
    """

    def __init__(self):
        pass

    def get_date_time_str_now(self, str_format):
        """
        str_format: Customer format ex) '%m-%d-%y' etc,
        Return string of Date time now as date_format
        """

        a_date_time = datetime.now()

        return self.get_date_time_str(a_date_time, str_format)

    def get_date_time_str(self, a_date_time, str_format):
        """
        a_date_time: dateTime or time stamp of python
        str_format: Customer format ex) '%m-%d-%y' etc,
        Return string of Date as date_format
        """
        rtn_str = ''

        try:
            # Conversion Python datetime to formated string.
            rtn_str = a_date_time.strftime(str_format)
        except ValueError:
            # str_format is not proper
            print(f"Can't not convert Python datetime \
                  to string format {str_format}")
        finally:
            # Return rtn_str
            return rtn_str

    def get_datetime(self, date_str, str_format):
        """
        date_str: sting, certain format of string of date time
        date_format: Customer format ex) '%m-%d-%y' etc,
        Return Python datetime
        """

        rtn = ''  # Placeholder for return value

        try:
            # Conversion string to Python datetime
            rtn = datetime.strptime(date_str, str_format)
        except ValueError:
            # str_format is not proper
            print(f"Can't not convert {str_format} \
                  formated string to Python datetime")
        finally:
            # Return rtn_str
            return rtn

    def get_month_name_str(self,
                           a_date_time):
        """
        a_datetime: Python datetime
        Return string of year and month name ex) 'Dec 2020'
        """

        year = a_date_time.year
        month_name_str = a_date_time.strftime('%b')

        return f'{month_name_str} {year}'

    def get_fiscal_quarter_str(self,
                               a_datetime,
                               start_month=11):
        """
        a_datetime: Python datetime
        start_month: int, start month of fiscal year
        Return string of Fiscal Quarter
        corresponding to date time sting ex) 'Q1 2020'
        """

        num_month_of_years = 12  # Numbers of month in year
        len_quarter = 3

        # Get year and month from datetime
        year = a_datetime.year
        month = a_datetime.month

        rtn_str = ''  # Placeholder for return string

        # Create quarter list
        quarter_list = []

        for i in range(start_month,
                       start_month + num_month_of_years):

            if (i > num_month_of_years):
                # If i is over 12 than subtract 12 from it
                # and append quarter_list
                quarter_list.append(i - num_month_of_years)
            else:
                # Append i in quarter_list
                quarter_list.append(i)

        # Check year whether make new year or not.
        if (month >= start_month
                and month <= num_month_of_years):
            # If Month is between start month to 12, Add year + 1
            rtn_str = f'{year + 1}'
        else:
            rtn_str = f'{year}'

        # Add quarter string
        for i in range(int(num_month_of_years / len_quarter)):
            # Iterate 4 each three month
            start = i * 3
            stop = start + 3

            if (month in quarter_list[start:stop]):
                # If month is in quarter, make string by i + 1
                rtn_str = f'Q{i+1} {rtn_str}'

        return rtn_str

    def get_list_period_timedate(self, start_str, stop_str,
                                 date_format_str='%Y-%m'):
        """
        start_str: string, start date yyyy-mm
        stop_str: string, stop date yyyy-mm
        date_format_str: string, date format of python
        Return list Python datetime  between start and stop
        """

        start = self.get_datetime(start_str,
                                  date_format_str)

        stop = self.get_datetime(stop_str,
                                 date_format_str)

        year_month_list = []  # Placeholder for result.

        if((stop.year - start.year) == 0):
            # No year difference
            if((stop.month - start.month) == 0):
                # No month difference
                year_month_list.append((start.year, start.month))
            else:
                # Month difference only
                for i in range(start.month, stop.month + 1):
                    year_month_list.append((start.year, i))
        else:
            # year difference >= 1.
            # Append start year and month
            year_month_list.append((start.year, start.month))

            while True:
                # Iterate by increase month
                month = year_month_list[-1][1] + 1

                if (month >= 13):
                    # Month >= 13, year + 1 and month set 1.
                    year_month_list.append((year_month_list[-1][0] + 1,
                                            1))
                else:
                    # Month < 13, month + 1
                    year_month_list.append((year_month_list[-1][0],
                                            month))
                    # print(year_month_list[-1])

                if(year_month_list[-1][0] == stop.year and
                   year_month_list[-1][1] == stop.month):
                    # Increased year and month is the same
                    # as stop year and month
                    # Break While loop
                    break

        rtn_datetimes = []
        for val in year_month_list:
            # Iterate convert tuple (year, month) to Python dateTime
            rtn_datetimes.append(datetime(val[0], val[1], 1))

        return rtn_datetimes

    def __del__(self):
        print("Destructor called, My_timeDate deleted.")


# Test Code for datetime conversion to fiscal quarter

# excel_f =
# 'C:/Users/tskdkim/Current_Job/ANAB/ANAB_CAL_Worked_List/ANAB_CAL_Worked_Log.xlsx'

# tab_name_str = 'LOG'


# df = FU.Create_DF_from_excel(excel_f,
#                              tab_name_str)

# start_date_str = '2020-03'
# stop_date_str = '2020-10'

# """
# ['SO#', 'Model', 'Serial', 'Account', 'PL', 'Cal Date', 'Customer',
#        'Tech #', 'Is_On_site', 'Traceability', 'Procedure', 'Cal_Due', 'LOG',
#        'MU', 'Cats', 'Infoline', 'Is_Error_Fixed', 'R5_50G_511', 'Price Note'
#        'Error Note'],
# """

# date_format_str = '%Y-%m'
# my_time =  My_timeDate()
# start_date_str = '2020-03'
# stop_date_str = '2022-05'

# year_month_list = my_time.get_list_period_timedate(start_date_str,
#                                                    stop_date_str)

# for val in year_month_list:
#     print(my_time.get_fiscal_quarter_str(val))

# print(my_time.get_fiscal_quarter_str(test))
# print(my_time.get_month_name_str(test))
