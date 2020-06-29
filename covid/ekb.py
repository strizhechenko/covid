#!/usr/bin/env python3
# coding: utf-8

from covid.utils import url2soup
import json
from pathlib import Path
import argparse
from datetime import date, timedelta
from copy import deepcopy


class Data(dict):
    def __repr__(self):
        return "cases: {0:5} dead: {1:3} recovered: {2:5} solved {3:6.2f}% sick {4:5}".format(
            self['cases'], self['dead'], self['recovered'], self['solved'], self['sick'])


def ekb_raw_data_fetch():
    soup = url2soup('http://све.рф/стопвирус')
    table = soup.find('table', attrs={'class': 'region-table'})
    data = dict()
    data['cases'], data['recovered'], data['dead'], data['tests'] = [int(td.text) for td in
                                                                     table.find('tr').find_all('td')]
    return data


def ekb_raw_data_read(filename):
    with open(str(filename)) as fp:
        data = next(i for i in json.load(fp)['Items'] if i['IsoCode'] == "RU-SVE")
        keys = list(data.keys())
        data['cases'] = data['Confirmed']
        data['dead'] = data['Deaths']
        data['recovered'] = data['Recovered']
        for key in keys:
            del data[key]
        return data


def ekb_raw_data_process(data):
    data['solved'] = (data['recovered'] + data['dead']) * 100 / data['cases']
    data['sick'] = data['cases'] - data['recovered'] - data['dead']
    return data


def ekb():
    for key, value in ekb_raw_data_process(ekb_raw_data_fetch()).items():
        if key == 'solved':
            print("{0:12} {1:.2f}%".format(key, value))
        else:
            print("{0:12} {1}".format(key, value))


def ekb_all():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--limit', type=int, default=7)
    parser.add_argument('-p', '--predict', type=int)
    args = parser.parse_args()
    data = {}
    for filename in sorted(Path('/root/covid/').iterdir()):
        if filename.name.endswith('.json'):
            key = filename.name.replace('.json', '')
            value = Data(ekb_raw_data_process(ekb_raw_data_read(filename)))
            data[key] = value
    for filename in sorted(data)[-args.limit:]:
        print(filename, data[filename])
    if args.predict:
        acc = dict()
        for key in 'cases', 'dead', 'recovered':
            if key not in acc:
                acc[key] = []
            for filename in sorted(data)[-args.limit:]:
                acc[key].append(data[filename][key])
            _min = min(acc[key])
            _max = max(acc[key])
            acc[key] = (_max - _min) / _min / args.limit
        last_date_str = max(data.keys())
        last_date = date(*map(int, last_date_str.split('.')))
        print('---- predict ----', acc)
        base_data = deepcopy(data[last_date_str])
        prev = deepcopy(base_data)
        for day in range(args.predict):
            today = deepcopy(prev)
            for key in 'cases', 'dead', 'recovered':
                today[key] += round(prev[key] * acc[key] * day)
            print(last_date + timedelta(days=day), Data(ekb_raw_data_process(today)))


if __name__ == '__main__':
    ekb_all()
