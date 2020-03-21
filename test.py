"""

Test how to group by date in our dataframe

We want to have for each day:
Mean Value
Max-Min Value
Max Value

"""

import pandas as pd
import numpy as np
from dateutil import parser
import datetime
# datetime.datetime.strptime(your_string, "%Y-%m-%dT%H:%M:%S.%f")
# time_now_str = datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")
# parser.parse("Aug 28 1999 12:00AM")

df = pd.read_csv("./data/df_confinement.tsv", sep='\t')
# print(df.datetime.strftime("%m"))
# df['date_parsed'] = df['datetime'].apply(parser.parse)
# print(type(df.loc[0,'datetime']))
def get_datetime(str_datetime):
    """
    From a string time in our dataframe, we want an object datetime
    :param str_datetime:
    :return:
    """
    return(datetime.datetime.strptime(str_datetime, "%d-%m-%Y_%I-%M-%S_%p"))

df['datetime_parsed'] = df['datetime'].apply(get_datetime)
df = pd.DataFrame(df.loc[:,['country','city', 'datetime_parsed', 'nb_detected']])
df.index = df['datetime_parsed']
print(df.index.day)
print(np.unique(df.index.day))
# print("HERE")
# print(pd.DataFrame(df_groups.nb_detected.mean()))
# print("HERE")





# print(df_groups.groups.keys())
# df_groups_Stockholm = df_groups.get_group((21,'Stockholm'))
# print(df_groups_Stockholm)
# print(df_groups_Stockholm.nb_detected.mean())
# print(df_groups_Stockholm.nb_detected.max())
# print(df_groups_Stockholm.nb_detected.std())
#
# def filter_groups(df_groups, city='Stockholm'):
#     """
#     :param city:
#     :return:
#     """
#     arr_df_groups = []
#     for key in df_groups.groups.keys():
#         if key[1] == city:
#             arr_df_groups.append(df_groups.get_group(key))
#     return arr_df_groups
# #
# df_all_groups_Stockholm = filter_groups(df_groups, city = 'Stockholm')
# print(df_all_groups_Stockholm[0].nb_detected.mean())
# print(df_all_groups_Stockholm[0].nb_detected.max())
# print(df_all_groups_Stockholm[0].nb_detected.std())


