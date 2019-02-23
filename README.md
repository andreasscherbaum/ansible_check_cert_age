# ansible_check_cert_age

Ansible filter which checks the age (remaining valid time) of a certificate


# Installation

Create a subfolder _filter_plugins_ in your Playbook directory. Place the file _cert_age.py_ in _filter_plugins_.


# Usage

In your Playbook, specify this filter on the certificate filename, and supply the minimum number of days the cert must be valid.

## Example 1:

```
- name: Cert is valid
  debug:
    msg: "{{ ('/path/to/signed.crt')|check_cert_age(15) }}

```

This will print _0_ if the cert is valid for the number days, and _1_ otherwise.


## Example 2:

```
- name: Renew cert
  shell: ...
  when: ('/path/to/signed.crt')|check_cert_age(15) == "1"
```

This will execute the Play when the cert is about to expire.
