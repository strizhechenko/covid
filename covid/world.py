import logging

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
    """
    выдернуть статистику по заражениям и смертям.
    PyPDF2 ставит переносы посреди строк, так что работаем на уровне слов.
    :param text: распарсенный PyPDF'ом текст страницы
    """
    words, word = list(reversed(text.split())), None
    while word != "Globally":
        word = words.pop()
    cases = ""
    while True:
        word = words.pop()
        if word == "confirmed":
            break
        else:
            cases += word
    while ")" not in word:
        word = words.pop()
    deaths = ""
    while True:
        word = words.pop()
        if word == "deaths":
            break
        else:
            deaths += word
    print("{0:12} {1}".format("cases", cases))
    print("{0:12} {1}".format("dead", deaths))


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
