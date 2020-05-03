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


def skip(words, to):
    word = None
    while word != to:
        word = words.pop()


def combine_word(words, until):
    result = ""
    while True:
        word = words.pop()
        if word == until:
            break
        result += word
    return result


def who_print_stat(text, report_type="new"):
    """
    выдернуть статистику по заражениям и смертям.
    PyPDF2 ставит переносы посреди строк, так что работаем на уровне слов.
    :param text: распарсенный PyPDF'ом текст страницы
    :param report_type: версия отчёта, new - новые, old - старые. Отличается начальное слово.
    """
    words = list(reversed(text.split()))
    skip(words, to="Globally")
    cases = combine_word(words, "cases" if report_type == "new" else "confirmed")
    skip(words, to=")")
    deaths = combine_word(words, "deaths")
    print("{0:12} {1}".format("cases", cases))
    print("{0:12} {1}".format("dead", deaths))


def recovered_stat():
    """ WHO почему-то не имеет информации по выздоровевшим. Дёргаем с левого сайта. """
    soup = url2soup("https://www.worldometers.info/coronavirus/coronavirus-cases/")
    recovered = soup.find('div', attrs={'class': 'tabbable-panel-cured'})
    for line in str(recovered).split('\n'):
        if line.strip().startswith('data:'):
            return int(re.sub(r"[^0-9]", "", line.split(',')[-2]))
