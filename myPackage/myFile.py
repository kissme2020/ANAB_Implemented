# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 19:24:53 2019

Related to file
include csv or text

2020/11/27: First version up

@author: kdkim
"""

# Futures
from __future__ import print_function
# […]

# Built-in/Generic Imports
import os
# import sys
from pathlib import Path
# […]

# Libs
import pandas as pd  # Or any other
import csv
# import glob
# […]

# Own modules
from myPackage.myTime import My_timeDate


# from {path} import {class}
# […]

__author__ = 'KD Kim'
__copyright__ = 'Copyright {year}, {project_name}'
__credits__ = ['{credit_list}']
__license__ = 'GPL'
__version__ = '0.0.1'
__maintainer__ = 'KD Kim'
__email__ = 'kissme2020@gmail.com'
__status__ = '{dev_status}'


# Help function
def get_parent_path(path):
    """
    path: String path
    Return parent path string
    """
    path = Path(path)

    return (path.parent)


def get_path_name(fn):
    """
    fn: string file name with full path .
    Return path name only
    """

    return os.path.dirname(fn)


def create_path(fn):
    """
    fn: string file name with full path
    Create path if path does not exist
    """

    dir = get_path_name(fn)

    if not os.path.exists(dir):
        os.mkdir(dir)

    return


def is_file_exist(fn):
    """
    fn: String, file name include path
    """

    return os.path.isfile(fn)


def get_fn_in_path(path, find_str=None):
    """
    path: string of path name
    find_str: string, to match in the file name.
              default is None
    Return list of all file name include sub path
    """

    all_fn_list = []  # Placeholder for all file name string
    for root, dir, files in os.walk(path):
        for filesname in files:
            all_fn_list.append(filesname)

    if (find_str is not None):
        return [x for x in all_fn_list if (find_str) in x]
    else:
        return all_fn_list


def get_full_fn(path, fn):
    """
    fn: string as file name.
    path: String path name, "/../../"
    Return file name with include full path name as string.
    """

    return os.path.join(path, fn)


def get_fn_only(fn):
    """
    fn: string, file name with full path
    Return file name only
    """

    path, fn = os.path.split(fn)

    return fn


# def Get_all_fn_from_dic(path, fn_extension_type):
#     """
#     path: string, of path
#     fn_extension_type: string file extension to select
#     """
#     str_of_extension = "**/*{0}".format(fn_extension_type)
#     files = [f for f in glob.glob(path + str_of_extension, recursive=True)]
#     return files


class File():
    """
    Abstract class of file
    """

    def __init__(self):
        """
        path: String, path
        fn: String, file name only without extension
        ext: String, file extension without '.'
        """
        self.fn = ''
        self.path = ''
        self.ext = ''
        self.full_fn = ''  # file name, abs path + file name + extension

    def add_file_date_tag(self):
        """
        fn: string, file name only not include extension
        Return Add nows date time tag on the tail of file name.
        """

        str_format = '%b_%d_%Y_%H_%M'  # Date time string format

        # Instance My_Time Class
        # add time tag on self.fn,
        # del My_Time Class
        t = My_timeDate()
        self.fn = f'{self.fn}_{t.get_date_time_str_now(str_format)}'
        del t

        self.set_full_fn()

        return

    def set_fields(self, path, fn, ext):
        """
        path: string, path
        fn: string, file name without extension
        ext: string, file's extension
        Set self field, path and fn
        """

        self.path = path
        self.fn = fn
        self.ext = ext
        self.set_full_fn()

        return

    def get_fileName(self):

        return self.fn

    def get_path(self):

        return self.path

    def get_ext(self):

        return self.ext

    def get_abs_path(self):
        """
        Return Absolute Path string
        """

        return get_path_name(self.full_fn)

    def set_full_fn(self):
        """
        Set self.full file name
        """
        self.full_fn = f'{self.path}/{self.fn}.{self.ext}'
        return

    def is_file_exist(self):
        """
        If file exist, return True, otherwise False
        """

        return os.path.isfile(self.full_fn)

    def read(self):
        """
        Abstract method, defined by convention only
        Read file
        """
        tmp_str = self.__name__
        tmp_str += "Subclass must implement 'read' abstract method"
        raise NotImplementedError(tmp_str)

    def write(self):
        """
        Abstract method, defined by convention only
        Read file
        """
        tmp_str = self.__name__
        tmp_str += "Subclass must implement 'write' abstract method"
        raise NotImplementedError(tmp_str)

    def __str__(self):

        rtn_str = f'Path: {self.path}\n'
        rtn_str += f'File Name: {self.fn}\n'
        rtn_str += f'extention: {self.ext}\n'
        rtn_str += f'Full File Name: {self.full_fn}'

        return rtn_str

    def __del__(self):
        print("A File class is destroyed")


