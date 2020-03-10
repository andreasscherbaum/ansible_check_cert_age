#!/usr/bin/env python

from ansible.errors import AnsibleError
import os
import sys
from ansible.module_utils._text import to_native
from ansible.module_utils._text import to_text
import subprocess


class FilterModule(object):
    ''' Query filter '''

    def filters(self):
        return {
            'cert_exists': self.cert_exists
        }


    def cert_exists(self, cert_path):
        '''Query a certificate (1st parameter) and check if the certificate exists
           Returns 0 if the cert exists
           Returns 1 if the cert does not exist
        '''

        result = 1
        # first check if the cert exists
        if (os.path.exists(cert_path) is True and os.access(cert_path, os.R_OK) is True):
            result = 0

        return(to_text(str(result)))
