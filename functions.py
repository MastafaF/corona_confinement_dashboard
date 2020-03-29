import pandas as pd
import io
import requests
import datetime


# thank you to @kinghelix and @trevormarburger for this idea
def get_date_list(dates):
	return [date.strftime('%-m/%-d/%y') for date in dates]


remote_time_series_files = {
	'Confirmed':'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Confirmed_archived_0325.csv',
	'Deaths': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Deaths_archived_0325.csv',
	'Recovered': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Recovered_archived_0325.csv'
}

local_time_series_files = {
			'Confirmed':'data/time_series_19-covid-Confirmed_archived_0325.csv',
			'Deaths': 'data/time_series_19-covid-Deaths_archived_0325.csv',
			'Recovered': 'data/time_series_19-covid-Recovered_archived_0325.csv'
		}

remote_time_series_files_new = {
			'Confirmed': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
			'Deaths': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
}

local_time_series_files_new = {
			'Confirmed': 'data/time_series_covid19_confirmed_global.csv',
			'Deaths': 'data/time_series_covid19_deaths_global.csv'
}

def get_time_series(local=True):

	ts = {}
	if local == False:
		time_series_files = remote_time_series_files
	else:
		time_series_files = local_time_series_files
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


def get_time_series_new(local=True):

	ts = {}
	if local == False:
		time_series_files = remote_time_series_files_new
	else:
		time_series_files = local_time_series_files_new

	confirmed = pd.read_csv( time_series_files['Confirmed'])
	deaths = pd.read_csv( time_series_files['Deaths'])
	# recovered = pd.read_csv( time_series_files['Recovered'])

	start_date = pd.to_datetime('01/22/2020')
	end_date = pd.to_datetime('today')
	dates = pd.date_range(start_date, end_date)
	valid_dates = []
	for date in dates:
		if date.strftime('%-m/%-d/%y') in confirmed.columns:
			valid_dates.append(date)

	return confirmed, deaths, valid_dates


def get_county_reports():
	daily_reports, valid_dates = get_daily_reports(start_date=pd.to_datetime('03/22/2020'))

	county_reports = daily_reports[daily_reports['Country_Region'] == 'US']
	return county_reports, valid_dates



def get_daily_reports(local=True, start_date=pd.to_datetime('01/22/2020')):
	daily_report_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
	end_date = pd.to_datetime('today')
	dates = pd.date_range(start_date, end_date)
	daily_reports = {}
	all_reports = []
	for date in dates:
			date_str = date.strftime('%m-%d-%Y')
			file_name =date_str + '.csv'
			if local == True:
#				print('Getting {file} using local data'.format(file=file_name))
				f = 'data/' + file_name
			elif local == False:
#				print('Getting daily reports using github (remote) data')
				f = daily_report_url + file_name
			try:
				df = pd.read_csv(f, header=0)
				df['Date'] = date_str
				if date > pd.to_datetime('03/21/2020'): # Handle the new format.
					df['Last Update'] = df['Last_Update']
					print("loaded {f}".format(f=f))
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
