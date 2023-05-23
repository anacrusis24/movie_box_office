'''
---------- bo_mojo_scraper.py ----------
Time    :  2023/05/22 16:44:49
Version :  1.0
Author  :  Austin Villegas 
Github  :  https://github.com/anacrusis24
Contact :  ajv131@gmail.com
Desc    :  Scraper for boxofficemojo.com
'''

# imports
import pandas as pd
from datetime import date
from tqdm.auto import tqdm
import csv
import requests
from requests.adapters import HTTPAdapter, Retry
from bs4 import BeautifulSoup

# set the number of retries
retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[500, 502, 503, 504])

# see if the csv has data
try:
    df = pd.read_csv('bo_data\\bo_data_daily.csv', sep=',', header=0)
    if len(df.index > 0):
        dates_in_file = df.date.unique()
        print('here')
    else:
        dates_in_file = None

# if the csv has no data 
except:
    # add column names
    with open('bo_data\\bo_data_daily.csv', 'a', newline='') as csv_file:
        cols = ['date', 'title', 'daily_gross', 'num_theaters', 'avg_gross', 'gross_to_date', 'day_of_release', 'distributor']
        writer = csv.writer(csv_file)
        writer.writerow(cols)

    dates_in_file = None

# base URL is https://www.boxofficemojo.com/date/2023-05-21/
# just have to iterate through date
today = date.today()
today = today.strftime('%m/%d/%Y')
date_list = pd.date_range(start='01/01/2000', end=today)
date_list = [str(date)[0:10] for date in date_list]
if dates_in_file is not None:
    s = set(dates_in_file)
    date_list = [date for date in date_list if date not in s]    

# continuously write data to csv
# open the csv file which will always exist
with open('bo_data\\bo_data_daily.csv', 'a', newline='') as csv_file:
    # get bo data for each date
    for date in tqdm(date_list, 'DATE'): 
        # make URL for that date
        URL = f'https://www.boxofficemojo.com/date/{date}/'

        # get the html code
        page = requests.Session()
        page.mount('http://', HTTPAdapter(max_retries=retries))
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        # get data from table
        results = soup.find(id='table')

        if results is not None:
            table_rows = results.find_all('tr')
            table_rows = table_rows[1:] # exclude column titles

            # loop through rows of the table
            for row in table_rows:
                # get values from row
                col_vals = [val.get_text(strip=True) for val in row.find_all('td') if val.get_text(strip=True)!=""]
                index_list = [2, 3, 6, 7, 8, 9, 10]
                col_vals = [date] + [col_vals[i] for i in index_list]
                writer = csv.writer(csv_file)
                writer.writerow(col_vals)