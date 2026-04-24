import json
import csv
import sys
import smart_open


class SECDataset(object):
    def __init__(self, path):
        self.path = path

    def __iter__(self):
        with smart_open.open(self.path, 'r') as f:
            if sys.version_info[0] == 2:
                reader = csv.DictReader(f, delimiter=",", quotechar='"')
            else:
                reader = csv.DictReader((line.decode('utf-8') for line in f), delimiter=",", quotechar='"')
            for row in reader:
                yield dict(row)