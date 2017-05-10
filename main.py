import sys
from difflib import SequenceMatcher as sm
import csv

constituencies = {}

used = {}

encoding = 'iso-8859-1'

def load_consituencies():
    with open('CONSTITUENCY.csv', 'r', encoding='iso-8859-1') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            constituencies[row['Constituency Name']] = row


def add_constituency_id(target_csv, target_col, output_file) :
    with open(target_csv, 'r', encoding=encoding) as csv_input:
        reader = csv.DictReader(csv_input)
        with open(output_file, 'w') as csv_output:
            writer = csv.DictWriter(csv_output, reader.fieldnames + ['constituency_id', 'pano_id'])
            writer.writeheader()
            for row in reader:
                target_val = row[target_col]
                constituency_entry = get_closest(target_val)
                constituency_id = constituency_entry['Constituency ID']
                pano_id = constituency_entry['PANO']
                if constituency_id in used:
                    raise Exception("%s : %s already resolved to %s" % (constituency_id , target_val, used[constituency_id]))
                row['constituency_id'] = constituency_id
                row['pano_id'] = pano_id
                used[constituency_id] = target_val
                writer.writerow(row)


def get_closest(target):
    if target in constituencies:
        return constituencies[target]
    else :
        max_score = 0
        for candidate, _ in constituencies.items():
            score = sm(None, target, candidate).ratio()
            if score > max_score:
                max_score = score
                closest = candidate
        return constituencies[closest]

if __name__ == "__main__":
    if len(sys.argv) < 4:
        exit(1)
    target_csv = sys.argv[1]
    target_col = sys.argv[2]
    output_file = sys.argv[3]
    if len(sys.argv) == 5:
        encoding = sys.argv[4]

    load_consituencies()

    add_constituency_id(target_csv, target_col, output_file)