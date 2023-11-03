#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import csv
import logging
from argparse import ArgumentParser
from pattern.text.de import conjugate
from pattern.text.de import INFINITIVE, PRESENT, PAST, PARTICIPLE, SINGULAR, PLURAL

# --------------------------------------------------------------------------- #
# conjugate function
# --------------------------------------------------------------------------- #
def get_word_conj_table(word, tense):
    word = word
    verb_table = []

    for i in range(1, 4):
        logging.debug(word)
        verb_table.append(conjugate(word, tense, i, SINGULAR))

    for i in range(1, 4):
        logging.debug(word)
        verb_table.append(conjugate(word, tense, i, PLURAL))

    return verb_table

# --------------------------------------------------------------------------- #
# main routine
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    current_dir = os.path.abspath(os.path.dirname(__file__))
    
    #-------- Parameters
    parser = ArgumentParser(description='Tools script to generate german conuguation.')
    parser.add_argument("verbs", help="can be a verb or a list of verb separate by ','", type = str)
    parser.add_argument("-p", "--path", help="path to CSV file where to write, by default data are just print", default=None)
    parser.add_argument('-v', '--verbose', help='Add debug infos.', action='store_true')
    args = parser.parse_args()

    #-------- Debug set-up
    if(args.verbose):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    #-------- File set-up
    if(args.path and os.path.exists(args.path)):
        generateCSV = True
    else:
        generateCSV = False

    args.verbs.replace(" ", "") # make sure no extra space is kept 
    list_words = args.verbs.split(",")
    output_rows = []

    for w in list_words:
        w = w
        row = [w, "", ""] # for anki cards
        row = row + get_word_conj_table(w, PRESENT)
        row = row + get_word_conj_table(w, PAST)
        row.append(conjugate(w, PAST+PARTICIPLE))
        output_rows.append(row)

    if generateCSV:
        with open(args.path, 'a', encoding='utf-8') as file:
            write = csv.writer(file, delimiter=';', lineterminator='\r')
            for r in output_rows:
                write.writerow(r)
    else:
        for r in output_rows:
            print(r)
