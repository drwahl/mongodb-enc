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
    """ This script adds nodes to the mongodb enc """

    col = config.main()
    cmd_parser = argparse.ArgumentParser(description='Add Nodes To Mongodb ENC')
    cmd_parser.add_argument('-a', '--action', dest='puppet_action', choices=['append', 'new'], help='Append Or Recreate Default Node', required=True)
    cmd_parser.add_argument('-n', '--node', dest='puppet_node', help='Puppet Node Hostname', required=True)
    cmd_parser.add_argument('-c', '--class', dest='puppet_class', help='Specify a class to add to a node', action='store')
    cmd_parser.add_argument('-m', '--classparameters', dest='class_params', help='Can specify multiple class paramters each with -m. Requires a class to be specified', action='append')
    cmd_parser.add_argument('-p', '--param', dest='puppet_param', help='Can specify multiple parameters (global variables) each with -p', action='append')
    cmd_parser.add_argument('-i', '--inherit', dest='puppet_inherit', help='Define a node to inherit classes from', action='store')
    cmd_parser.add_argument('-e', '--environment', dest='environment', help='Optional, defaults to "production"', default='production')
    args = cmd_parser.parse_args()

    if args.puppet_node == args.puppet_inherit != 'default' :
        print "ERROR: Node name and inherit name can not be the same"
        sys.exit(1)

    if args.puppet_class:

        c = {}
        for pclass in args.puppet_class:
            c[pclass] = ''

    if args.puppet_param:
        args.puppet_param = dict([arg.split('=') for arg in args.puppet_param])

    if args.puppet_inherit:
        ck = col.find_one({ "node" : args.puppet_inherit})
        if not ck:
            print "ERROR: Inherit node does not exist, please add "+args.puppet_inherit+" and then retry"
            sys.exit(1)

    if args.puppet_action == 'new':
        if not args.puppet_inherit:
          print "ERROR: You Need To Define PUPPET_INHERIT"
          sys.exit(1)
        check = col.find({ 'node' : args.puppet_node }, {'node': 1})
        for document in check:
            node = document['node']
            if node == args.puppet_node:  
                print args.puppet_node+" Exists In Mongodb. Please Remove Node"


        if args.puppet_class:
            paramclass = {}
            if not args.class_params:
                paramkeyvalue = ''
            else:
                paramkeyvalue = {}
                for param in args.class_params:
                    paramvalue = []
                    paramkey = ''
                    for pkey in param.split(','):
                        paramkey = pkey.split('=')[0]
                        paramvalue.append(pkey.split('=')[1])
                        paramkeyvalue[paramkey] = paramvalue
            paramclass[args.puppet_class] = paramkeyvalue
            d = { 'node' : args.puppet_node, 'enc' : { 'classes': paramclass, 'environment' : args.environment }}
        else:
            d = { 'node' : args.puppet_node, 'enc' : { 'environment' : args.environment }}

        if args.puppet_param:
            d['enc']['parameters'] = args.puppet_param

        if args.puppet_inherit:
            d['inherit'] = args.puppet_inherit

        col.ensure_index('node', unique=True)
        col.insert(d)
		
    if args.puppet_action == 'append':

        node = col.find_one({ 'node' : args.puppet_node})
        if node == None:
            print "ERROR: Not Node In Mongo ENC. Please Use -a new"
            sys.exit(1)

        if args.puppet_class:
		
            if 'classes' in node['enc']:
                node['enc']['classes'].update(c)
            else:
                node['enc']['classes'] = c
            c = node['enc']['classes']
            col.update({ 'node' : args.puppet_node}, { '$set': { 'enc.classes' : c }})

        if args.puppet_param:
			
            if 'parameters' in node['enc']:
                node['enc']['parameters'].update(args.puppet_param)
            else:
                node['enc']['parameters'] = args.puppet_param
            p = node['enc']['parameters']
            col.update({ 'node' : args.puppet_node}, { '$set': {'enc.parameters' : p}})

        if args.puppet_inherit:
            node['enc']['inherit'] = args.puppet_inherit
            col.update({ 'node' : args.puppet_node}, { '$set' : {'inherit' : args.puppet_inherit}})
				

if __name__ == "__main__":
    main()
