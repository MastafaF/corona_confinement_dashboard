from functions import (
	get_time_series, get_time_series_new, get_daily_reports, get_date_list
	, make_country_labels, get_county_reports
	)
from config import config
import pandas as pd
import numpy as np
import datetime
from scipy import stats


##### Drowdown values to be selected ########
city_Sweden_arr = ['Stockholm', 'Goteborg']
city_Sweden_labels = [{'label': city, 'value': city} for city in city_Sweden_arr]

confirmed, deaths, time_series_dates = get_time_series_new(local=config['LOCAL'])
daily_report_data, daily_dates = get_daily_reports(local=config['LOCAL'])
# confined_df, confined_dates = get_confinement_time_series(local=config['LOCAL'])
# print("CONFINEMENT DATRAFRAME")
# print(confined_df)

county_data, county_dates = get_county_reports()


time_series_date_list = get_date_list(time_series_dates)
daily_date_list = daily_dates.tolist()

from model import doubling_time, growth_rate

confirmed_totals = confirmed.groupby('Country/Region').sum()
death_totals = deaths.groupby('Country/Region').sum()
# recovered_totals = recovered.groupby('Country/Region').sum()

new_confirmed = confirmed_totals[confirmed_totals.columns[2:]].diff(axis=1)
# new_recovered = recovered_totals[recovered_totals.columns[2:]].diff(axis=1)
new_deaths = death_totals[death_totals.columns[2:]].diff(axis=1)

case_mortality = death_totals/confirmed_totals
# case_recovery = recovered_totals/confirmed_totals

countries = confirmed_totals.index

case_rate = growth_rate(df=confirmed_totals)
death_rate = growth_rate(df=death_totals)

case_doubling = doubling_time(case_rate)
death_doubling = doubling_time(death_rate)

data = []
for country in countries:
    for date in time_series_date_list:
        data.extend(
            [dict(
                country=country,
                state='Nation',
                date=date,
                variable='confirmed',
                value=confirmed_totals.loc[country, date]
            ),
            dict(
                country=country,
                state='Nation',
                date=date,
                variable='deaths',
                value=death_totals.loc[country, date]
            ),
            # dict(
            #     country=country,
            #     state='Nation',
            #     date=date,
            #     variable='recovered',
            #     value=recovered_totals.loc[country, date]
            # ),
            dict(
                country=country,
                state='Nation',
                date=date,
                variable='new_confirmed',
                value=new_confirmed.loc[country, date]
            ),
            dict(
                country=country,
                state='Nation',
                date=date,
                variable='new_deaths',
                value=new_deaths.loc[country, date]
            ),
            # dict(
            #     country=country,
            #     state='Nation',
            #     date=date,
            #     variable='new_recovered',
            #     value=new_recovered.loc[country, date]
            # ),
            dict(
                country=country,
                state='Nation',
                date=date,
                variable='case_rate',
                value=case_rate.loc[country, date]
            ),
            dict(
                country=country,
                state='Nation',
                date=date,
                variable='death_rate',
                value=death_rate.loc[country, date]
            ),
            dict(
                country=country,
                state='Nation',
                date=date,
                variable='case_mortality',
                value=case_mortality.loc[country, date]
            ),
            # dict(
            #     country=country,
            #     state='Nation',
            #     date=date,
            #     variable='case_recovery',
            #     value=case_recovery.loc[country, date]
            # ),
            dict(
                country=country,
                state='Nation',
                date=date,
                variable='case_doubling',
                value=case_doubling.loc[country, date]
            ),
            dict(
                country=country,
                state='Nation',
                date=date,
                variable='death_doubling',
                value=death_doubling.loc[country, date]
            )
            ])

data_df = pd.DataFrame.from_dict(data)

# Adding our dataset
confinement_df = pd.read_csv("./data/df_confinement.tsv", sep='\t')
def get_datetime(str_datetime):
    """
    From a string time in our dataframe, we want an object datetime
    :param str_datetime:
    :return:
    """
    return(datetime.datetime.strptime(str_datetime, "%d-%m-%Y_%I-%M-%S_%p"))

