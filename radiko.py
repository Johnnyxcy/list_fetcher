import xmltodict
import pandas as pd
import requests

def radiko(url, mapping):
    """
    Constructs a Pandas Data Frame based on the given 
    url of radiko programs list API.

    Args:
        d(string): url of radiko programs list API
        
    Returns: 
        [pd.DataFrame, dict]: Pandas DataFrame and a 
        mapping including detailed information of programs.
    """
    res = requests.get(url)
    print('Status: ', str(res.status_code))
    d = xmltodict.parse(res.content.decode('utf8'))

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
                'station': station_name,
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

    return df, mapping