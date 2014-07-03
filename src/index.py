#!/usr/bin/env python
# encoding: utf-8
#
# Copyright © 2014 deanishe@deanishe.net
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2014-07-03
#

"""
Read in data from `books.tsv` and add it to the search index database.

See `catalogue_to_tsv.py` for the generation of the `books.tsv` file.
"""

from __future__ import print_function, unicode_literals

import sys
import os
import sqlite3
import csv
from time import time

from workflow import Workflow

from config import INDEX_DB, DATA_FILE

log = None


def create_index_db():
    """Create a "virtual" table, which sqlite3 uses for its full-text search

    Given the size of the original data source (~45K entries, 5 MB), we'll put
    *all* the data in the database.

    Depending on the data you have, it might make more sense to only add
    the fields you want to search to the search DB plus an ID (included here
    but unused) with which you can retrieve the full data from your full
    dataset.
    """
    log.info('Creating index database')
    con = sqlite3.connect(INDEX_DB)
    with con:
        cur = con.cursor()
        # cur.execute(
        #     "CREATE TABLE books(id INT, author TEXT, title TEXT, url TEXT)")
        cur.execute(
            "CREATE VIRTUAL TABLE books USING fts3(id, author, title, url)")


def update_index_db():
    """Read in the data source and add it to the search index database"""
    start = time()
    log.info('Updating index database')
    con = sqlite3.connect(INDEX_DB)
    count = 0
    with con:
        cur = con.cursor()
        with open(DATA_FILE, 'rb') as file:
            reader = csv.reader(file, delimiter=b'\t')
            for row in reader:
                id_, author, title, url = [v.decode('utf-8') for v in row]
                id_ = int(id_)
                cur.execute("""INSERT OR IGNORE INTO
                            books (id, author, title, url)
                            VALUES (?, ?, ?, ?)
                            """, (id_, author, title, url))
                log.info('Added {} by {} to database'.format(title, author))
                count += 1
    log.info('{} items added/updated in {:0.3} seconds'.format(
             count, time() - start))


def main(wf):
    if not os.path.exists(INDEX_DB):
        create_index_db()
    update_index_db()
    log.info('Index database update finished')


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
