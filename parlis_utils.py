#!/usr/bin/env

import sys
import os
import httplib2

def get_http_client():
    h = httplib2.Http(disable_ssl_certificate_validation=True)
    h.add_credentials( 'SOS', 'Open2012' )
    return h
