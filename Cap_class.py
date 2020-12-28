# -*- coding: utf-8 -*-
"""
Created on Dec 03 09:55:39 2020

Python Script Populate Korea ANAB Capability

Load worked model from
C:/Users/tskdkim/Current_Job/ANAB/ANAB_Capability/Meta_data/worked_list

Get DF
Agilent Model #,mfg,mfg_Desc,mfg_model,Product_Line,WDB,EOS, # of SO
save to result's "All Models" tabe

Compare to Ref_data's "IOS_SW_SUPPORT" tab
If model in "IOS_SW_SUPPORT" tab
Check "17025/Z540.3  Validation" is "New", "Old"

Agilent Model #,mfg,mfg_Desc,mfg_model,Product_Line,WDB,EOS,
# of SO, Part Number, Family

Save to result "ISO Support" tab

Compare Model  "Kore support"
Add "Korea SUpport","Update date"
on  Agilent Model #,mfg,mfg_Desc,mfg_model,Product_Line,
WDB,EOS, # of SO, Part Number, Family

@author: tskdkim

"""

# Futures
from __future__ import print_function


# Built-in/Generic Imports
# import sys
# Set Model path
# sys.path.insert(1, 'c:/Users/tskdkim/Projects/myPackage')

# Libs
# import os
# import re
# import decimal

# from datetime import datetime
# import importlib
# import numpy as np
# import matplotlib
# import matplotlib.pyplot as plt
import pandas as pd


# from {path} import {class}

# Own modules
from myPackage.myFile import Text
from myPackage.myFile import DF_Excel
from myPackage.myFile import get_fn_in_path
from myPackage.myTime import My_timeDate


def get_fns_worked(path, search_ext_str):
    """
    path: String, path
    search_ext_str: String extension of file to search
    Return file name string only to list
    """
    # Get file name on path exclude extension
    fns = get_fn_in_path(path, search_ext_str)
    return [x.split('.')[0] for x in fns]


def get_df_from_file(path, fn, tab_name):
    """
    Path: String, path name
    fn: String, file name
    tab_name: String, tab name
    Return DataFrame from excel File.
    """

    f = DF_Excel()
    df = f.get_df(path, fn, tab_name)
    del f

    return df


def save_df_to_excel(path, fn,
                     tabs,
                     dfs,
                     need_time_tag):
    """
    path: String path of worked history excel
    fn: String file name
    dfs: List of DF
    tabs: List of tab name string
    need_time_tag: Boolean, if True add time tag end of file string
    Save DF to Excel
    """

    # Save to Excel
    f = DF_Excel()
    f.save_dfs(path, fn,
               tabs,
               dfs,
               need_time_tag)
    del f

    return


def save_ref_worked_file(path, fn,
                         ext_str,
                         nums):
    """
    path: String, path of worked history excel
    fn: String, file name
    ext_str: String, file extension
    nums: Int, number of worked file
    # file format "num_of_worked_file,date,date,nums"
    dfs: List of DF
    tabs: List of tab name string
    Save DF to Excel
    """

    # Get todays date as '%b_%d_%Y'
    str_format = '%b_%d_%Y'
    t = My_timeDate()  # Instance My_timeDate class
    date = t.get_date_time_str_now(str_format)
    del t  # Del My_timeDate class

    alist = [f'num_of_worked_file,{date},{nums}\n']

    # Save to Excel
    f = Text()
    f.save_file(path, fn, ext_str,
                alist)
    del f

    return


def get_all_models(path, fns, col_names):
    """
    path: String, path
    fns: list of file names
    col_names: List of column names
    Return Set of models in worked files
    ['Agilent Model #','mfg','mfg_Desc', # columns worked list
                 'mfg_model','Product_Line',
                 'WDB','EOS','# of SO', ]
    """
    print('\n')
    # f = myF.DF_Excel()    # Instance DF_Excel class
    dfs = []  # Placeholder for worked list df

    # Get Unique Model First
    model_str = []  # Placeholder for model name
    for fn in fns:
        tab_name = 'Sheet1'
        col = col_names[0]
        # Iterate Worked history file and get models
        print(f"Get Models from {fn}.xlsx")
        df = get_df_from_file(path, fn, tab_name)
        model_str += df[col].tolist()
        dfs.append(get_df_from_file(path, fn, tab_name))

    model_str = list(set(model_str))  # Get Unique Models
    # Placeholder for return list
    rtn = [[x, '', '', '', '', '', 1, 0] for x in model_str]

    for df in dfs:
        # Iterate Worked history file
        for model in rtn:
            # Iterate Models
            # Get indices of matched model from DF of worked list
            # Check Length of indices is not zero
            # Add len(indices) to # of SO to last on the model
            # Update last index's information to remind

            indics = (df.loc[df[col] == model[0]].index).tolist()
            if(len(indics) > 0):
                # Model found
                model[-1] += len(indics)  # Add number of SO

                idx = 1
                for col_str in col_names[1:-1]:
                    model[idx] = df[col_str][indics[-1]]
                    idx += 1
    return rtn


