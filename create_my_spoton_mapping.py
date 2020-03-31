#!/usr/bin/env python
# coding: utf-8

import sys
import json
from datetime import datetime
import csv
import zipfile

def convertDate(datenum):
    #Dates seem to start with 0 = 2001-01-01
    base_date = datetime.date(2001, 1, 1)
    #add key from the spot on object to this base date to get the date
    record_date = base_date + datetime.timedelta(days=datenum)
    record_date = record_date.isoformat()
    return record_date

def parseEmoji(data):
    emoji = []
    for k, v in data['days'].items():
        if len(v['CustomState']) > 0:
            for c in v['CustomState']:
                emoj = {}
                emoj['id'] = c['id']
                emoj['label'] = c['label']
                emoj['emoji'] = c['emoji']
                emoji.append(emoj)
    #dedupe emoji
    emoji = list({e['id']:e for e in emoji}.values())
    return emoji

def addEmojiToMap(data, my_map, app):
    custom_emoji = parseEmoji(data)
    for c in custom_emoji:
        if app.lower() == 'drip':
            new_field = {}
            new_field['SpotOn_field'] = 'E-' + c['label']
            new_field['Drip_field'] = ''
            new_field['Drip_value'] = ''
        if app.lower() == 'clue':
            new_field = {}
            new_field['SpotOn_field'] = 'E-' + c['label']
            new_field['Clue_field'] = ''
            new_field['Clue_datatype'] = ''
            new_field['Clue_value'] = ''
        my_map.append(new_field)
    return my_map

def writeToCsv(my_map, app):
    filename = 'my_spoton-to-{}_mapping.csv'.format(app.lower())
    f = open(filename, 'w')
    fieldnames = [m for m in my_map[0].keys()]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for mm in my_map:
        writer.writerow(mm)
    f.close()

if __name__ == "__main__":

    #unpack Spot On Info.spa archive file
    with zipfile.ZipFile('Spot On Info.spa', 'r') as zip_ref:
        zip_ref.extractall('spoton_data')

    data = json.load(open('spoton_data/upgrade_data.json', 'r'))
        
    app = 'clue'
    try:
        app = sys.argv[1]
        if app.lower() == 'drip':
            my_map = csv.DictReader(open('default_drip_mapping.csv', 'r'))
            my_map = [m for m in my_map]
        elif app.lower() == 'clue':
            my_map = csv.DictReader(open('default_clue_mapping.csv', 'r'))
            my_map = [m for m in my_map]
        #parse upgrade_data.json file to find all custom emoji used
        my_map = addEmojiToMap(data, my_map, app)
        #output new mapping (my_spoton-to-drip_mapping.csv) for user to adjust as needed
        writeToCsv(my_map, app)
        print('Custom emoji successfully added to your ' + app + ' mapping. Next, edit your "my_spoton-to-{}_mapping.csv" file in a spreadsheet editor.'.format(app.lower()))
    except:
        print('Please include "Drip" or "Clue" in. your command, ex. "create_my_spoton_mapping.py Drip"')
        

    

