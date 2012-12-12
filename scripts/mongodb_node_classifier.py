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
import yaml
import sys
import config

def main():
    """ This script is called by puppet  """
    if (len(sys.argv) < 2):
        print "ERROR: Please supply a hostname or FQDN"
        sys.exit(1)

    col = config.main()

    node = sys.argv[1]

    # Find the node given at a command line argument
    d = col.find_one({"node": node}) 
    if d == None:
        print "ERROR: Node "+node+" not found in ENC" 
        sys.exit(1)

    # Check if the node requiers inheritance
    n = col.find_one({"node": node})
    if 'inherit' in n:
        i = True
        while i == True:
            # Grab the info from the inheritance node
            inode = n['inherit']
            if not col.find_one({"node" : inode}):
                print "ERROR: Inheritance node "+inode+" not found in ENC"
                sys.exit(1)
            idict = col.find_one({"node": inode})
            if 'classes' in idict['enc']:
                # Grab the classes from the inheritance node
                iclass = idict['enc']['classes']
                # Apply inheritance node classes to the requested node
                if 'classes' in n['enc']:
                    # Grab the requested node's classes
                    tmp_class_store = d['enc']['classes']
                    # Apply the inheritance node classes
                    d['enc']['classes'] = iclass
                    # Apply the requested node's classes and overrides
                    d['enc']['classes'].update(tmp_class_store)
                else:
                    d['enc']['classes'] = iclass 
            n = col.find_one({"node": inode})
            if 'inherit' not in n:
                i = False

    print yaml.safe_dump(d['enc'], default_flow_style=False)


if __name__ == "__main__":
    main()
