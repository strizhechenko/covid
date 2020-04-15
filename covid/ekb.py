from covid.utils import url2soup


def ekb():
    soup = url2soup('http://све.рф/стопвирус')
    table = soup.find('table', attrs={'class': 'region-table'})
    cases, recovered, tests = [int(td.text) for td in table.find('tr').find_all('td')]
    print("{0:10} {1}".format("cases", cases))
    print("{0:10} {1}".format("recovered", recovered))
    print("{0:10} {1}".format("tests", tests))
