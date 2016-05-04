#!/usr/bin/env python
#-*- coding:utf-8 -*-

###############################################################
# CLAM: Computational Linguistics Application Mediator
# -- WSGI script for launching CLAM (from within a webserver) --
#       by Maarten van Gompel (proycon)
#       http://ilk.uvt.nl/~mvgompel
#       Induction for Linguistic Knowledge Research Group
#       Universiteit van Tilburg
#
#       Licensed under GPLv3
#
###############################################################

import os
import sys

sys.path.append('/exp2/mre/ticclops/ticclops')
os.environ['PYTHONPATH'] = '/exp2/mre/ticclops/ticclops'

os.environ['language'] = 'grc'
import ticclopsinapache
import clam.clamservice
application = clam.clamservice.run_wsgi(ticclopsinapache)
