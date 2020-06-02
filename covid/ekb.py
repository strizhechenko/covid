from covid.utils import url2soup


def ekb():
    soup = url2soup('http://све.рф/стопвирус')
    table = soup.find('table', attrs={'class': 'region-table'})
    data = dict()
    data['cases'], data['recovered'], data['dead'], data['tests'] = [int(td.text) for td in table.find('tr').find_all('td')]
    data['solved'] = (data['recovered'] + data['dead']) * 100 / data['cases']
    data['sick'] = data['cases'] - data['recovered'] - data['dead']
    for key, value in data.items():
        if key == 'solved':
            print("{0:12} {1:.2f}%".format(key, value))
        else:
            print("{0:12} {1}".format(key, value))
