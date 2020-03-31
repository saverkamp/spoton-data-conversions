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

def spotOnToDrip(day, mapping, spotting='exclude'):
    """Convert a day of Spot On data to Drip format"""
    mapkeys = [m['SpotOn_field'] for m in mapping]
    dripday = {}
    ddate = convertSODate(day[0])
    dripday['date'] = ddate
    for k, v in day[1].items():
        if k == 'CustomState' and len(v) > 0:
            for cs in v:
                field = 'E-' + cs['label']
                value = True
                if field in mapkeys:
                    dripstate = mapState((field,value), mapping)
                    if len(dripstate) > 0:
                        dripday = updateDripday(dripstate, dripday)
        if k == 'DayState':
            for field, value in v.items():
                if field in mapkeys:
                    dripstate = mapState((field,value), mapping)
                    if len(dripstate) > 0:
                        dripday = updateDripday(dripstate, dripday)      
    #SpotOn doesn't count spotting as part of your period. Default to bleeding.exclude=True
    if 'bleeding.value' in dripday:
        if dripday['bleeding.value'] == 0:
            if spotting == 'include':
                dripday['bleeding.exclude'] = False
            else:
                dripday['bleeding.exclude'] = True       
    return dripday

def mapState(state, mapping):
    dripstate = {}
    k = state[0]
    v = state[1]
    for m in mapping:
        if k == m['SpotOn_field'] and v != False:
            try:
                if m['Drip_value'] == 'boolean':
                    if m['Drip_field'].split('.')[1] == 'exclude':
                        dripstate[m['Drip_field']] = False
                    else:
                        dripstate[m['Drip_field']] =  True
                elif m['Drip_value'][0] in ['0', '1', '2', '3']:
                    dripstate[m['Drip_field']] = int(m['Drip_value'][0])
                elif m['Drip_field'].split('.')[-1] == 'note':
                    dripstate[m['Drip_field']] = m['Drip_value']
                    otherfield = m['Drip_field'].split('.')[0] + '.other'
                    dripstate[otherfield] = True
                elif m['Drip_field'].split('.')[0] == 'note':
                    dripstate[m['Drip_field']] = m['Drip_value']
            except:
                print('Something is wrong with your mapping in field:' + m['SpotOn_field'] + '.  ' +
                      'Fix your mapping, re-export the CSV, and try again.') 
    return dripstate

def updateDripday(dripstate, dripday):
    dskey = [k for k,v in dripstate.items()][0]
    if dskey in dripday.keys():
        if dripday[dskey] != True and dripday[dskey] != '':
            dripday[dskey] = dripday[dskey] + ', ' + dripstate[dskey]
    else:
        dripday.update(dripstate)
    return dripday

def dripDedupe(drip_mapped, drip_export, preference):
    """Merge with existing Drip export data according to user preference"""
    dm_dates = [d['date'] for d in drip_mapped]
    for de in drip_export:
        if de['date'] in dm_dates:
            for idx, dm in enumerate(drip_mapped):
                #find matching dates
                if de['date'] == dm['date']:
                    #combine both date's data points if 'combine' is chosen, but preference drip export
                    #on conflict
                    if preference.lower() == 'combined':
                        for k, v in drip_mapped[idx].items(): 
                            if k in de:
                                if k.startswith('note') or k.endswith('note'):
                                    drip_mapped[idx][k] = drip_mapped[idx][k] + ', ' + de[k]
                                else:
                                    drip_mapped[idx][k] = de[k]
        else:
            drip_mapped.append(de)
    return drip_mapped

def writeToCsv(drip, mapping):
    """Write import data to CSV"""
    filename = 'new_drip_import.csv'
    f = open(filename, 'w')
    fieldnames = list(set([m['Drip_field'] for m in mapping]))
    fieldnames.append('date')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for d in drip:
        writer.writerow(d)
    f.close()

if __name__ == "__main__":
    
    #default to exclude spotting from period and preference drip data
    spotting = 'exclude'
    preference = 'drip'


    #all necessary files are hardcoded into this scripts, but command line takes two optional
    #arguments -- preference ('Drip', 'Combined', 'SpotOn') and spotting ('include' or 'exclude')
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ['drip', 'combined', 'spoton']:
            preference = sys.argv[1].lower()
        elif sys.argv[1].lower() in ['include', 'exclude']:
            spotting = sys.argv[1].lower()
    if len(sys.argv) > 2:
        if sys.argv[2].lower() in ['drip', 'combined', 'spoton']:
            preference = sys.argv[2].lower()        
        elif sys.argv[2].lower() in ['include', 'exclude']:
            spotting = sys.argv[2].lower()

    #take in custom mapping, spot-on data, and drip data from command line
    mapfile = open('my_spoton-to-drip_mapping.csv', 'r')
    my_map = csv.DictReader(mapfile)
    my_map = [m for m in my_map]
    
    my_data = json.load(open('spoton_data/upgrade_data.json'))
        
    #create list for all days
    drip = []
    
    #iterate through each day of data
    for k, v in my_data['days'].items():
        drip_day = spotOnToDrip((k,v), my_map, spotting)
        drip.append(drip_day)
    
    #append existing drip data if provided, giving preference for duplicate days to app specified 
    #in CLI, ignore on exception and default to SpotOn mapping (this can be overriden on ingest)
    try:
        drip_export_file = open('my drip data export.csv', 'r')
        de = csv.DictReader(drip_export_file)
        #specify which data to preference for overlapping days--Drip, SpotOn, or both (combined)
        drip = dripDedupe(drip, de, preference)
    except:
        #if no drip export is detected, change preference to spoton data
        preference = 'spoton'
        print('Data was not merged with an existing Drip export. If you were trying to merge your SpotOn ' +
             'data with your existing Drip data, make sure you included your "my drip data export.csv" file ' +
             'and specified one of the following options on the command line: "drip", "combined", "spoton". ' +
             'If not, then ignore this message!')
        pass
    
    #sort list by date (not sure if this matters, but why not)
    drip_sorted = sorted(drip, key=lambda k: k['date']) 
    
    #write out drip csv
    writeToCsv(drip_sorted, my_map)
    if spotting == 'include':
        print('Spotting included as period bleeding')
    print('Drip import file created as new_drip_import.csv')

