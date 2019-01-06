import requests
import xmltodict
import datetime
import pandas as pd
import numpy as np
import progressbar
import argparse

url = 'http://radiko.jp/v3/program/today/JP13.xml'

res = requests.get(url)
d = xmltodict.parse(res.content.decode('utf8'))
key_word = '乃木坂'

mapping = {'No Live': 
                {
                'duration': 0, 
                'start_time': '--', 
                'end_time': '--', 
                'info': '--',
                'pfm': '--',
                'url': '--',
                'keywords': []
                }
           }

stations = d['radiko']['stations']['station'] 
df = pd.DataFrame()
tol_dur = 60 * 24
cur_time = '05:00-05:30'
time_stamp = []
for i in range(tol_dur):
    if i % 30 == 29:
        if (i + 1) // 30 % 2 == 1:
            cur_time = cur_time[-5:] + '-' + str(int(cur_time[-5:-3]) + 1).zfill(2) + ':00'
        else:
            cur_time = cur_time[-5:] + '-' + str(int(cur_time[-5:-3])).zfill(2) + ':30'
    time_stamp.append(cur_time)
df['Time'] = time_stamp
#bar = progressbar.ProgressBar()
for s in stations:
    ls = list()
    station_name = s['name']
    i = 0
    for p in s['progs']['prog']:
        i += 1
        if len(ls) == 0 and p['@ftl'] > '0500': # if the start time is not 0500
            diff = (int(p['@ftl'][1]) - 5) * 60 + (int(p['@ftl'][2] + p['@ftl'][3]))
            for _ in range(diff): ls.append('No Live')
        dur = int(int(p['@dur']) / 60)
        cur_el = {
            'duration': dur,
            'start_time': p['@ftl'], 
            'end_time': p['@tol'], 
            'info': p['info'],
            'pfm': p['pfm'],
            'url': p['url'],
            'keywords': []
            }
        if not cur_el['info']: cur_el['info'] = ''
        if not cur_el['pfm']: cur_el['pfm'] = ''
        if not cur_el['url']: cur_el['url'] = ''
        title = p['title']
        if title not in mapping:
            mapping[title] = cur_el
        for _ in range(dur): ls.append(title)
        if i == len(s['progs']['prog']) and p['@tol'] < '2900': # if the end time is not 2900
            diff = (29 - int(p['@tol'][0] + p['@tol'][1])) * 60 - (int(p['@tol'][2] + p['@tol'][3]))
            for _ in range(diff): ls.append('No Live')
    df[station_name] = ls

writer = pd.ExcelWriter('list.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='1', index=False, encoding='utf-8-sig')
workbook = writer.book
worksheet = writer.sheets['1']
merge_format = workbook.add_format({
    'align': 'center', 
    'valign': 'vcenter', 
    'bold': 1, 
    'border': 1,
    'fg_color': '#CACACA',
    'text_wrap': True
    })

# Time Cells Merge
cur_time = '05:00-05:30'
frm = 2
for i in range(tol_dur):
    if i % 30 == 29:
        to = frm + 30 - 1
        worksheet.merge_range('A'+str(frm)+':A'+str(to), cur_time, merge_format)
        if (i + 1) // 30 % 2 == 1:
            cur_time = cur_time[-5:] + '-' + str(int(cur_time[-5:-3]) + 1).zfill(2) + ':00'
        else:
            cur_time = cur_time[-5:] + '-' + str(int(cur_time[-5:-3])).zfill(2) + ':30'
        frm = to + 1

# Programs Cells Merge
merge_format = workbook.add_format({ # not highlight
    'align': 'center', 
    'valign': 'vcenter', 
    'bold': 1, 
    'border': 1,
    'text_wrap': True
    })

k = 65
for col in df:
    if col != 'Time':
        cur_prog = df[col][0]
        frm = 2
        for i in range(tol_dur):
            if df[col][i] != cur_prog:
                to = i - 1 + 2
                worksheet.merge_range(chr(k)+str(frm)+':'+chr(k)+str(to), cur_prog, merge_format)
                if  key_word in mapping[cur_prog]['keywords'] or\
                    key_word in mapping[cur_prog]['info'] or\
                    key_word in mapping[cur_prog]['pfm']: # Machine Learning Process
                    #a051a2
                    if key_word not in mapping[cur_prog]['keywords']:
                        mapping[cur_prog]['keywords'].append(key_word)
                frm = to + 1
                cur_prog = df[col][i]

    k += 1
writer.save()