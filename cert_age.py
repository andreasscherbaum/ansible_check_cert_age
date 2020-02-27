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
            'check_cert_age': self.check_cert_age
        }


    def check_cert_age(self, cert_path, remaining_days):
        '''Query a certificate (1st parameter) and check if the remaining valid
           time is at least as many days as specified in the 2nd parameter
           Returns 0 if the cert is valid for the specified number of days
           Returns 1 if the cert is not valid for that time
        '''

        # first check if the cert exists
        if (os.path.exists(cert_path) is False):
            raise AnsibleError('Not found: %s' % to_native(cert_path))
        if (os.access(cert_path, os.R_OK) is False):
            raise AnsibleError('No access: %s' % to_native(cert_path))

        # there is a slight chance that the file goes away between the time
        # existence and access is checked, but that's ok
        # raising the proper error in the majority of cases is more important

        remaining_time = int(remaining_days) * 86400
        d0 = open(os.devnull, 'w')
        result = subprocess.call(['/usr/bin/openssl', 'x509', '-in', cert_path, '-noout', '-checkend', str(remaining_time)], stdout = d0, stderr = d0)
        if (result != 0):
            # make sure we return '1' for an expiring certificate, or for every error
            result = 1

        return(to_text(str(result)))
