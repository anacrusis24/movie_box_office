'''
---------- mojo_scraper_v0.py ----------
Time    :  2023/05/21 19:27:25
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
import requests
from requests.adapters import Retry
from bs4 import BeautifulSoup

# set the number of retries
retries = Retry(total=5,
                backoff_factor=120,
                status_forcelist=[500, 502, 503, 504])

# make df to hold all the data
bo_data = pd.DataFrame()
date_col = []
title_col = []
daily_gross_col = []
num_theaters_col = []
avg_gross_per_day_col = []
to_date_gross_col = []
days_release_col = []
distributor_col = []

# make the list of sites to scrape
# base URL is https://www.boxofficemojo.com/date/2023-05-21/?ref_=bo_di_table_1
# just have to iterate through date

# get dates
date_list = pd.date_range(start ='01/01/2000', end ='05/21/2023')
date_list = [str(date)[0:10] for date in date_list ]

# get bo data for each date
for date in tqdm(date_list, 'DATE'): 
    # make URL for that date
    URL = f'https://www.boxofficemojo.com/date/{date}/?ref_=bo_di_table_1'

    # get the html code
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # get data from table
    results = soup.find(id="table")
    
    # loop through rows of the table
    table_rows = results.find_all("tr", class_='mojo-annotation-isEstimated')

    for row in table_rows:
        # get values from row
        col_vals = [row.get_text(strip=True) for row in table_rows[0].find_all("td") if row.get_text(strip=True)!=""]

        # add data to lists
        date_col.append(date)
        title_col.append(col_vals[2])
        daily_gross_col.append(col_vals[3])
        num_theaters_col.append(col_vals[6])
        avg_gross_per_day_col.append(col_vals[7])
        to_date_gross_col.append(col_vals[8])
        days_release_col.append(col_vals[9])
        distributor_col.append(col_vals[10])


# add the columns of data to the df
bo_data['date'] = date_col
bo_data['title'] = title_col
bo_data['daily_gross'] = daily_gross_col
bo_data['num_theaters'] = num_theaters_col
bo_data['avg_gross'] = avg_gross_per_day_col
bo_data['gross_to_date'] = to_date_gross_col
bo_data['day_of_release'] = days_release_col
bo_data['distributor'] = distributor_col

# convert the df to a .csv and save
bo_data.to_csv(f'bo_data\\bo_data_{date.today()}.csv')