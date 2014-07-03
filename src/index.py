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
"""

from __future__ import print_function, unicode_literals

import sys
import os
import sqlite3
import csv

from workflow import Workflow

from config import INDEX_DB, DATA_FILE

log = None


def create_index_db():
    log.info('Creating index database')
    con = sqlite3.connect(INDEX_DB)
    with con:
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE books(id INT, author TEXT, title TEXT, url TEXT)")
        cur.execute(
            "CREATE VIRTUAL TABLE search USING fts3(id, author, title)")


def update_index_db():
    log.info('Updating index database')
    con = sqlite3.connect(INDEX_DB)
    with con:
        cur = con.cursor()
        with open(DATA_FILE, 'rb') as file:
            reader = csv.reader(file, delimiter=b'\t')
            for row in reader:
                id_, author, title, url = [v.decode('utf-8') for v in row]
                id_ = int(id_)
                cur.execute("""INSERT OR IGNORE INTO
                            books (id, author, title, url)
                            VALUES (?, ?, ?, ?)""", (id_, author, title, url))
                cur.execute("""INSERT OR IGNORE INTO
                            search (id, author, title)
                            VALUES (?, ?, ?)
                            """, (id_, author, title))
                log.info('Added {} by {} to database'.format(title, author))


def main(wf):
    if not os.path.exists(INDEX_DB):
        create_index_db()
    update_index_db()
    log.info('Index database update finished')


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
