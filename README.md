# ansible_check_cert_age

Ansible filter plugins which checks the age (remaining valid time) of a certificate, or if a certificate exists.


# Installation

Create a subfolder _filter_plugins_ in your Playbook directory. Place the .py script in _filter_plugins_.


# cert_age.py

## Usage

In your Playbook, specify this filter on the certificate filename, and supply the minimum number of days the cert must be valid.

### Example 1:

```
- name: Cert is valid
  debug:
    msg: "{{ ('/path/to/signed.crt')|check_cert_age(15) }}

```

This will print _0_ if the cert is valid for the number days, and _1_ otherwise.


### Example 2:

```
- name: Renew cert
  shell: ...
  when: ('/path/to/signed.crt')|check_cert_age(15) == "1"
```

This will execute the Play when the cert is about to expire.

# cert_exists.py

## Usage

In your Playbook, specify this filter on the certificate filename in order to find out if the certificate already exists.
There is no easy way to loop over many domains/certificates and make Ansible not fail the loop if the certificate does not (yet) exists.

This can be handled for a single cert, by using the _stat_ module. But in a loop this requires moving the entire code block into a separate file, and looping over the domains/certs by including the files. As of now, Ansible can't loop over code blocks with more than one tasks.

### Example

```
- name: Cert exists
  msg: "Certificate file exists: {{ item }}"
  with_dict: "{{ websites }}"
  loop_control:
    loop_var: website
    label: "{{ website.key }}"
  when:
    - (website.key + '/signed.crt')|cert_exists() == "1"
```
