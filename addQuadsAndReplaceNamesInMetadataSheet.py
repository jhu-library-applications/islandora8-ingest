import pandas as pd
import argparse
import re
import os
from datetime import datetime
import numpy as np
import mappingtaxonomiesandrelators as mt

"""
For lookUpByID fields specified in the mappingtaxonomiesandrelators.py, this script replaces taxonomy names in your 
metadata spreadsheet with their unique identifiers and adds quad formatting. For lookUpByName fields, the script adds 
quad formatting with look-up of 'name'. 

For relators fields, the script combines pre-existing relator prefixes, quads, and unique_id for look-up. 
Note: the script does NOT add relator prefixes, those should already exist in the metadata spreadsheet 
in front of the taxonomy name.
Use "||" to separate more than one value in your metadata spreadsheet.

Each taxonomy spreadsheet needs the following fields: unique_id, name.
Name your taxonomy spreadsheets by their machine names (corporate_body.csv, family.csv, genre.csv
geo_location.csv, language.csv, person.csv, subject.csv) and place into a folder by themselves.
Your taxonomy spreadsheets should include all of taxonomy terms that exist in your metadata spreadsheet, this includes 
new taxonomy terms you are adding HDL and taxonomy terms that already exist in HDL.

If the script cannot find a taxonomy term in a taxonomy spreadsheet, that value will not be changed in the 
new metadata spreadsheet.
"""

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file')
parser.add_argument('-d', '--directory')
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter metadata filename (including \'.csv\'): ')
if args.directory:
    directory = args.directory
else:
    directory = input('Enter directory with taxonomies: ')


def make_dataframe(full_filename, file):
    frame = pd.read_csv(full_filename)
    for csv_name, lookup in mt.quads.items():
        if csv_name == file:
            frame['quad'] = lookup
    frames.append(frame)


# Split any string columns to list.
df_1 = pd.read_csv(filename, header=0)
all_items = []
for count, row in df_1.iterrows():
    row = row
    for key, value in mt.columnDict.items():
        for column in value:
            columnValue = row.get(column)
            if pd.notnull(columnValue):
                row[column] = str(columnValue).split('||')
    all_items.append(row)
df_1 = pd.DataFrame.from_dict(all_items)
df_1 = df_1.where(pd.notnull(df_1), None)
print(df_1.head)

# Create DataFrames from taxonomy spreadsheets.
frames = []
chart = {}
for count, file in enumerate(os.listdir(directory)):
    print(count, file)
    full_filename = directory+"/"+file
    if full_filename.endswith('.csv'):
        make_dataframe(full_filename, file)
        chart[file] = count

# Get identifiers and labels from taxonomy DataFrames.
taxonomies = []
for df in frames:
    for count, row in df.iterrows():
        unique_id = row.get('unique_id')
        name = row.get('name')
        quad_lookup = row.get('quad')
        new_dict = {'unique_id': unique_id, 'name': name, 'quad': quad_lookup}
        taxonomies.append(new_dict)
taxonomies = pd.DataFrame.from_dict(taxonomies)
print(taxonomies.head)


def find_term_add_quad(relator, key, stripped_value):
    for tax_index, tax_row in taxonomies.iterrows():
        tax_term = tax_row.get('name')
        if stripped_value == tax_term:
            tax_id = tax_row.get('unique_id')
            quad = tax_row.get('quad')
            if key == 'lookUpByName':
                quad = quad.replace('::', ':name:')
                new_list_value = quad+tax_id
            elif key == 'lookUpByID':
                new_list_value = quad+tax_id
            elif key == 'relators':
                new_list_value = relator+quad+tax_id
            return new_list_value


# Find and replace using new_dict with labels and ids.
all_items = []
# Loop through metadata fields.
for index, row in df_1.iterrows():
    print(index)
    row = row
    # Checks fields with taxonomy terms.
    for key, value in mt.columnDict.items():
        for column in value:
            dataValue = row.get(column)
            # If there is a dataValue (formatted as list), loop through it.
            if dataValue is not None:
                original_count = len(dataValue)
                dataValue = dataValue
                for i, listValue in enumerate(dataValue):
                    if pd.notnull(listValue):
                        # If dataValue doesn't already have quad lookup, continue.
                        if re.search(r"(?:[^:]*:){3}[^:]*", listValue) is None:
                            listValue = listValue.strip()
                            # Remove relator to search for match in taxonomy DataFrame.
                            if key == 'relators':
                                for relator in mt.relators:
                                    if relator in listValue:
                                        listValue = listValue.replace(relator, "")
                                        relator = relator
                            else:
                                listValue = listValue
                                relator = None
                            # Build full string with quad and relator (if needed).
                            # If field in lookUpById, replace taxonomy name with unique_id.
                            # Else, format quad as :taxonomy:name:.
                            newListValue = find_term_add_quad(relator, key, listValue)
                            if newListValue:
                                dataValue[i] = newListValue
                            else:
                                pass

                row[column] = dataValue
                new_count = len(dataValue)
                if original_count != new_count:
                    print('Oops!! There is an error.')
                row[column] = '||'.join(dataValue)
            else:
                pass
    all_items.append(row)
new = pd.DataFrame.from_dict(all_items)
print(new.head)


# Create CSV for new DataFrame.
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
new.to_csv('flip_'+dt+'.csv')