def add_iso_sw(path, fn,
               tab_name,
               col_names,
               models):
    """
    path: String, path
    fn: String file name
    tab_name: String tab name
    col_names: List of column names
               ['Model', 'Family', '17025/Z540.3  Validation']
    models: List [['agilent medel' , ......], [],......]
    Remove duplicated model by col name of Family
    Return Set of models in worked files
    """

    df = get_df_from_file(path, fn, tab_name)  # Load ISO SW list as DF

    # Placeholder Dictionary
    # {k(model): [s/w families,...], ['Yes' or 'No' is in ISO list]}
    dic = {model[0]: [[], ''] for model in models}
    max_num_families = 0  # Placeholder for max number of S/W
    for model in dic:
        # Iterate Models

        # Get indices of model in ISO S/W List
        indices = (df[df[col_names[0]] == model].index).tolist()
        idx_sw = 0  # Dictionary item index of Sw list
        idx_validate = 1  # Dictionary item index of validation
        if(len(indices) > 0):
            # If Model support by ISO S/W

            if (len(indices) > max_num_families):
                # Update max num of SW
                max_num_families = len(indices)

            for j in indices:
                # Iterate idx, append S/W
                sw_str = df['Family'][j]
                if sw_str not in dic[model][idx_sw]:
                    # SW is in dic's sw list, append
                    dic[model][idx_sw].append(sw_str)

            dic[model][idx_validate] = "Yes"  # Update SW validation Statues

        else:
            # No model in support SW
            dic[model][idx_validate] = "No"  # Update SW validation Statues

    # Add update S/W and validate statues to model
    for i in range(len(models)):
        # Iterate models to add ISO sws and validate state
        idx_sw = 0  # Dictionary item index of Sw list
        idx_validate = 1  # Dictionary item index of validation
        sw_tmp_list = ['None' for x in range(3)]
        sw_list = dic[models[i][0]][idx_sw]  # List of SW
        for j in range(len(sw_list)):
            # Iterate SW list, insert it at index
            sw_tmp_list[j] = dic[models[i][0]][idx_sw][j]

        # Add sw list at models list
        # Add validate statues at models list
        models[i] += sw_tmp_list
        models[i].append(dic[models[i][0]][idx_validate])

    # Make column names
    new_col_names = [f'Family_{x}' for x in range(max_num_families)]
    new_col_names.append('17025/Z540.3  Validation')
    return new_col_names, models


def add_local_cap(path, fn, tab_name, models):
    """
    path: String, path
    fn: String file name
    tab_name: String tab name
    models: List [['agilent medel', ......], [],......]
    Return list of model added local capability and
    column name added
    """

    df = get_df_from_file(path, fn, tab_name)  # Load DF of Local Capability
    t = My_timeDate()  # Instance My_timeDate Class

    for m in models:
        # Iterate worked model

        # Get index of model in local capability
        indices = (df[df['Model'] == m[0]].index).tolist()

        if (len(indices) > 1):
            # If Indices are more than 1
            print(f'!!! Model {m[0]} Has Duplicate indices {indices} !!!')

        if(len(indices) > 0):
            # Model in Local Capability
            m.append("Y")  # Add Local capability as 'Y'
            m.append(df['Update_Date'][indices[0]])  # Append Update date

            # m.append(t.get_month_name_str(
            #     df['Update_Date'][indices[0]]))  # Add Update as 'mmm yyyy'
            # m.append(t.get_fiscal_quarter_str(
            # df['Update_Date'][indices[0]]))  Add Update as 'Qx 2020'
            # m.append(df['Update_Date'][indices[0]]) # Add Update Date
        else:
            m.append("N")
            m.append("N/A")
    del t  # Deleted My_timeDate Class
    add_col_names = ['Local Capability', 'Update Date']

    return add_col_names, models


