import requests
from bs4 import BeautifulSoup as bs
import time, datetime
from pprint import pprint

#To get HTML Text
def getHTMLText(url):
    kv = {'user-agent':'Mozilla/5.0'}
    try:
        r = requests.get(url, timeout=30, headers = kv)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return ""

# 获取最好成绩
def get_best(wcaid):
    rootURL = 'https://cubingchina.com/results/person/'
    resultHTML = getHTMLText(rootURL + wcaid)
    soup = bs(resultHTML, 'html.parser')
    trList = soup.tbody.find_all('tr')
    trList = list(trList)
    eventsDict={}
    for t in trList:
        try:
            if len(t('a')) == 3:
                eventsDict[t.td.i['title']] = [t('a')[1].string, t('td')[1].string, t('td')[2].string, t('td')[3].string, t('a')[2].string, t('td')[8].string, t('td')[7].string, t('td')[6].string]
            elif len(t('a')) == 2:
                eventsDict[t.td.i['title']] = [t('a')[1].string, t('td')[1].string, t('td')[2].string, t('td')[3].string, ' ']
        except:
            continue
    return eventsDict

# 时间转换 eg. 1:20.73 -> 80.73
def format_time(t):
    if ':' in t:
        t = t.split(':')
        t = float(t[0]) * 60 + float(t[1])
    return float(t)

# 获取在校期间的最好成绩
def get_best_oncampus(wcaid, entertime, leavetime):
    rootURL = 'https://www.worldcubeassociation.org/'
    resultHTML = getHTMLText(rootURL + 'persons/' + wcaid)
    soup = bs(resultHTML, 'html.parser')

    # 获取所有比赛名和对应日期的字典
    comp_date_dic = {}
    all_ = [item.strip().strip(',') for item in soup.find_all('script')[-1].get_text().strip().split('\n')]
    i = 0
    while i < len(all_):
        if all_[i][:6] == '"name"':
            comp = all_[i].split(':')[1].strip().strip('"')
            # print(comp)
            if '\\u0026' in comp:
                comp = comp.replace('\\u0026', '&')
            i += 4
            date = all_[i].split(':')[1].strip().strip('"')
            if '-' in date:
                date = date.split('-')
                date[0] = date[0].strip() + ', '
                date[1] = date[1][-4:]
                date = ''.join(date)
            date = ''.join(str(datetime.datetime.strptime(''.join(date), '%b %d, %Y')).split()[0].split('-'))
            comp_date_dic[comp] = date
        i += 1

    # pprint(comp_date_dic)

    # 获取在校期间最好成绩
    personal_best = {}
    events = ['333', '222', '444', '555', '666', '777', '333bf', '333fm', '333oh', 'clock', 'minx', 'pyram', 'skewb', 'sq1', '444bf', '555bf', '333mbf']
    for e in events:
        personal_best[e] = {'single':[float('inf'), '', '', ''], 'avg':[float('inf'), '', '', '']}
    personal_best['333mbf'] = {'single':[[float('-inf'), float('inf')], '', '', ''], 'avg':[[float('-inf'), float('inf')], '', '', '']}  # 多盲计分
        
    tbody_list = soup('tbody')
    for tbody in tbody_list[2:]:
        try: event = tbody.get('class')[0].split('-')[-1]
        except: continue
        if event == '333ft': continue
        tr_list = tbody.find_all('tr', {'class':'result'})
        for tr in tr_list:
            # print(tr)
            temp = tr.find('td', {'class':'competition'}).text.strip()
            if temp:
                comp = temp
            date = comp_date_dic[comp]
            if int(entertime) < int(date) < int(leavetime):
                if event == '333mbf':      # 多盲计分
                    try:
                        single = tr.find('td', {'class':'single'}).text.strip()
                        temp = single.split()
                        score = 2 * int(temp[0].split('/')[0]) - int(temp[0].split('/')[1])
                        single_time = [score, format_time(temp[1])]
                    except: single = single_time = [float('-inf'), float('inf')]
                    try: 
                        avg = tr.find('td', {'class':'average'}).text.strip()
                        temp = avg.split()
                        score = 2 * int(temp[0].split('/')[0]) - int(temp[0].split('/')[1])
                        avg_time = [score, format_time(temp[1])]
                    except: avg = avg_time = [float('-inf'), float('inf')]
                    # print(single_time, single, comp)
                else:
                    try:
                        single = tr.find('td', {'class':'single'}).text.strip()
                        single_time = format_time(single)
                    except: single = single_time = float('inf')
                    try: 
                        avg = tr.find('td', {'class':'average'}).text.strip()
                        avg_time = format_time(avg)
                    except: avg = avg_time = float('inf')
                # print(event, comp, single_time, avg_time)
                if event == '333mbf':    # 多盲计分
                    if single_time[0] > personal_best[event]['single'][0][0] or (single_time[0] == personal_best[event]['single'][0][0] and single_time[1] < personal_best[event]['single'][0][1]):
                        personal_best[event]['single'] = [single_time, single, comp, date]
                    if avg_time[0] > personal_best[event]['avg'][0][0] or (avg_time[0] == personal_best[event]['avg'][0][0] and avg_time[1] < personal_best[event]['avg'][0][1]):
                        personal_best[event]['avg'] = [single_time, single, comp, date]
                else:
                    if single_time < personal_best[event]['single'][0]:
                        personal_best[event]['single'] = [single_time, single, comp, date]
                    if avg_time < personal_best[event]['avg'][0]:
                        personal_best[event]['avg'] = [avg_time, avg, comp, date]
    return personal_best

if __name__ =='__main__':

    # pprint(get_best('2014wenc01'))
    res = get_best_oncampus('2013LINK01', '20130910', '20210701')
    pprint(res)
