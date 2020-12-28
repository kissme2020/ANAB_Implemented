# -*- coding: utf-8 -*-
"""
Created on Dec 27 2020

Python Script related to plot


@author: kd Kim

"""

# Futures
from __future__ import print_function

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from myPackage.myFile import Text
from myPackage.myTime import My_timeDate

matplotlib.use('TkAgg')


def save_figure(fig, path, fn,
                ext_str='svg',
                time_tag=True):
    """
    fig: Plot.subplot Object
    path: String path name
    fn: String file name
    ext_str: String file extension, Default is 'png'
    time_tag: Boolean, if True, file name add time tage
              Otherwise not add.
              Default is True
    """

    # Set file name
    f = Text()
    f.set_fields(path, fn, ext_str)
    if (time_tag):
        f.add_file_date_tag()

    fn = f.full_fn
    del f

    fig.savefig(fn, format=ext_str, transparent=True)
    # Fig size changed as set up of dpi
    # fig.savefig(fn, transparent=True, dpi=300)

    return


"""
# Plot Nested Pie Chart for ANAB Capability
"""


def sortSecond(val):
    """
    val: List [PL str, # of ISO support, # of local support]
    Return Second value of list.
           Use for sort key.
    """
    return val[1]


def get_num_limit(alist):
    """
    alist: List [# ISO support, , ...]
    Return number of limit by mean and STD
    """

    # Get Mean and STD
    std = np.std(alist)
    mean = np.mean(alist)
    # print(f'mean: {mean}, std: {std}')

    # Assumed as Normal, Get 95 % confidence level
    z_val = 1.960
    interval = z_val * (std / (len(alist) ** (1/2)))
    if (std <= mean):
        # STD < Mean
        interval = z_val * (std / (len(alist) ** (1/2)))
    else:
        # If STD > Mean
        interval = std - mean

    return int(interval)


def get_select_data_nested_pie(alist):
    """
    alist: List [[pl_str, #  ISO support, # Local Support], [], ...]
    Return List of sting of PL
           Numpy array [[support , not support], [], ...]
           as limit number and local support ratio.
    """

    # Get Limit number
    idx = 1  # index of iso_support
    lim_num = get_num_limit([x[idx] for x in alist])
    print(f'!!! Omits Number less than {lim_num} !!!')

    # Sort list by # of ISO Support
    alist.sort(key=sortSecond, reverse=True)

    pl_str = []  # Placeholder for PL string
    nums = []    # Placeholder for [[total, support, not_support], ]

    # Make pie as even
    for val in alist:
        # Iterate alist
        idx_str = 0  # Index of PL string
        idx_iso = 1  # Index of # ISO
        idx_local = 2  # Index of # Local

        # Get ratio of local support
        ratio = val[idx_local] / val[idx_iso]  # Local support Ratio
        ratio_lim = 0.05  # 5 % Limit

        if ((val[idx_iso] >= lim_num) or
                (ratio >= ratio_lim)):
            # # OF ISO support is limit, OR local support ration over 5 %
            pl_str.append(val[idx_str])  # Append PL String
            # Append [total, support , not support]
            nums.append([val[idx_local],
                         val[idx_iso] - val[idx_local]])

    return pl_str, np.array(nums)


def get_color_map_nest_pie(arr, color_map):
    """
    arr: Numpy array
          [[# of ISO support, # of Local support], [] ...]
    color_map: plt.cm color map
    Return two color plt color map for inner color and outer color
    """

    total = arr.sum(axis=1)

    # Normalize of  the data to 0..1
    # for covering the full range of
    # the colormap, LogNorm show more clear data
    norm = matplotlib.colors.LogNorm(min(total),
                                     max(total))
    # norm = matplotlib.colors.Normalize(0,
    #                                    max(total))
    # print(np.min(total))
    # print(np.max(total))

    # Append inner colors
    inner_colors = []
    for num in total:
        inner_colors.append(color_map(norm(num)))

    # Append outer colors
    outer_colors = []
    for (t, vals) in zip(total, arr):

        outer_colors.append(color_map(
            norm(t)))
        # Color for not support
        outer_colors.append(color_map(
            norm(0)))

    return inner_colors, outer_colors, norm


