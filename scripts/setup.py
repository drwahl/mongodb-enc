#!/usr/bin/python
# vim: set expandtab:
"""
**********************************************************************
GPL License
***********************************************************************
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

***********************************************************************/

:author: Brian Carpio
:email: bcarpio@thetek.net
:web: http://www.briancarpio.com

"""
import sys
import argparse
import config


def main():
    """ This script creates the default node definition """

    col = config.main()

    cmd_parser = argparse.ArgumentParser(description='Add Default Node To Mongodb ENC')
    cmd_parser.add_argument('-a', '--action', dest='puppet_action', choices=['append', 'new'], help='Append Or Recreate Default Node', required=True)
    cmd_parser.add_argument('-c', '--class', dest='puppet_class', help='Specify a puppet class', action='store', required=True)
    cmd_parser.add_argument('-m', '--classparameters', dest='class_params', help='Specify multiple parameters for a class with each -m', action='append', required=False)
    args = cmd_parser.parse_args()

    paramclass = {}
    paramclass[args.puppet_class] = ''
    col.ensure_index('node', unique=True)

    if not args.class_params:
        paramkeyvalue = ''
    else:
        paramkeyvalue = {}
        for param in args.class_params:
            paramvalue = []
            paramkey = ''
            for pkey in param.split(','):
                paramkey = pkey.split('=')[0]
                if "=" in pkey:
                    paramvalue.append(pkey.split('=')[1])
                else:
                    paramvalue = ''
                paramkeyvalue[paramkey] = paramvalue
        paramclass[args.puppet_class] = paramkeyvalue

    if args.puppet_action == 'append':
        d = { 'node' : 'default', 'enc' : { 'classes': paramclass }}
        check = col.find_one({ 'node' : 'default' }, {'node': 1})
        if not check:
            print "Default Node Doesn't Exist, Please Add It First"
            sys.exit(1)
        ec = col.find_one({ 'node' : 'default'})
        ec['enc']['classes'].update(paramclass)
        col.remove({ 'node' : 'default'})
        col.insert(ec)

    if args.puppet_action == 'new':
        d = { 'node' : 'default', 'enc' : { 'classes': paramclass }}
        check = col.find_one({ 'node' : 'default' }, {'node': 1})
        if check:
            col.remove({ 'node' : 'default'})
        col.insert(d)

if __name__ == "__main__":
    main()
