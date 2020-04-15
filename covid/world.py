import logging
import re

import PyPDF2
import requests

from covid.utils import url2soup


def who_fetch_latest_pdf():
    """ :return имя скачанного файла """
    soup = url2soup('https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports')
    report_list = soup.find("div", attrs={'id': 'PageContent_C002_Col01'})
    report_list = report_list.find('div', attrs={'class': 'content-block'})
    report = report_list.find('a').attrs['href'].split('?')[0]
    url = 'https://www.who.int' + report
    logging.debug("report url: %s", url)
    filename = report.split('/')[-1]
    pdf = requests.get(url).content
    with open(filename, 'wb') as fd:
        fd.write(pdf)
    return filename


def who_read_first_page(pdf):
    """
    :param pdf: путь до PDF
    :return: текст первой страницы
    """
    fd = open(pdf, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(fd)
    return pdf_reader.getPage(0).extractText()


def who_print_stat(text):
    """ :param text: выдернуть статистику по заражениям и смертям """
    start, stop = "Globally", "European Region"
    do_print = False
    count = "cases"
    for line in text.split('\n'):
        if not line.strip():
            continue
        if stop == line.strip():
            break
        if do_print:
            print("{0:12} {1}".format(count, re.sub(r'[a-z ]', '', line).split('(')[0]))
            if count == "cases":
                count = "dead"
        if start == line.strip():
            do_print = True


def recovered_stat():
    """ WHO почему-то не имеет информации по выздоровевшим. Дёргаем с левого сайта. """
    soup = url2soup("https://www.worldometers.info/coronavirus/coronavirus-cases/")
    recovered = soup.find('td', text="Recovered/Discharged")
    items = [x.text for x in recovered.parent.parent.children if hasattr(x, 'text')]
    needle = False
    for item in items:
        if needle:
            return int(item.strip().split()[0].replace(',', ''))
        if "Recovered/Discharged" in item:
            needle = True
