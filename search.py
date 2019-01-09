import pandas as pd
from pathlib import Path
from datetime import datetime
import pytz

def search(df, key_word, mapping, if_output, save_to):
    '''
    Search for the given keyword and highlight the cells that
    match the keywords. 

    :param df: Pandas DataFrame of the programs
    :param key_word: a String of the keyword to search for
    :param if_text: a Boolean. If True, print out all programs
    containing the keyword with its duration, start time, end time,
    peronalities, information and url.
    ''' 
    if save_to[-1] != '/': save_to += '/'
    dir = save_to + 'radiko_' + datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%y%m%d')
    if not Path(dir).exists():
            Path(dir).mkdir(parents=True)
    writer = pd.ExcelWriter(Path(dir+'/list'+key_word+'.xlsx'), engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Full Schedule', index=False, encoding='utf-8-sig')
    workbook = writer.book
    worksheet = writer.sheets['Full Schedule']
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
    tol_dur = 60 * 24
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
    merge_format_highlight = workbook.add_format({
        'align': 'center', 
        'valign': 'vcenter', 
        'bold': 1, 
        'border': 1,
        'text_wrap': True,
        'fg_color': '#a051a2'
        })
    k = 65
    matches = []
    for col in df:
        if col != 'Time':
            worksheet.set_column(k-65, k-65, 15)
            cur_prog = df[col][0]
            frm = 2
            for i in range(tol_dur):
                if df[col][i] != cur_prog or i == tol_dur - 1:
                    to = i - 1 + 2
                    if i == tol_dur - 1:
                        to += 1
                    if  len(key_word) != 0 and\
                        (key_word in mapping[cur_prog]['keywords'] or\
                        key_word in mapping[cur_prog]['info'] or\
                        key_word in mapping[cur_prog]['pfm'] or\
                        key_word in cur_prog):
                        worksheet.merge_range(chr(k)+str(frm)+':'+chr(k)+str(to), cur_prog, merge_format_highlight)
                        matches.append(cur_prog)
                        if key_word not in mapping[cur_prog]['keywords']: # Machine Learning Process
                            mapping[cur_prog]['keywords'].append(key_word)
                    else:
                        worksheet.merge_range(chr(k)+str(frm)+':'+chr(k)+str(to), cur_prog, merge_format)
                    frm = to + 1
                    cur_prog = df[col][i]
        k += 1

    # Search Results Output
    if if_output and len(key_word) != 0:
        output_df = pd.DataFrame(index=['Station',
                                        'Duration', 
                                        'Start Time', 
                                        'End Time', 
                                        'Detailed Information', 
                                        'Personality', 
                                        'Website'])
        for match in matches:
            output_df[match] = [mapping[match]['station'],
                                str(mapping[match]['duration']) + ' min',
                                mapping[match]['start_time'][0:2] + ':' + mapping[match]['start_time'][2:4],
                                mapping[match]['end_time'][0:2] + ':' + mapping[match]['end_time'][2:4],
                                mapping[match]['info'],
                                mapping[match]['pfm'],
                                mapping[match]['url']]
        # Fit column and row width
        text_wrap = workbook.add_format({'text_wrap': True, 
                            'align': 'left',
                            'valign': 'vcenter'})
        output_df.to_excel(writer, sheet_name='Search Results', encoding='utf-8-sig')
        output_worksheet = writer.sheets['Search Results']
        output_worksheet.set_row(0, 20, text_wrap)
        for row in range(len(output_df)):
            if list(output_df.index)[row] == 'Detailed Information':
                output_worksheet.set_row(row+1, 200, text_wrap)
            else:
                output_worksheet.set_row(row+1, 20, text_wrap)
        for col in range(len(output_df.columns)+1):
            if col == 0:
                output_worksheet.set_column(col, col, 15, text_wrap)
            else:
                output_worksheet.set_column(col, col, 80, text_wrap)
        
    writer.save()
    workbook.close()