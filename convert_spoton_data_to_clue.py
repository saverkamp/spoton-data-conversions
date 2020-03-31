#!/usr/bin/env python
# coding: utf-8

import sys
import csv
import json
import datetime

def convertSODate(datenum):
    """Convert Spot On's date format to ISO 8601"""
    #Date numbers seem to start with 0 = 2001-01-01
    base_date = datetime.date(2001, 1, 1)
    #add key from the spot on object to this base date to get the date
    record_date = base_date + datetime.timedelta(days=int(datenum))
    record_date = record_date.isoformat()
    return record_date

def spotOnToClue(day, mapping):
    """Convert a day of Spot On data to Clue format"""
    mapkeys = [m['SpotOn_field'] for m in mapping]
    clueday = {}
    cdate = convertSODate(day[0])
    clueday['day'] = cdate
    for k, v in day[1].items():
        if k == 'CustomState' and len(v) > 0:
            for cs in v:
                field = 'E-' + cs['label']
                value = True
                #map custom field if it's in the mapping
                if field in mapkeys:
                    cluestate = mapState((field,value), mapping)
                    if len(cluestate) > 0:
                        clueday = updateClueday(cluestate, clueday)
        if k == 'DayState':
            for field, value in v.items():
                if field in mapkeys:
                    cluestate = mapState((field,value), mapping)
                    if len(cluestate) > 0:
                        clueday = updateClueday(cluestate, clueday) 
    return clueday
                        
def mapState(state, mapping):
    cluestate = {}
    k = state[0]
    v = state[1]
    for m in mapping:
        if k == m['SpotOn_field'] and v != False:
            try:
                if m['Clue_datatype'] == 'array':
                    cluestate[m['Clue_field']] = [m['Clue_value']]
                elif m['Clue_datatype'] == 'text':
                    cluestate[m['Clue_field']] = m['Clue_value']
                elif m['Clue_datatype'] == 'boolean':
                    cluestate[m['Clue_field']] = True
            except:
                print('Something is wrong with your mapping in field:' + m['SpotOn_field'] + '.  ' +
                      'Fix your mapping, re-export the CSV, and try again.') 
    return cluestate
    
def updateClueday(cluestate, clueday):
    cskeys = [k for k,v in cluestate.items()]
    for c in cskeys:
        if c in clueday.keys():
            if type(v) == list:
                clueday[c].extend(cluestate[c])
                #dedupe list if necessary
                clueday[c] = list(set(clueday[c]))
            else:
                clueday[c] = cluestate[c]
        else:
            clueday.update(cluestate)
    return clueday

def clueDedupe(clue_mapped, clue_export, preference):
    """Merge with existing Clue export data according to user preference"""
    cm_dates = [c['day'] for c in clue_mapped]
    for ce in clue_export['data']:
        if ce['day'] in cm_dates:
            for idx, cm in enumerate(clue_mapped):
                #find matching dates
                if ce['day'] == cm['day']:
                    #combine both date's data points if 'combine' is chosen, but preference clue export
                    #on conflict
                    if preference.lower() == 'combined':
                        for k, v in clue_mapped[idx].items(): 
                            if k in ce:
                                clue_mapped[idx][k].extend(ce[k])
                                clue_mapped[idx][k] = list(set(clue_mapped[idx][k]))
                            else:
                                clue_mapped[idx][k] = ce[k]
        else:
            clue_mapped.append(ce)
    return clue_mapped

def writeToCsv(clue):
    """Write import data to CSV if needed for editing data"""
    filename = 'new_clue_import_for_editing.csv'
    f = open(filename, 'w')
    fieldnames = list(set([m['Clue_field'] for m in mapping]))
    fieldnames.append('date')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for c in clue:
        writer.writerow(c)
    f.close()

def getAllTags(clue):
    tags = []
    for c in clue:
        for k, v in c.items():
            if k == 'tags':
                for t in v:
                    tags.append(t)
        tags = list(set(tags))    
    return tags

if __name__ == "__main__":
    
    #all necessary files are hardcoded into this scripts, but command line takes two optional
    #arguments -- .cluedata export file and preference ('Clue', 'Combined', 'SpotOn')
    clue_export_file = None

    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ['clue', 'combined', 'spoton']:
            preference = sys.argv[1].lower()
        elif sys.argv[1].endswith('cluedata'):
            clue_export_file = sys.argv[1]
    if len(sys.argv) > 2:
        if sys.argv[2].lower() in ['clue', 'combined', 'spoton']:
            preference = sys.argv[2].lower()  
        elif sys.argv[2].endswith('cluedata'):
            clue_export_file = sys.argv[2]

    #take in custom mapping, spot-on data, and clue data from command line
    mapfile = open('my_spoton-to-clue_mapping.csv', 'r')
    my_map = csv.DictReader(mapfile)
    my_map = [m for m in my_map]
    
    my_data = json.load(open('spoton_data/upgrade_data.json'))
    
    #create list for all days
    clue = []
    
    #iterate through each day of data, map, and add to the list of days
    for k, v in my_data['days'].items():
        clue_day = spotOnToClue((k,v), my_map)
        clue.append(clue_day)
        
    #append existing clue data if provided, giving preference for duplicate days to app specified 
    #in CLI, ignore on exception and default to SpotOn mapping (this can be overriden on ingest)
    try:
        clue_export = json.load(open(clue_export_file))
        #specify which data to preference for overlapping days--Clue, SpotOn, or both (combined)
        clue = clueDedupe(clue, clue_export, preference)
    except:
        print('Data was not merged with an existing Clue export. If you were trying to merge your SpotOn ' +
             'data with your existing Clue data, make sure you specify the filename of your Clue export file ' +
             'and one of the following options on the command line: "clue", "combined", "spoton"\n' +
              'example: python3 ClueBackup-2020-03-25.cluedata combined')
        pass
    
    #sort list by date (not sure if this matters, but why not)
    clue_sorted = sorted(clue, key=lambda k: k['day']) 
    
    #add default settings
    all_tags = getAllTags(clue_sorted)
    clue_import = {}
    clue_import['data'] = clue_sorted
    clue_import['version'] = 5
    clue_import['settings'] = {}
    clue_import['settings'].update({'user_defaults':[]})
    defaults = {}
    defaults['app_state'] = {'user_created_tags': all_tags}
    clue_import['settings']['user_defaults'].append(defaults)
    
    #output to json
    json.dump(clue_import, open('new_clue_import.cluedata', 'w'))
    print('Clue import file created at "new_clue_import.cluedata"')

