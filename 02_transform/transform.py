import csv
import json

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputfile', help="the path to the input csv-file", required=True)
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()

print("Reading organizations from: %s"%args.inputfile)


def transformToPublisher(data):
    # Transforming according to rules in README
    transformed = {}
    transformed['id'] = data['organisasjonsnummer']
    transformed['uri'] = "http://data.brreg.no/enhetsregisteret/enhet/" + data['organisasjonsnummer']
    transformed['name'] = data['navn']
    transformed['organisasjonsform'] = data['organisasjonsform']['kode']
    transformed['orgPath'] = "/PRIVAT/" + data['organisasjonsnummer']
    # Valid attribute needs to be "calculated"
    if (data['konkurs']):
        transformed['valid'] = "false"
    else:
        transformed['valid'] = "true"
    prefLabel = {}
    prefLabel['no'] = data['navn']
    transformed['prefLabel'] = prefLabel
    # Næringskode object
    naeringskode = {}
    naeringskode['uri'] = "http://www.ssb.no/nace/sn2007/" + data['naeringskode1']['kode']
    naeringskode['code'] = data['naeringskode1']['kode']
    prefLabel = {}
    prefLabel['no'] = data['naeringskode1']['beskrivelse']
    naeringskode['prefLabel'] = prefLabel
    transformed['naeringskode'] = naeringskode
    # Sektokode object
    sektorkode = {}
    sektorkode['uri'] = "http://www.brreg.no/sektorkode/" + data['institusjonellSektorkode']['kode']
    sektorkode['code'] = data['institusjonellSektorkode']['kode']
    prefLabel = {}
    prefLabel['no'] = data['institusjonellSektorkode']['beskrivelse']
    sektorkode['prefLabel'] = prefLabel
    transformed['sektorkode'] = sektorkode
    # TODO Do the actual transformation
    return transformed

with open(args.inputfile, encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=",")
  # extracting field names through first row
    next(reader, None)
    for row in reader:
        orgNummer = row[0]
        inputfileName = args.outputdirectory + orgNummer + "_enhetsregisteret.json"
        outputfileName = args.outputdirectory + orgNummer + "_Publisher.json"
        with open(inputfileName) as json_file:
            data = json.load(json_file)
            # Transform the organization object to publihser format:
            with open(outputfileName, 'w', encoding="utf-8") as outfile:
                json.dump(transformToPublisher(data), outfile, ensure_ascii=False, indent=4)