def need_update_worked_models(path):
    """
    path: String path of worked history excel
    fn: String file name
    Return True if update need, otherwise False

    # Check previous number of checking file
    # If the previous check file does not exist get all_model
    # Or number of worked file does not match Exit,
    # Reload worked list.
    # else get df from Exits one.
    """

    worked_files_path = f'{path}/Meta_data/worked_list'
    ref_file_path = f'{path}/Python_Output'
    ref_fn = 'worked_file_log'

    ext_str = ''
    # file format "num_of_worked_file,date,date,nums"
    separator_char = ','

    # Load DF of Local Capability
    f = Text()
    result = f.get_file(ref_file_path, ref_fn, ext_str)
    del f

    if(len(result) <= 0):
        # No previous load of worked files.
        return True
    else:
        # Previous worked files Existed
        # Compare previous and current length of worked file
        num_worked_list = result[-1].split(separator_char)
        num_worked_list = num_worked_list[-1]
        num_worked_list = int(num_worked_list)
        # print(num_worked_list)

        # Get num of worked list files
        fns = get_fns_worked(worked_files_path, '.xlsx')
        # print(len(fns))
        print('\n')
        if (len(fns) == num_worked_list):
            # No Changing
            print("No Change in Number of Worked History File")
            print('\n')
            return False
        else:
            # There is change
            print("Change in Number of Worked History File")
            print("Reload files")
            return True


def get_combined_result(path):
    """
    path: String of parent path
    Return combined DF(all_model worked, ISO_SW_support, Local support)
    """

    # Path and files for worked list
    # path is
    # 'C:/Users/tskdkim/Current_Job/ANAB/ANAB_Capability/Meta_data/worked_list'
    # save_path =
    # 'C:/Users/tskdkim/Current_Job/ANAB/ANAB_Capability/Python_Output'

    worked_files_path = f'{path}/Meta_data/worked_list'
    save_path = f'{path}/Python_Output'
    save_fn = 'worked_model'
    save_tab = 'Worked Models'
    ref_fn_num_worked = 'worked_file_log'

    # columns worked list
    col_names = ['Agilent Model #', 'mfg', 'mfg_Desc',
                 'mfg_model', 'Product_Line',
                 'WDB', 'EOS', '# of SO']

    df = None  # Placeholder for Dataframe
    worked_models = None  # Placeholder for result

    if (need_update_worked_models(path)):
        # If there is change in worked history files
        # Load worked list files, turn it to DF, save as excel

        # Get all file name of '.xlsx'
        fns = get_fns_worked(worked_files_path, '.xlsx')

        # Get all model in worked list
        worked_models = get_all_models(worked_files_path,
                                       fns,
                                       col_names)

        # Change 'WBD' and 'Product_Line' to string
        for model in worked_models:
            idx = col_names.index('WDB')
            model[idx] = str(model[idx])
            idx = col_names.index('Product_Line')
            model[idx] = str(model[idx])

        print(f'Length of worked model: {len(worked_models)}')

        # Save to Excel
        df = pd.DataFrame(worked_models, columns=col_names)
        worked_models = df.values.tolist()

        # Save DF to excel
        save_df_to_excel(save_path,
                         save_fn,
                         [save_tab],
                         [df],
                         False)

        # Save ref_fn_of_num_worked
        save_ref_worked_file(save_path,
                             ref_fn_num_worked,
                             '',
                             len(fns))
    else:
        # No Updated worked models Use existed file
        # Load Worked Models Dataframe
        print("!!! No Updated worked excel files !!!")
        print(f"Use {save_fn} as Worked Models")
        df = get_df_from_file(save_path,
                              save_fn,
                              save_tab)
        worked_models = df.values.tolist()

    # Add ISO CAL SW columns
    path = f'{path}/Meta_data'
    fn = 'Ref_data'
    tab_name = 'IOS_SW_SUPPORT'

    iso_col_names = ['Model', 'Family', '17025/Z540.3  Validation']
    new_col_names, worked_models = add_iso_sw(path, fn, tab_name,
                                              iso_col_names, worked_models)
    col_names += new_col_names  # Update col_names
    print(f'Length of worked model after add IOS S/W : {len(worked_models)}')
    # print(col_names)

    # Add local cap, Update col_names
    tab_name = 'Korea_Support'
    new_col_names, worked_models = add_local_cap(path, fn,
                                                 tab_name,
                                                 worked_models)
    col_names += new_col_names
    # print(worked_models[0])
    # print(col_names)
    print(f'Length of worked model after add LOCAL CAP : {len(worked_models)}')

    # Make Two DF, row: all data combined
    # Not_support: model's not support local capability
    df = pd.DataFrame(worked_models, columns=col_names)

    # Append DF, ISO support but not Local support
    col_1 = '17025/Z540.3  Validation'
    cond_1 = 'Yes'
    col_2 = 'Local Capability'
    cond_2_str = 'N'

    df2 = df[(df[col_1] == cond_1) &   # ISO support
             (df[col_2] == cond_2_str)]   # Not Local capability

    # Save to the Excel File
    save_fn = 'Combined'
    save_tab_names = ['ISO SW Support', 'Not Local Support']
    save_df_to_excel(save_path,
                     save_fn,
                     save_tab_names,
                     [df, df2],
                     True)

    print('\n'*10)

    return df


