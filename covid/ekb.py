from covid.utils import url2soup


def ekb():
    soup = url2soup('http://све.рф/стопвирус')
    table = soup.find('table', attrs={'class': 'region-table'})
    data = dict()
    data['cases'], data['recovered'], data['tests'] = [int(td.text) for td in table.find('tr').find_all('td')]
    for key, value in data.items():
        print("{0:12} {1}".format(key, value))
