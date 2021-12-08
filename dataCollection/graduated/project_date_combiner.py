import csv
import pandas as pd

list_file = pd.read_csv('lists_2019_8.csv', usecols=['listname', 'start_date', 'end_date'])
project_file = pd.read_csv('graduated_project_updated_urls.csv', usecols=['GIT_URLS', 'Status'])

for a in project_file.itertuples():
    if a[2] == 'Graduated':
        project_name = a[1].replace('https://github.com/apache/','')
        for b in list_file.itertuples():
            if project_name == b[1].lower():
                print(project_name, b[2], b[3])