# Changing each string datetime into a datatime object that we can manipulate
confinement_df['datetime_parsed'] = confinement_df['datetime'].apply(get_datetime)
confinement_df = pd.DataFrame(confinement_df.loc[:,['country','city', 'datetime_parsed', 'nb_detected']])
confinement_df.index = confinement_df['datetime_parsed']
confinement_df_groups = confinement_df.groupby(by=[confinement_df.index.day, confinement_df.city])

def filter_groups(df_groups, city='Stockholm'):
    """
    :param city:
    :return:
    """
    arr_df_groups = []
    for key in df_groups.groups.keys():
        if key[1] == city:
            arr_df_groups.append(df_groups.get_group(key))
    return arr_df_groups

# @TODO: change get_confinement_time_series to return the below instead of confined_dates
# this array should be an array of the exact days of the month, here it will only give us number
# Like 21 but we have no idea from which month it is ==> @TODO: keep month and year information
# before
# datetime_confinement_arr = np.unique(confinement_df.index.day)
# after -> we want the days with more information in the format DAY-MONTH-YEAR
datetime_confinement_arr = np.unique(confinement_df.index.strftime('%-m/%-d/%y'))
# print(datetime_confinement_arr)

label_dict = dict(
    confirmed='Total Confirmed Cases',
    deaths='Total Deaths',
    # recovered='Total Recovered Cases',
    new_confirmed='New Confirmed Cases',
    new_deaths='New Deaths',
    # new_recovered='New Recovered Cases',
    case_rate='Percent Increase in Confirmed Cases',
    death_rate='Percent Increase in Deaths',
    case_mortality='Cumulative Case Mortality Rate',
    # case_recovery='Cumulative Case Recovery Rate',
    case_doubling='Doubling Time for Confirmed Cases',
    death_doubling='Doubling Time of Deaths'
)

variable_dict = {}
for variable, label in label_dict.items():
	variable_dict[label] = variable

dates = np.array(
	[datetime.datetime.strptime(date, '%m/%d/%y') for date in data_df.date.unique()])
date_strings = [date.strftime('%-m/%-d/%y') for date in dates]

country_labels = make_country_labels(data=confirmed)

old_confirmed, old_deaths, old_recovered, time_series_dates = get_time_series(local=config['LOCAL'])


print("TIME SERIES DATE LIST ORIGINAL")
print(time_series_date_list)


def confinement_by_area(country='Sweden', col = 'country', df=None):
    data = pd.Series(
        [df.loc[df[col] == country][date].mean() for date in confined_dates]
    )
    print("DATA BY AREA")
    print(data)
    return data

# Creating our dataframe with mean,max,std values of our detected number of people
def make_data_confinement(city = 'Stockholm'):
    if city == None or city == 'Stockholm': # default value is Stockholm
        city = 'Stockholm'
        df_all_groups_city = filter_groups(confinement_df_groups, city=city)
        mean_nb_detected = [df_group.nb_detected.mean() for df_group in df_all_groups_city]
        max_nb_detected = [df_group.nb_detected.max() for df_group in df_all_groups_city]
        std_nb_detected = [df_group.nb_detected.std() for df_group in df_all_groups_city]
        df = pd.DataFrame(
            data={
                'mean_nb_detected': mean_nb_detected,
                'max_nb_detected': max_nb_detected,
                'std_nb_detected': std_nb_detected
            }, index=datetime_confinement_arr)
    else:
        df_all_groups_city = filter_groups(confinement_df_groups, city=city)
        mean_nb_detected = [df_group.nb_detected.mean() for df_group in df_all_groups_city]
        max_nb_detected = [df_group.nb_detected.max() for df_group in df_all_groups_city]
        std_nb_detected = [df_group.nb_detected.std() for df_group in df_all_groups_city]
        df = pd.DataFrame(
            data={
                'mean_nb_detected': mean_nb_detected,
                'max_nb_detected': max_nb_detected,
                'std_nb_detected': std_nb_detected
            }, index=datetime_confinement_arr)
    return df

