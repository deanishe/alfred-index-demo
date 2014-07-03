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

from __future__ import unicode_literals

from workflow import Workflow

wf = Workflow()

INDEX_DB = wf.cachefile('index.db')
DATA_FILE = wf.workflowfile('books.tsv')
