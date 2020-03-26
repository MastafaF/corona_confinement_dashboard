import pandas as pd
import io
import requests
import datetime


# thank you to @kinghelix and @trevormarburger for this idea
def get_date_list(dates):
	return [date.strftime('%-m/%-d/%y') for date in dates]


def get_time_series(local=True):

	ts = {}
	if local == False:
		time_series_files = {
	'Confirmed':'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Confirmed_archived_0325.csv',
	'Deaths': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Deaths_archived_0325.csv',
	'Recovered': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Recovered_archived_0325.csv'
}
	else:
		time_series_files = {
	    	'Confirmed':'data/time_series_19-covid-Confirmed.csv',
	    	'Deaths': 'data/time_series_19-covid-Deaths.csv',
	    	'Recovered': 'data/time_series_19-covid-Recovered.csv'
		}
	print(time_series_files['Confirmed'])
	confirmed = pd.read_csv( time_series_files['Confirmed'])
	deaths = pd.read_csv( time_series_files['Deaths'])
	recovered = pd.read_csv( time_series_files['Recovered'])

	start_date = pd.to_datetime('01/22/2020')
	end_date = pd.to_datetime('today')
	dates = pd.date_range(start_date, end_date)
	valid_dates = []
	for date in dates:
		if date.strftime('%-m/%-d/%y') in confirmed.columns:
			valid_dates.append(date)

	return confirmed, deaths, recovered, valid_dates



def get_confinement_time_series(local=True):
	ts = {}
	if local == False: # TODO: do like below
		time_series_files = {
	    	'Confirmed':'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv',
	    	'Deaths': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv',
	    	'Recovered': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'
		}
	else:
		time_series_files = {
	    	'confinement':'data/df_confinement.tsv'
		}

	confinement = pd.read_csv( time_series_files['confinement'], sep = '\t' )

	start_date = pd.to_datetime('01/22/2020')
	end_date = pd.to_datetime('today')
	dates = pd.date_range(start_date, end_date)
	valid_dates = []
	for date in dates:
		if date.strftime('%-m/%-d/%y') in confinement.datetime:
			valid_dates.append(date)

	return confinement, valid_dates


def get_daily_reports(local=True):
	start_date = pd.to_datetime('01/22/2020')
	end_date = pd.to_datetime('today')
	dates = pd.date_range(start_date, end_date)
	daily_reports = {}
	all_reports = []
	if local == True:
		print('Getting daily reports using local data')
		for date in dates:
			date_str = date.strftime('%m-%d-%Y')
			file_name = 'data/' + date_str + '.csv'
			try:
				df = pd.read_csv(file_name, header=0)
				df['Date'] = date_str
				all_reports.append(df)
			except:
				print("Failed to load {file}".format(file=file_name))
	elif local == False:
		print('Getting daily reports using on-line data')
		daily_report_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
		for date in dates:
			# File format: 'MM-DD-YYYY.csv'
			date_str = date.strftime('%m-%d-%Y')
			file_name =date_str + '.csv'
			url = daily_report_url + file_name
			#print(url)
			try:
				df = pd.read_csv(url, header=0)
				df['Date'] = date_str
				all_reports.append(df)
			except:
				print("Failed to load {file}".format(file=file_name))
	daily_reports = pd.concat(all_reports, axis=0, ignore_index=True)
	daily_reports.Date = pd.to_datetime(daily_reports['Date'])
	daily_reports['Last Update'] = pd.to_datetime(daily_reports['Last Update'])
	valid_dates = df.Date.unique()
#	valid_dates = [pd.to_datetime(date) for date in list(daily_reports.keys())]
	return daily_reports, valid_dates

def make_country_labels(by_cases=True, data=None):
    if by_cases == False:
        countries = sorted(data['Country/Region'].drop_duplicates())
    elif by_cases == True:
    	countries = list(data.groupby('Country/Region').sum().iloc[:,-2].sort_values(ascending=False).index)

    return [{'label': 'Global', 'value': 'Global'}] + [{'label': country, 'value': country} for country in countries]

def make_state_labels(by_cases=True, data=None):
	if by_cases == False:
		states = sorted(data['State'].drop_duplicates())
	elif by_cases == True:
		states = list(data.groupby('State').sum().iloc[:,-2].sort_values(ascending=False).index)
	return [{'label': 'National', 'value': 'National'}] + [{'label': state, 'value': state} for state in states]