# Creating our dataframe with mean,max,std values of our detected number of people
def make_data_hourly_confinement(city = 'Stockholm'):
    def get_hour(str_datetime):
        """
        From a string time in our dataframe, we want an object datetime
        :param str_datetime:
        :return: hour
        """
        return(datetime.datetime.strptime(str_datetime, "%d-%m-%Y_%I-%M-%S_%p").hour)

    def get_date(str_datetime):
        """
        From a string time in our dataframe, we want an object datetime
        :param str_datetime:
        :return: day-month-year
        """
        return(datetime.datetime.strptime(str_datetime[:10], "%d-%m-%Y"))

    def get_hourly_data(df, city):
        # get date of observation
        date_of_study = get_date(df.max(axis = 0).datetime)

        # create a column with date
        df['datetime_parsed'] = df['datetime'].apply(get_date)
        # filter city
        df = df.where(df.city == city)
        # filter day
        df = df[df.datetime_parsed == date_of_study]
        #create a column with hours
        df['datetime_hour'] = df['datetime'].apply(get_hour)
        #group by hours and apply mean
        hourly_data = df.groupby([df.datetime_hour]).mean()
        return hourly_data.nb_detected.values, hourly_data.index.map(lambda x : int(x)), date_of_study

    confinement_hourly_df = pd.read_csv("./data/df_confinement.tsv", sep='\t')

    if city == None or city == 'Stockholm': # default value is Stockholm
        city = 'Stockholm'
        mean_nb_detected, hour_confinement_arr, date_of_study = get_hourly_data(confinement_hourly_df, 'Stockholm')
        df = pd.DataFrame(
            data={
                'mean_nb_detected': mean_nb_detected
            }, index=hour_confinement_arr)
    else:
        mean_nb_detected, hour_confinement_arr, date_of_study= get_hourly_data(confinement_hourly_df, city)
        df = pd.DataFrame(
            data={
                'mean_nb_detected': mean_nb_detected
            }, index=hour_confinement_arr)
    return df, date_of_study



def data_by_area(area='US', col='Country/Region', df=None):
	data =pd.Series(
		[df.loc[(df[col] == area)][date].sum() for date in time_series_date_list],
		)
	return data

def make_data_global(country='Global'):
    if country == None or country == 'Global':
        df = pd.DataFrame(
            data={
                'confirmed': [confirmed[date].sum() for date in time_series_date_list],
                'deaths': [deaths[date].sum() for date in time_series_date_list],
                # 'recovered': [recovered[date].sum() for date in time_series_date_list]
            }, index=time_series_date_list)
    else:
        df = pd.DataFrame(
        data={
            # These dictionaries need to include lists, not pd.Series!
            # 'recovered': data_by_area(area=country, df=recovered).tolist(),
            'confirmed': data_by_area(area=country, df=confirmed).tolist(),
            'deaths': data_by_area(area=country, df=deaths).tolist()
        }, index=time_series_date_list)
    return df

def make_data_state(state='National', limit=28):
    if state == None or state == 'National':
        df = pd.DataFrame(
            data={
                'confirmed': [us_confirmed[date].sum() for date in time_series_date_list],
                'deaths': [us_deaths[date].sum() for date in time_series_date_list],
                # 'recovered': [us_recovered[date].sum() for date in time_series_date_list]
            }, index=time_series_date_list)
    else:
        df = pd.DataFrame(
            data={
            # 'recovered': data_by_area(area=state, df=us_recovered, col='State').tolist(),
            'confirmed': [us_confirmed[us_confirmed.index == state][date].values[0] for date in time_series_date_list],
            'deaths': [us_deaths[us_deaths.index == state][date].values[0] for date in time_series_date_list]
        }, index=time_series_date_list)
    return df.iloc[limit:,:]

	
def compute_correlation(df_nb_detected, df_nb_cases):
    """
    Computes the Spearman Rank Correlation factor between the column df_nb_detected and df_nb_cases
    :param df_nb_detected: df['nb_detected'] = pd.Series
    :param df_nb_cases: df['nb_cases'] = pd.Series
    :return: float = Spearman Rank Correlation
    """
    # res = (spearman_rank, p_value_are_the_random_variables_correlated)
    res = stats.spearmanr(list(df_nb_detected), list(df_nb_cases))
    return res[0]
