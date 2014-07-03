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
Convert the Gutenberg RDF data dump to a TSV file.

The script expects the data dump from
http://www.gutenberg.org/wiki/Gutenberg:Feeds#The_Complete_Project_Gutenberg_Catalog
to be extracted into the same directory (i.e. the `epub` directory is
in the same directory as this script.)

Usage:

python catalogue_to_tsv.py > books.tsv
"""

from __future__ import print_function, unicode_literals

import sys
import os
import csv
from lxml import etree


NS_DC = '{http://purl.org/dc/terms/}'
NS_PG = '{http://www.gutenberg.org/2009/pgterms/}'
NS_RDF = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'

resource_tag = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'
title_tag = '//{}title'.format(NS_DC)
author_tag = '//{}creator/{}agent/{}name'.format(NS_DC, NS_PG, NS_PG)
book_id_tag = '//{}isFormatOf'.format(NS_DC)
book_id_attrib = '{}resource'.format(NS_RDF)


def iter_books(dirpath):
    for root, dirnames, filenames in os.walk(dirpath):
        for filename in filenames:
            if filename.endswith('.rdf'):
                yield os.path.join(root, filename)


def tidy(text):
    text = text.replace('\r', '')
    text = text.replace('\n', ' - ')
    return text


def parse_book(path):
    data = {}
    tree = etree.parse(path)
    title = tree.findtext(title_tag)
    if not title:
        return None
    author = tree.findtext(author_tag)
    if not author:
        return None
    data['title'] = tidy(title)
    data['author'] = tidy(author)
    elems = tree.findall(book_id_tag)
    if not elems:
        return None
    id_ = elems[0].attrib[book_id_attrib]
    data['url'] = 'http://www.gutenberg.org/{}'.format(id_)
    data['id'] = id_.split('/')[1]
    return data


def main():
    writer = csv.writer(sys.stdout, delimiter=b'\t', quoting=csv.QUOTE_MINIMAL)
    count = 0
    for i, path in enumerate(iter_books('epub')):
        count += 1
        print(os.path.basename(path), file=sys.stderr)
        book = parse_book(path)
        if not book:
            continue
        i += 1
        for k, v in book.items():
            book[k] = unicode(v).encode('utf-8')
        writer.writerow((book['id'], book['author'],
                         book['title'], book['url']))


if __name__ == '__main__':
    main()