def get_support_precentage_label(num_array):
    """
    pl_str_list: String of PL
    num_array: Numpy array [[total, support, not support], [], ...]
    Return List of string [xx %, ....]
    """

    percentage_label = []
    for nums in num_array:
        # Iterate num_array

        idx_support = 0  # index of total #
        idx_not_support = 1  # index of support
        # Got String percentage of Local support and Not
        perc_support = (nums[idx_support] /
                        (nums[idx_support] + nums[idx_not_support])) * 100

        if (perc_support == 0):
            # Local support is Zero percent
            percentage_label += ['', '']
        else:
            # Local support is not Zero
            percentage_label += [f'{perc_support:0.0f} %', '']

    return percentage_label


def get_pie_chart_data(arr):
    """
    arr: Numpy array [[# support, # not support]]
    Return same size of len(arr),
           [ratio support, ratio not support]
    """

    pie_data = []  # Placeholder for return value
    for nums in arr:
        # Iterate arr [support, not_support]

        factor = 1.0 / np.sum(nums)  # Get ratio iso_support
        pie_data.append(factor * nums)

    return np.array(pie_data)


def plot_dist_pie(pl_dist,
                  total_vol,
                  c_map_str,
                  path,
                  fn,
                  ext_str='png'):
    """
    pl_vol_dist: List [[PL string, # ISO vol, # Local vol], [] , ....]
    total_vol: int Total Volume
    c_map_str: String of python color map
    path: String, path name to save
    fn: String, file name to save
    ext_str: String, file Extension
    Save Pie chart plot of PL and local Volume Capability ratio
    """

    # Get pl string list and data of [[total, support, not support], ..]
    pl_str, data = get_select_data_nested_pie(pl_dist)
    outer_percentage_label = get_support_precentage_label(data)

    # Get inner, outer and norm (color bar)
    # color_map = plt.cm.BuGn
    color_map = getattr(plt.cm, c_map_str)
    inner_colors, outer_colors, norm = get_color_map_nest_pie(data,
                                                              color_map)

    # plot Pic Chart
    fig, ax = plt.subplots(figsize=(12, 8))

    # create a second axes for the colorbar
    # [x1, y1, delta x , delta y]
    ax2 = fig.add_axes([0.9, 0.1, 0.03, 0.8])

    # Get same size data for Pie Chart same pieces
    pie_data = get_pie_chart_data(data)

    size = 0.1  # Control depth of ling
    startangle = 110  # Start angle, west is 0 degree

    # Outer Ring Ratio of Local support.
    ax.pie(pie_data.flatten(),
           radius=1,
           colors=outer_colors,
           labels=outer_percentage_label,
           # labeldistance=1,
           # textprops={'fontsize': 14, 'color':'b'},
           textprops={'fontsize': 16, 'color': 'b'},
           rotatelabels=True,
           startangle=startangle,
           counterclock=False,
           wedgeprops=dict(width=size, edgecolor='w'))

    # Inner Ring PL Distortion
    ax.pie(pie_data.sum(axis=1),
           radius=1-size,
           colors=inner_colors,
           labels=pl_str,
           labeldistance=(1 - (size + 0.05)),
           # labeldistance=(1 - (size + 0.05)),
           textprops={'fontsize': 14},
           # textprops={'fontsize': 14, 'color': 'dimgray'},
           startangle=startangle,
           counterclock=False,
           wedgeprops=dict(width=size*2, edgecolor='w'))

    ax.set(aspect="equal")

    # Add color bar
    matplotlib.colorbar.ColorbarBase(ax2,
                                     cmap=color_map,
                                     norm=norm,
                                     orientation='vertical')
    plt.show()

    # Save to file
    save_figure(fig, path, fn)

    return


"""
Plot ANAB Order Trend
"""