# Help function for ANAB_CAP class
def get_model_num(df, indices):
    """
    df: DataFrame
    indices: List of index
    Return number of unique column value on col
    """

    alist = []  # Placeholder for result
    col = 'Agilent Model #'

    for i in indices:
        if (df[col][i] not in alist):
            alist.append(df[col][i])

    return len(alist)


def add_string_detail(str1, alist):
    """
    str1: String to add and return.
    alist: List [[pl_str, # of ISO, # of local], ...]
    Added string of PL: # ISO, LOCAL, Ratio in str1
    Return str1
    """

    str1 += '\n'

    for vals in alist:
        num_iso = vals[1]
        num_loc = vals[2]
        ratio = num_loc / num_iso
        str1 += f'{vals[0]}, ISO: {num_iso}, LOCAL: {num_loc},\
                   Ratio: {ratio:0.2f}\n'

    return str1


def get_models_support_iso(models, df):
    """
    models: Set of model string to check.
    Date frame: Reference Data Frame
    Return list of models can ISO CAL
           and not support model
    """

    # ecp_str = 'ACC'
    # emp_id_str = 'QEPS1365'
    # entity_str = 'E500'

    col = '17025/Z540.3  Validation'
    iso = 'Yes'
    t_col = 'Agilent Model #'

    ref_models = set(df.loc[(df[col] == iso), t_col].tolist())

    alist = []  # Placeholder for return ISO support model
    not_alist = []  # Placeholder for return ISO not support model

    for model in models:
        if (model in ref_models):
            # Possible ISO CAL
            alist.append(model)
        else:
            not_alist.append(model)

    return alist, not_alist


def get_model_skill_list(model, model_skills):
    """
    model: String model name
    model_skills: List of result to update
    Append list to model_skills
    ['Model','EPC','Employee Id','Entity']
    """

    ecp_str = 'ACC'
    emp_id_str = 'QEPS1365'
    ent_str = 'E500'

    model_skills.append([model, ecp_str, emp_id_str, ent_str])

    return


def get_support_strategy_list(model, eos, support_strategies):
    """
    model: String model name
    eos: Integer, 0 or 1, if 1 than EOS model
    support_strategies: List to append result
    Append list of Support strategy
           ['Entity Site', 'Model', 'SAC Name']
    """

    ent_str = 'E500'
    sac_name_list = None

    if (eos == 1):
        # Model is EOS
        sac_name_list = ['AO - Accredited Cal',
                         'OA - VOSCAL Accredited Cal']
    else:
        # Model is not EOS
        sac_name_list = ['AJ - Tech Eval + Accred Cal',
                         'AO - Accredited Cal',
                         'FG - Rep + Accredited Cal',
                         'UC - Upgrade Installation + Accredited Cal',
                         'OA - VOSCAL Accredited Cal']

    for sac_name in sac_name_list:
        # Iterate sac name
        support_strategies.append([ent_str, model, sac_name])

    return


