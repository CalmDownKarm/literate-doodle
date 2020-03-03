def schedule_me():
    import pandas as pd

    # clean new updates
    ideal_promises = pd.read_excel('./assets/data/Promises.xlsx')
    # ideal_promises.to_excel('newPromises.xlsx', index=None)
    ideal_promises.Promise = ideal_promises.Promise.apply(lambda x: x.lower().strip())
    ideal_promises['Sub promise'] = ideal_promises['Sub promise'].apply(lambda x: x.lower().strip())
    import requests
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQi5APAZW3CvMw-8LUdCFxdg5CIEjAB-EnnKHe6kzMxQyHDWZbZToW3kLSvpDMcEQZ34o6nOIxbMcwm/pub?output=xlsx"
    googleFormUpdates = requests.get(url)
    open('./assets/data/googleFormUpdates.xlsx', 'wb').write(googleFormUpdates.content)
    updates = pd.read_excel('./assets/data/googleFormUpdates.xlsx')
    updates = updates.rename(columns={'Promise ': 'Promise', 'SubPromise ': 'SubPromise'})
    updates['Promise'].fillna('None', inplace=True)
    updates['Promise'] = updates['Promise'].apply(lambda x: x.lower().strip())
    correct_subpromises = ideal_promises['Sub promise'].unique()
    correct_promises = set([promise.lower() for promise in ideal_promises.Promise.unique()])
    assert len(correct_promises) == 70
    updates_promises = set([promise.lower() for promise in updates['Promise'].unique()])
    errors = updates_promises - correct_promises
    from fuzzywuzzy import process
    corrections = {k:process.extract(k, correct_promises, limit=1)[0][0] for k in errors}
    maps = {k:k for k in updates['Promise'].unique()}
    maps.update(corrections)
    updates['Promise'] = updates['Promise'].map(maps)
    updates['SubPromise'].fillna('None', inplace=True)
    updates['SubPromise'] = updates['SubPromise'].apply(lambda x: x.split('__')[-1].lower().strip())
    subpromise_errors = set(updates['SubPromise'].unique()) - set(correct_subpromises)
    corrections = {k:process.extract(k, correct_subpromises, limit=2) for k in subpromise_errors}
    subpromise_error_indices = updates[updates['SubPromise'].isin(subpromise_errors)].index
    updates = updates.drop(subpromise_error_indices)
    updates.to_excel('./assets/data/googleFormUpdates.xlsx')

    # Merge old and new updates
    oldupdates = pd.read_excel('./assets/data/old/updates.xlsx')
    oldupdates['Promise'] = oldupdates['Promise'].apply(lambda x: x.lower().strip())
    old_and_new_updates = pd.concat([updates, oldupdates], sort=False)
    merged_df = pd.merge(old_and_new_updates, ideal_promises, left_on='SubPromise', right_on = 'Sub promise')
    merged_df.drop(merged_df.columns[merged_df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    merged_df.drop(['Promise_x', '__', 'Sr No'],axis=1, inplace=True)
    merged_df = merged_df.rename(columns={'Promise_y': 'Promise'})
    merged_df.to_excel('./assets/data/updates.xlsx')