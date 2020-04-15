#!/usr/bin/env python3

import argparse
import os

from covid_ru import main as ru

from covid.ekb import ekb
from covid.world import who_fetch_latest_pdf, who_print_stat, who_read_first_page, recovered_stat


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--pdf")
    parser.add_argument("--fetch-pdf", action='store_true', default=False)
    parser.add_argument("-a", "--auto", action='store_true', default=False)
    parser.add_argument("-r", "--russia", action='store_true', default=False)
    parser.add_argument('-e', '--ekb', action='store_true', default=False)
    parser.add_argument("--all", action='store_true', default=False)
    args = parser.parse_args()
    if args.all:
        args.russia = True
        args.ekb = True
        args.auto = True
    if not (args.auto or args.pdf or args.fetch_pdf or args.russia or args.ekb):
        args.auto = True
    if args.auto or args.fetch_pdf:
        args.pdf = who_fetch_latest_pdf()
        if args.fetch_pdf:
            return
    if args.ekb:
        print('# - EKB ------------------')
        ekb()
    if args.russia:
        print('# - Russia ---------------')
        for _key, _value in ru().items():
            print("{0:12} {1}".format(_key, _value))

        if args.all:
            print('# - World ----------------')
    if (not args.russia and not args.ekb) or args.all:
        who_print_stat(who_read_first_page(args.pdf))
        print("{0:12} {1}".format('recovered', recovered_stat()))
    if args.auto:
        os.unlink(args.pdf)


if __name__ == '__main__':
    main()
