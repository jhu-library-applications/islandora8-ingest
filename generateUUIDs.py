import uuid
import pandas as pd
import argparse
import os
from datetime import datetime

# Script takes all CSVs files located in desired directory (folder)
# and turns them into DataFrames, adding a column of UUIDs to each.
# Each updated DataFrame is turned into a new CSV and placed in a sub-folder
# named by a timestamp, like "2021-06-31_10-30-29."

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory')
args = parser.parse_args()

if args.directory:
    directory = args.directory
else:
    # Example: /Users/michelle/Desktop/spreadsheets
    directory = input('Enter directory with migration spreadsheets: ')


# Function to create DataFrame and add frames dictionary.
def make_dataframe(frame, full_filename, filename):
    frame = pd.read_csv(full_filename)
    new_filename = filename[:-4]
    frames[new_filename] = frame


# Create DataFrames from spreadsheets.
frames = {}
for count, file in enumerate(os.listdir(directory)):
    full_file = directory + "/" + file
    if full_file.endswith('.csv'):
        make_dataframe("df_{}".format(count), full_file, file)

print('{} spreadsheets found and added to dictionary'.format(len(frames)))
print('')

# Create sub-folder to put spreadsheets updated with UUIDs.
# Example: /Users/michelle/Desktop/spreadsheets/2021-07-02_10-30-29
dt = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
new_path = directory + r'/' + dt
if not os.path.exists(new_path):
    os.makedirs(new_path)
    print("New folder '{}' created in {}".format(dt, directory))

# Add UUIDs to DataFrames.
for filename, frame in frames.items():
    uuids = []
    for count, row in frame.iterrows():
        local_id = uuid.uuid4()
        uuids.append(local_id)
    frame['unique_id'] = uuids
    print("UUIDs added to '{}'".format(filename))

    # Create updated spreadsheet in new sub-folder.
    updt_filename = filename+'_withUniqueIds.csv'
    frame.to_csv(path_or_buf=new_path + '/' + updt_filename,
                 index=False)
    print("Updated file '{}' created in '{}'".format(updt_filename, new_path))
    print('')