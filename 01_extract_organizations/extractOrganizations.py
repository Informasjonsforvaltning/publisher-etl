import csv
import requests
import json

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputfile', help="the path to the input csv-file", required=True)
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()

print("Reading organizations from: %s"%args.inputfile)
headers={"Accept":"application/json"}

with open(args.inputfile, encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=",")
  # extracting field names through first row
    next(reader, None)
    for row in reader:
        orgNummer = row[0]
        orgName = row[1]
        url = "https://data.brreg.no/enhetsregisteret/api/enheter/" + orgNummer
        r = requests.get(url=url, headers=headers)
        print (orgNummer + "/" + orgName + ": Status code " + str(r.status_code))
        with open(args.outputdirectory + orgNummer + '_enhetsregisteret.json', 'w', encoding="utf-8") as outfile:
            json.dump(r.json(), outfile, ensure_ascii=False, indent=4)

    # get total number of rows
    print("Total no. of organizations from enhetsregisteret: %d"%(reader.line_num - 1))
