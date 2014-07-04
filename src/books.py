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
import struct
from time import time

import sqlite3

from workflow import Workflow, ICON_INFO, ICON_WARNING
from workflow.background import run_in_background, is_running

from config import INDEX_DB

log = None


# Search ranking function
# Adapted from http://goo.gl/4QXj25 and http://goo.gl/fWg25i
def make_rank_func(weights):
    """`weights` is a list or tuple of the relative ranking per column.

    Use floats (1.0 not 1) for more accurate results. Use 0 to ignore a
    column.
    """
    def rank(matchinfo):
        # matchinfo is defined as returning 32-bit unsigned integers
        # in machine byte order
        # http://www.sqlite.org/fts3.html#matchinfo
        # and struct defaults to machine byte order
        bufsize = len(matchinfo)  # Length in bytes.
        matchinfo = [struct.unpack(b'I', matchinfo[i:i+4])[0]
                     for i in range(0, bufsize, 4)]
        it = iter(matchinfo[2:])
        return sum(x[0]*w/x[1]
                   for x, w in zip(zip(it, it, it), weights)
                   if x[1])
    return rank


def main(wf):
    # Workflow requires a query
    query = wf.args[0]

    index_exists = True

    # Create index if it doesn't exist
    if not os.path.exists(INDEX_DB):
        index_exists = False
        run_in_background('indexer', ['/usr/bin/python', 'index.py'])

    # Can't search without an index. Inform user and exit
    if not index_exists:
        wf.add_item('Creating search index…', 'Please wait a moment',
                    icon=ICON_INFO)
        wf.send_feedback()
        return

    # Inform user of update in case they're looking for something
    # recently added (and it isn't there)
    if is_running('indexer'):
        wf.add_item('Updating search index…',
                    'Fresher results will be available shortly',
                    icon=ICON_INFO)

    # Search!
    start = time()
    db = sqlite3.connect(INDEX_DB)
    # Set ranking function with weightings for each column.
    # `make_rank_function` must be called with a tuple/list of the same
    # length as the number of columns "selected" from the database.
    # In this case, `url` is set to 0 because we don't want to search on
    # that column
    db.create_function('rank', 1, make_rank_func((1.0, 1.0, 0)))
    cursor = db.cursor()
    try:
        cursor.execute("""SELECT author, title, url FROM
                            (SELECT rank(matchinfo(books))
                             AS r, author, title, url
                             FROM books WHERE books MATCH ?)
                          ORDER BY r DESC LIMIT 100""", (query,))
        results = cursor.fetchall()
    except sqlite3.OperationalError as err:
        # If the query is invalid, show an appropriate warning and exit
        if b'malformed MATCH' in err.message:
            wf.add_item('Invalid query', icon=ICON_WARNING)
            wf.send_feedback()
            return
        # Otherwise raise error for Workflow to catch and log
        else:
            raise err

    if not results:
        wf.add_item('No matches', 'Try a different query', icon=ICON_WARNING)

    log.info('Search for `{}` finished in {:0.3f} seconds'.format(
             query, time() - start))

    # Output results to Alfred
    for (author, title, url) in results:
        wf.add_item(title, author, valid=True, arg=url, icon='icon.png')

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
