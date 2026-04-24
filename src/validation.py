import csv
import sys

csv.field_size_limit(sys.maxsize)

path = 'data/NVDA_financial_data.csv'
fields = [] # Column names
rows = [] # Data rows

with open(path, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    
    fields = next(csvreader)
    for rows in csvreader:
        rows.append(rows)

        print("Total number of rows: %d" % csvreader.line_num)
    print('Field names are: ' + ', '.join(fields))

# OverflowError: Python int too large to convert to C long
# Fix with while loop
try:
    max_int = sys.maxsize
    while True:
        try:
            # Attempt to set the maximum field size limit
            csv.field_size_limit(max_int)
            break  # Break the loop if successful
        except OverflowError:
            # Reduce max_int and retry
            max_int = int(max_int / 10)
except Exception as e:
    print(f"Unexpected error while setting field size limit: {e}")