# Plot job trends
def plot_jobs_trends(total, external, on_site,
                     path, ext_str='png'):
    """
    total_jobs, external_jobs, on_site:
    list of tuple,[(2020 Feb, 10), (), ....]
    path: String, save path
    ext_str: String, save figure file extension, default is 'png'
    Plot trend of internal, on_site and external jobs,
    3 month rolling avg of external jobs
    """

    mytime = My_timeDate()  # Instance the DateTime class

    # Create DF of # of jobs to plot
    # column names for # Jobs
    col_names = ['Date', 'Total', 'External', 'On-Site']
    alist = []  # Placeholder for Iterate result.

    for i in range(len(total)):
        # Iterate total Job by index
        # [[date time, # Total Jobs, # External Jobs, # of On-site Jobs], ...]
        str_format = '%b %Y'  # Format of datetime
        # tmp_list = [DataTime, # Total Job, #  External Job, # of On-site Job]
        tmp_list = [mytime.get_datetime(total[i][0], str_format),
                    total[i][1],
                    external[i][1],
                    on_site[i][1]]
        alist.append(tmp_list)

    del mytime  # Deleted my time

    # Create DF  [month, internal, external]
    df_jobs = pd.DataFrame(alist, columns=col_names)
    # Add 2 month rolling mean of external jobs
    df_jobs['External 3 Month Mean'] = df_jobs['External'].rolling(3).mean()

    fig, ax = plt.subplots(figsize=(12, 8))  # Instance Figure

    # Plot Jobs trend, total, external and on-site
    df_jobs.plot(x='Date', y='Total',
                 linestyle='--', marker='o', ax=ax)
    df_jobs.plot(x='Date', y='External',
                 linestyle='--', marker='o', ax=ax)
    df_jobs.plot(x='Date', y='On-Site',
                 linestyle='--', marker='o', ax=ax)
    df_jobs.plot(x='Date', y='External 3 Month Mean',
                 linestyle='-',  ax=ax)

    # Set individual value above list for Total Jobs, External and On-site
    for i, j in zip(df_jobs['Date'], df_jobs['Total']):
        if (j != 0):
            ax.annotate(str(j), xy=(i, j), color='k', fontsize=16)

    for i, j in zip(df_jobs['Date'], df_jobs['External']):
        if (j != 0):
            ax.annotate(str(j), xy=(i, j), color='k', fontsize=16)

    for i, j in zip(df_jobs['Date'], df_jobs['On-Site']):
        if (j != 0):
            ax.annotate(str(j), xy=(i, j), color='k', fontsize=16)

    # set y-axis label

    # Remove top, right, left axis
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_xlabel('')
    # ax.set_ylabel("# of Jobs", color='b' ,fontsize=16)
    ax.grid(axis='y')
    # ax.set_title('ANAB Jobs', fontsize=20)

    # fig.tight_layout()
    plt.show()

    # Save to file
    fn = 'job_trend'  # Save file name
    save_figure(fig, path, fn)

    return


# Plot Order Trend
def plot_order_trends(order, path, ext_str='png'):
    """
    order: List of tuple [('Q3 2020', 22425242.53), ()  ...]
    path: String, save path
    ext_str: String, save figure file extension, default is 'png'
    """

    # Get list ['Q1', 'Q2', 'Q3', 'Q4']
    years = []
    delta_idx = 3  # Index of year start

    for val in order:
        # iterate order list

        if (val[0][delta_idx:] not in years):
            # year not in year list
            years.append(val[0][delta_idx:])

    years = sorted(years)  # Sort

    col_names = ['YEAR', 'Q1', 'Q2', 'Q3', 'Q4']

    alist = []  # Placeholder for result
    for i in range(len(years)):
        # Iterate year and Insert 0 on each Fiscal Quarter
        alist.append([0 for i in range(len(col_names))])
        # print(years[i])
        alist[i][0] = years[i]

    for val in order:
        # Iterate order fill Order Amount

        # Get year string
        str_year = val[0][delta_idx:]
        # Get quarter string
        str_quarter = val[0][:delta_idx-1]
        # Get Row Index
        row_idx = years.index(str_year)
        # Get Column Index
        col_idx = col_names.index(str_quarter)
        # Store Order amount to corresponded index
        alist[row_idx][col_idx] = val[1]

    # Create DF
    df_order = pd.DataFrame(alist, columns=col_names)
    df_order = df_order.set_index('YEAR')
    # print(df_order.head())

    # Plot order bar chart
    fig, ax = plt.subplots(figsize=(12, 8))     # Instance Figure

    df_order.plot(kind='bar', ax=ax, rot=30)
    currency_factor = 1e-6

    # set individual bar lables using above list
    for p in ax.patches:
        # get_x pulls left or right; get_height pushes up or down
        y_delta = 0.31 / currency_factor
        if (p.get_height() != 0.0):
            i = p.get_x()            # + offset
            j = p.get_height() + y_delta  # .31
            val = p.get_height() * currency_factor

            ax.annotate(f"{val:0.2f} M",
                        xy=(i, j),
                        color='k', fontsize=16)
            # rotation=30)

    # Remove top, right, left axis
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    # ax.set_ylabel("(M) KRW",color='b',fontsize=14)
    # ax.set_title('Order Trend', fontsize = 20)
    ax.set_xlabel('')
    ax.grid(axis='y')

    # fig.tight_layout()
    plt.show()

    # Save to file
    fn = 'Order'  # Save file name

    save_figure(fig, path, fn)

    return


