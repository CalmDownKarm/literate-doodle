import pandas as pd
ideal_promises = pd.read_excel('assets/data/Promises.xlsx')
ideal_promises.to_excel('newPromises.xlsx', index=None)
ideal_promises.Promise = ideal_promises.Promise.apply(lambda x: x.lower().strip())
ideal_promises['Sub promise'] = ideal_promises['Sub promise'].apply(lambda x: x.lower().strip())

# point this to where the new reponses will be donwloaded
updates = pd.read_excel('assets/data/newResponses.xlsx')


updates.Promise = updates.Promise.apply(lambda x: x.lower().strip())
correct_promises = set([promise.lower() for promise in ideal_promises.Promise.unique()])
assert len(correct_promises) == 70
updates_promises = set([promise.lower() for promise in updates.Promise.unique()])
errors = updates_promises - correct_promises
from fuzzywuzzy import process
corrections = {k:process.extract(k, correct_promises, limit=1)[0][0] for k in errors}
maps = {k:k for k in updates.Promise.unique()}
maps.update(corrections)
updates['Promise'] = updates['Promise'].map(maps)
updates['SubPromise'] = updates['SubPromise'].apply(lambda x: x.split('__')[-1].lower().strip())
subpromise_errors = set(updates['SubPromise'].unique()) - set(correct_subpromises)
corrections = {k:process.extract(k, correct_subpromises, limit=2) for k in subpromise_errors}
updates[updates['SubPromise'].isin(subpromise_errors)].to_excel('soumya_corrections.xlsx')
subpromise_error_indices = updates[updates['SubPromise'].isin(subpromise_errors)].index
updates = updates.drop(subpromise_error_indices)
updates.to_excel('newupdates.xlsx')

# read current updates
old_updates = pd.read_excel('assets/data/updates.xlsx')

old_updates['SubPromise'] = old_updates['SubPromise'].apply(lambda x: x.split('__')[-1].lower().strip())
# concat updates
old_and_new_updates = pd.concat([updates, old_updates])
merged_df = pd.merge(old_and_new_updates, ideal_promises, left_on='SubPromise', right_on = 'Sub promise')
#write to file
merged_df.to_excel('assets/data/updates.xlsx', index=None)
