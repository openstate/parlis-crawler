#!/usr/bin/env

import sys
import os
import httplib2

from parlis_settings import settings

def get_http_client():
    h = httplib2.Http(disable_ssl_certificate_validation=True)
    #h.add_credentials( 'SOS', 'Open2012' )
    h.add_credentials(settings['parlis_api_user'], settings['parlis_api_password'])
    return h
