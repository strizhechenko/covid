#!/usr/bin/env python3
# coding: utf-8

from covid.utils import url2soup
import json
from pathlib import Path
import logging


class Data(dict):
    def __repr__(self):
        return f"cases: {self['cases']:5} dead: {self['dead']:3} recovered: {self['recovered']:5} " \
               f"solved {self['solved']:6.2f}% sick {self['sick']:5}"


def ekb_raw_data_fetch():
    soup = url2soup('http://све.рф/стопвирус')
    table = soup.find('table', attrs={'class': 'region-table'})
    data = dict()
    data['cases'], data['recovered'], data['dead'], data['tests'] = [int(td.text) for td in
                                                                     table.find('tr').find_all('td')]
    return data


def ekb_raw_data_read(filename):
    with open(filename) as fp:
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
    for filename in sorted(Path('/root/covid/').iterdir()):
        if str(filename).endswith('.json'):
            try:
                print(filename.name.replace('.json', ''), Data(ekb_raw_data_process(ekb_raw_data_read(filename))))
            except json.decoder.JSONDecodeError:
                logging.exception(filename.name)


if __name__ == '__main__':
    ekb_all()
