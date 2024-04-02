#!/usr/bin/env python3
#    yaml2script.py
#    Copyright (C) 2024  Daniel Mohr
#    Version: 0.1.0
#
# This script tries to extract the scripts from a '.gitlab-ci.yml' file.
# In this way the scripts inside '.gitlab-ci.yml' can be tested/analyzed for
# example with 'shellcheck'.

import sys
import warnings

import yaml


def main():
    if len(sys.argv) != 3:
        print('yaml2script [filename] [job name]')
        sys.exit(1)
    with open(sys.argv[1]) as fd:
        data = yaml.load(fd, Loader=yaml.SafeLoader)
    script = {}
    if 'extends' in data[sys.argv[2]]:
        for key in ['before_script', 'script', 'after_script']:
            if data[sys.argv[2]]['extends'] in data:
                if key in data[data[sys.argv[2]]['extends']]:
                    script[key] = data[data[sys.argv[2]]['extends']][key]
            else:
                warnings.warn('job to extend not available: ignoring')
    for key in ['before_script', 'script', 'after_script']:
        if key in data[sys.argv[2]]:
            script[key] = data[sys.argv[2]][key]
    script_code = ['#!/usr/bin/env sh']
    for key in ['before_script', 'script', 'after_script']:
        if key in script:
            script_code += script[key]
    print('\n'.join(script_code))


if __name__ == "__main__":
    main()