class DF_Excel(File):
    """
    Derive Class of File
    Read/Write python DataFrame to excel
    """

    def __init__(self):
        File.__init__(self)
        self.ext = 'xlsx'

    def set_fields(self, path, fn):
        """
        path: string, path
        fn: string, file name without extension
        ext: string, file's extension
        Set self field, path and fn
        """

        self.path = path
        self.fn = fn
        self.set_full_fn()

        return

    def get_df(self, path, fn, tab_name):
        """
        path: string, file path
        fn: string, file name without extension
        tab_name = string, name of tab to load
        Load Excel and return it as Python DataFrame
        """

        self.set_fields(path, fn)  # Set path file name

        # Check file exists
        if not self.is_file_exist():
            print(f'{self.full_fn} Does Not exist !!!')
            return
        else:
            rtn = None
            with open(self.full_fn, 'rb') as f:
                rtn = pd.read_excel(f,
                                    sheet_name=tab_name,
                                    engine='openpyxl')  # Excel to DataFrame
            f.close()

        # Filling a null values using fillna()
        rtn.fillna("N/A", inplace=True)

        return rtn

    def save_dfs(self, path, fn,
                 tabs, dfs,
                 is_date_tag=False):
        """
        path: string, file path
        fn: string, file name without extension
        tabs: list of string, tab names
        dfs: list of DataFrame
        is_date_tag: Boolean,
                     If true,
                     add data time tag end of file name '%b_%d_%Y_%H_%M
                     Otherwise, use file name.
        Save to Excel file
        """

        self.set_fields(path, fn)  # Set path file name

        if (is_date_tag):
            # Add tie tag on end of file name
            self.add_file_date_tag()

        # Path does not exist, Create path
        create_path(self.full_fn)

        if (len(tabs) != len(dfs)):
            # If length of tabs and dfs, print error and return
            print('Length of Tab name and DataFrame Not Match')
            print('Cannot Save DataFrame to Excel File')
            return

        writer = pd.ExcelWriter(self.full_fn, engine='xlsxwriter')

        # Open excel write
        for i in range(len(tabs)):
            # Iterate sheet name and dfs
            dfs[i].to_excel(writer,
                            sheet_name=tabs[i],
                            index=False)
        writer.save()

        return


class Text(File):
    """
    Derive Class of File
    Read/Write python DataFrame to excel
    """

    def __init__(self):
        File.__init__(self)
        self.ext = ''
        self.encode_str = 'utf-8'

    def get_file(self, path, fn, ext_str):
        """
        path: String, file path
        fn: String, file name without extension
        ext_str: String, extension string
        Read file and Return list as line
        """

        rtn = []  # Placeholder for result return

        # Set path file name
        self.set_fields(path, fn, ext_str)

        # Check file exists
        if not self.is_file_exist():
            print(f'{self.full_fn} Does Not exist !!!')
            return rtn
        else:
            with open(self.full_fn, 'r', encoding=self.encode_str) as f:
                # File open
                lines = f.readlines()  # Read Lines on file.

                for line in lines:
                    # Iterate lines
                    rtn.append(line.rstrip())  # Remove '\n'

        return rtn

    def save_file(self, path, fn, ext_str,
                  alist):
        """
        path: String, file path
        fn: String, file name without extension
        ext_str: String, extension string
        alist: List of string
        Read file and Return list as line
        """

        self.set_fields(path, fn, ext_str)  # Set path file name

        with open(self.full_fn, 'a', encoding=self.encode_str) as f:
            for val in alist:
                f.write(val)

        return


def ReadCSV(fn, delimiterStr=','):
    """
    Read csv file
    return as a string list.
    fn: file name
    """
    result = []  # s alist of result.
    with open(fn, encoding='utf-8-sig') as csv_file:
        csv_read = csv.reader(csv_file, delimiter=delimiterStr)
        for raw in csv_read:
            result.append(raw)

    return result


def ReadText(fn):
    """
    Read Text file line by line
    fn: string of file name.
    Return [line0, line1, ....]
    """
    rtnList = []
    # data = open('info.txt', encoding='utf-8-sig')
    with open(fn, mode='r', encoding='utf-8-sig') as reader:
        lines = reader.readlines()
        for line in lines:
            rtnList.append(line.rstrip())

    return rtnList


def WriteText(fn, aList):
    """
    Write as text file
    aList is string list.
    """
    with open(fn, 'w', encoding='utf-8-sig') as f:
        for item in aList:
            f.write("{0}\n".format(item))

    return


def Save_as_CSV(fn, alist, delimiterStr=';'):
    """
    Write as csv file
    alist is string list.
    """

    for i in range(len(alist)):  # Iterate list
        tmp_str = ''
        if (len(alist[i]) == 1):  # ? length is over 1.
            tmp_str = tmp_str + alist[i]
        else:
            for j in range(len(alist[i])):
                if (j != (len(alist[i])-1)):
                    print("{0}:{1}".format(alist[i][j], type(alist[i][j])))
                    tmp_str += alist[i][j] + delimiterStr
                else:
                    tmp_str += alist[i][j]
    return


# # Function test code

# path = 'C:/Users/tskdkim/Current_Job/
# ANAB/cmc_current/Network/RF_Power_Relative_PNA/'
# alist = get_fn_in_path(path, '.xlsx')
