import re
import requests
import pandas as pd
from fuzzywuzzy import process


def schedule_me():
    ideal_promises = pd.read_excel('assets/data/Promises.xlsx')
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQi5APAZW3CvMw-8LUdCFxdg5CIEjAB-EnnKHe6kzMxQyHDWZbZToW3kLSvpDMcEQZ34o6nOIxbMcwm/pub?output=xlsx"
    googleFormUpdates = requests.get(url)
    with open('assets/data/googleFormUpdates.xlsx', 'wb') as f:
        f.write(googleFormUpdates.content)
    updates = pd.read_excel('assets/data/googleFormUpdates.xlsx').rename(
        columns={'Promise ': 'Promise', 'SubPromise ': 'Sub promise'}).dropna(how='all')
    for col in ['Promise', 'Sub promise']:
        ideal_promises[col] = ideal_promises[col].apply(lambda x: x.lower().strip())
        updates[col] = updates[col].apply(lambda x: x.lower().strip())
    correct_subpromises = set(ideal_promises['Sub promise'].unique())
    correct_promises = set(ideal_promises['Promise'].unique())
    updates_promises = set(updates['Promise'].unique())
    errors = updates_promises - correct_promises
    corrections = {k: process.extract(k, correct_promises, limit=1)[0][0] for k in errors}
    maps = {k: k for k in updates['Promise'].unique()}
    maps.update(corrections)
    updates['Promise'] = updates['Promise'].map(maps)
    updates['Sub promise'] = updates['Sub promise'].apply(
        lambda x: x.split('__')[-1].lower().strip())
    updates[updates['Sub promise'].isin(correct_subpromises)].to_excel(
        'assets/data/googleFormUpdates.xlsx', index=None)
    oldupdates = pd.read_excel('assets/data/old_website_updates.xlsx')
    combined = pd.concat([updates, oldupdates], sort=False)
    merged_df = pd.merge(combined, ideal_promises, left_on='Sub promise', right_on='Sub promise')
    merged_df = merged_df.drop(['Department_x', 'Promise_x', 'Outcome_x', 'Sr No'], axis=1).rename(
        columns={'Promise_y': 'Promise', 'Department_y': 'Department', 'Outcome_y': 'Outcome'})
    merged_df['Department'] = merged_df['Department'].apply(
        lambda x: re.sub('\sDepartment', '', x))
    status_maps = {
        'Done': 'Fulfilled',
        'In Progress': 'Partially Fulfilled',
        'Started': 'Partially Fulfilled',
        'Not Started': 'Unfulfilled'
    }
    merged_df['Status'] = merged_df['Status'].map(status_maps)
    merged_df.to_excel('assets/data/updates.xlsx', index=None)