def plot_quality(col_names, quality,
                 path, ext_str='png'):
    """
    col_names: List string, column string related with quality
    quality: List, [['Mar 2020', 2, 0, 0, 0, 0, 0, 1, 5], [],...]
    path: String, save path
    ext_str: String, save figure file extension, default is 'png'
    """

    # Create DataFrame for plotting
    col_names.insert(0, 'Month')
    df = pd.DataFrame(quality, columns=col_names)

    fig, ax = plt.subplots(figsize=(12, 8))
    df.plot(x='Month', y=col_names[1:-1],
            kind='bar', stacked=True,
            rot=30, ax=ax)

    # To annotate % of error on top of stacked bar char

    x = []
    for p in ax.patches:
        # Iterate patches and get x position
        if (p.get_x() not in x):
            x.append(p.get_x())

    y = []
    val = []
    for q in quality:
        # Iterate quality get sum # of error, and percentage of error
        num_sum = sum(q[1:-1])
        y.append(num_sum)
        val.append(100 * (num_sum/q[-1]))

    for i, j, v in zip(x, y, val):
        x_dalta = 0.05
        y_delta = 0.15
        ax.annotate(f"{v:0.1f} %",
                    xy=(i + x_dalta, j + y_delta),
                    color='k', fontsize=16)

    # Remove top, right, left axis
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    # ax.set_ylabel("# of Job",color='b',fontsize=16)
    ax.set_xlabel('')
    # ax.set_title('Quality',fontsize=20)
    ax.grid(axis='y')

    plt.show()

    # Save to file
    fn = 'Quality_trend'  # Save file name
    save_figure(fig, path, fn)

    return


def get_pie(alist, ax):
    """
    alist: List, [(Label, num), (), ....]
    title: String Figure title
    return Pie ax
    """

    labels = []  # Label x-axis
    nums = []    # numbers y_axis
    # explode = [] # Space between pies

    for val in alist[1]:
        # Iterate alist, sprite Label and Number
        labels.append(val[0])
        nums.append(val[1])

    # for num in nums:
    #     # Iterate nums, get space between pies.
    #     num_str = f'{(num/sum(nums))/10 : 0.2f}'
    #     explode.append(float(num_str))

    ax.pie(nums, labels=labels,
           # explode=explode,
           autopct='%1.1f%%',
           textprops={'fontsize': 16, 'color': 'k'},
           startangle=90,
           wedgeprops=dict(width=.15))
    # ax.set_title(alist[0],fontsize=20, color='b')

    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.axis('equal')

    return ax


def plot_distribution(alist,
                      path,
                      ext_str='png'):
    """
    alist: List, [[title_str, [[label,...]]],[num,....]]], [], .....]
    path: String, save path
    ext_str: String, save figure file extension, default is 'png'
    Plot, pie chart for PL and account
    """

    fig, axs = plt.subplots(1, 2, figsize=(12, 8))

    for i in range(len(alist)):
        fig_col_num = 2  # Number of columns on figures
        # row = int(i / fig_col_num)
        col = i % fig_col_num
        axs[col] = get_pie(alist[i], axs[col])

    plt.show()

    # Save to file
    fn = 'Distrinution'  # Save file name
    save_figure(fig, path, fn)

    return