class ANAB_CAP():
    """
    Class for ANAB Capability Analysis
    """

    def __init__(self, parent_path):
        """
        parent_path: String, path name of parent's path
        """
        # Combined DF of model's worked, ISO_SW_Support,and Local Capability
        self.parent_path = parent_path
        self.df = get_combined_result(parent_path)
        self.pl_models_list = None
        self.pl_vol_list = None
        self.set_pl_model_dist()
        self.set_pl_vol_dist()

    def save_df_Hub_support_Strategy(self, tab_name):
        """
        tab_name: String Excel tab name to Mass update
        Return two df  with two tabs names
               'Support_Strategy_Template'
               'Model_Skills'
        """

        path = f"{self.parent_path}/Meta_data/"  # Path String
        fn = 'Ref_data'  # File Name

        # Get models to update
        col_name = 'Model'
        df = get_df_from_file(path, fn, tab_name)
        col_name = 'Model'

        # Get model Set and support model list and not support model
        models = set(df[col_name].tolist())
        support, not_support = get_models_support_iso(models,
                                                      self.df)

        if (len(not_support) > 0):
            # Not support model exist on models
            # Show model list
            print("!!! There are not ISO support Models !!!")
            for model in not_support:
                # Iterate not supported
                # and print out model
                print(model)

        df_list = []  # Placeholder for Dataframes
        # Add Model Skill
        col_names = ['Model', 'EPC', 'Employee Id', 'Entity']
        alist = []

        for model in support:
            # Iterate model
            get_model_skill_list(model, alist)

        # Append model skills
        df_list.append(pd.DataFrame(alist,
                                    columns=col_names))

        # Add Support Strategy
        col_names = ['Entity Site', 'Model', 'SAC Name']
        alist = []

        for model in support:
            # Iterate model
            # Get EOS statues
            col = 'Agilent Model #'
            t_col = 'EOS'
            eos = self.df.loc[(self.df[col] == model), t_col].item()
            get_support_strategy_list(model, eos,
                                      alist)

        # Append Support strategy
        df_list.append(pd.DataFrame(alist,
                                    columns=col_names))

        # Save as Excel file
        save_path = f"{self.parent_path}/Python_Output"
        fn = "Add_Hub"
        tabs = ["Model_Skills", "Support_Strategy_Template"]

        save_df_to_excel(save_path,
                         fn,
                         tabs,
                         df_list,
                         True)

        return

    def get_num_models(self):
        """
        Return all Model's number in worked history
        """

        col = 'Agilent Model #'

        return len(set(self.df[col].tolist()))

    def get_num_iso_support(self):
        """
        Return # of model ISO support
        """
        col = '17025/Z540.3  Validation'
        iso = 'Yes'

        # Get index of ISO SW support model
        indices = ((self.df[self.df[col] == iso]).index).tolist()

        return get_model_num(self.df, indices)

    def get_num_local_cap(self):
        """
        Return # of local support model
        """
        col = 'Local Capability'
        con_str = 'Y'

        # Get index of Local Capability
        indices = (self.df[self.df[col] == con_str].index).tolist()

        return get_model_num(self.df, indices)

    def get_pl_list(self):
        """
        Return list of PLs ISO support
        """

        # Get DIC Key PL ISO SUPPORT SW
        col = '17025/Z540.3  Validation'  # Condition Column
        iso = 'Yes'            # Condition Column's Condition
        t_col = 'Product_Line'            # Target Column

        pls = list(set((self.df.loc[self.df[col] == iso, t_col].tolist())))

        return sorted(pls)

    def get_pl_total_vol(self):
        """
        Return total volume
        """
        col = '# of SO'
        return self.df[col].sum()

    def get_pl_iso_vol(self):
        """
        Return ISO support volume
        """
        col = '17025/Z540.3  Validation'
        cond = 'Yes'
        col_t = '# of SO'

        return self.df.loc[(self.df[col] == cond),
                           col_t].sum()

    def get_pl_local_vol(self):
        """
        Return Local Support volume
        """
        col = 'Local Capability'
        cond = 'Y'
        col_t = '# of SO'

        return self.df.loc[(self.df[col] == cond),
                           col_t].sum()

    def set_pl_vol_dist(self):
        """
        Set self.pl_vol_dist
        PL iso support job volume vs. local support volume
        """

        # Get SO numbers from PL support ISO
        pls = self.get_pl_list()
        self.pl_vol_list = [[] for x in range(len(pls))]

        # Get Job volume of PLs and local support volume
        for i in range(len(pls)):
            # Iterate Pls
            self.pl_vol_list[i].append(pls[i])  # Add pl String

            # Append ISO Support Volume
            col = '17025/Z540.3  Validation'  # Condition cols
            cond1 = 'Yes'                     # Condition 1
            col2 = 'Product_Line'             # Condition cols 2
            t_col = '# of SO'                 # Target Column
            self.pl_vol_list[i].append(
                self.df.loc[((self.df[col] == cond1) &
                             (self.df[col2] == pls[i])),
                            t_col].sum())

            # Append Local support Volume
            col3 = 'Local Capability'
            cond3 = 'Y'
            self.pl_vol_list[i].append(
                self.df.loc[((self.df[col] == cond1) &
                             (self.df[col2] == pls[i]) &
                             (self.df[col3] == cond3)),
                            t_col].sum())
        return

    def set_pl_model_dist(self):
        """
        Set self.pl_model_dist
            [[pl_str , # iso support, # local support], [], ...]
        PL iso support and Local support
        """

        pls = self.get_pl_list()
        # PL distortion [[pl, models iso support, models loacl support], [],...
        pl_models = [[] for x in range(len(pls))]

        for i in range(len(pls)):
            # Iterate PL

            col = '17025/Z540.3  Validation'  # Condition cols
            cond1 = 'Yes'            # Condition 1
            col2 = 'Product_Line'             # Condition cols 2
            t_col = 'Agilent Model #'         # Target Column
            model = (self.df.loc[((self.df[col] == cond1) &  # ISO Support
                                  (self.df[col2] == pls[i])),   # Same PL
                                 t_col]).tolist()               # Model

            model = list(set(model))  # Remove duplicated Model

            if (len(model) > 0):
                # If Model exist
                pl_models[i].append(pls[i])  # Append PL
                pl_models[i].append(model)   # Append Model

                col = 'Local Capability'   # Condition Column 1
                cond1 = 'Y'                # Condition String
                col2 = 'Product_Line'      # Condition Column 2
                t_col = 'Agilent Model #'  # Target Column

                # Local Support and Same PL than Append
                model = (self.df.loc[(
                    (self.df[col] == cond1) &
                    (self.df[col2] == pls[i])), t_col]).tolist()
                model = list(set(model))  # Remove Duplicated Model
                pl_models[i].append(model)  # Append model

        # Counter # of iso support
        # And local models and append to self.pl_model_list
        self.pl_models_list = []
        for vals in pl_models:
            # Iterate pl_models
            idx_pl_str = 0   # Index of PL string
            idx_iso = 1      # Index of iso_support model's list
            idx_local = 2    # Index of local support model's list
            self.pl_models_list.append(
                [vals[idx_pl_str],
                 len(vals[idx_iso]),
                 len(vals[idx_local])])
        return

    def __str__(self):

        rtn_str = '!!! ANAB Capability Summarize !!!\n'
        rtn_str += '########################################################\n'

        # Add PL Model distribution
        total = self.get_num_models()
        iso_support = self.get_num_iso_support()
        local_num = self.get_num_local_cap()

        rtn_str += '\n'
        rtn_str += 'PL Model Distortion\n'
        rtn_str += f'Total Model: {total}\n'
        rtn_str += f'ISO S/W Support: {iso_support}\n'
        rtn_str += f'Local Capability Model: {local_num}\n'
        rtn_str += f'ISO Support Ratio: {iso_support/total:0.1f}\n'
        rtn_str += f'Local Support Ratio: {local_num/iso_support:0.1f}\n'
        rtn_str += '\n'
        rtn_str = add_string_detail(rtn_str, self.pl_models_list)

        # Add PL volume distortion
        total = self.get_pl_total_vol()
        iso_support = self.get_pl_iso_vol()
        local_num = self.get_pl_local_vol()

        rtn_str += '\n'
        rtn_str += 'PL Volume Distortion\n'
        rtn_str += f'Total Volume: {total}\n'
        rtn_str += f'ISO S/W Support: {iso_support}\n'
        rtn_str += f'Local Capability Volume: {local_num}\n'
        rtn_str += f'ISO Support Ratio: {iso_support/total:0.1f}\n'
        rtn_str += f'Local Support Ratio: {local_num/iso_support:0.1f}\n'
        rtn_str = add_string_detail(rtn_str, self.pl_vol_list)
        rtn_str += '########################################################\n'

        return rtn_str

    def __del__(self):
        print("A ANAB_CAP class is destroyed")
