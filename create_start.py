#!/usr/bin/env python
################################################################################
# Script to create missing "start pages" in all your name spaces in a Dokuwiki
# Note: pages created/edited outside the Dokuwiki editor will not be updated
# in the Dokuwiki search cache (thus the "move" plugin will not work with them)
#
# Usage: 
#  'create_start.py [<dokuwiki_root>/]data/pages/<wiki_dir> ["tag1 tag2 .."]'
# 	https://www.dokuwiki.org/config:startpage
# The script:
#   - assumes your name spaces are in .../data/pages/
#   - creates a start page template in all name spaces without one
#   - takes at least one argument
#      - a (relative) directory ending with data/pages/<namespace>
#      - optional extra argument: a (quoted) string with Dokuwiki tags
#
# Dokuwiki extensions you need with this:
#  - https://www.dokuwiki.org/plugin:addnewpage (for the create page form)
#  - https://www.dokuwiki.org/plugin:newpagetemplate (for advanced templates)
#  - optional: 
#    - https://www.dokuwiki.org/plugin:tag
#    
# Create the templates you use in the default folder 'pagetemplates', e.g.
#   newpgtpl1, newpgtpl2 and - for a start page in a new namespace: startpage
#
# Run as the apache user from cron - /etc/cron.d/dokuwiki - or manually
# Works with Python 2.6 - 3.6
#
# Joachim la Poutre' 2017-12
################################################################################
import sys, os, re

def ctemplate(wikidir,tags):
    """ (str[, str]) -> NoneType

    Search a Dokuwiki directory (first string) for 
    sub-directories without a 'start.txt', 
    in all these directories create a the start pate, optionally using
    the second ("quoted") string for the "tags"

    """

    for dirpath, subdirs, files in os.walk(wikidir):
        if not 'start.txt' in files:
            myfile = open(dirpath+'/start.txt', 'w')
            dwpath = dirpath.rstrip('/')
            title = dwpath.split('/')[-1]
            dwpath = re.sub('.*data/pages/', '', dwpath)           
            dwpath = dwpath.replace('/',':')+":start"
            lines = ['{{tag>'+tags+' }}\n','\n',
                     '====== '+title.capitalize()+' ======\n',
                     "Create a new page using the form and drop-down menu's",'\n',
                     '  - Select a name space on the left','\n',
                     "  - In the second field specify the page to create:",'\n'
                     "    * A new page in the selected namespace: ''namespace:pagename''"'\n',
                     "    * A new sub namespace: **''newnamespace:start''**",'\n'
                     "  - Select the required template from the right menu<div>",'\n',
                     "{{NEWPAGE#pagetemplates:newpgtpl1|Simple template,pagetemplates:newpgtpl2|Template with link,pagetemplates:startpage|Start page}}",
                     "\n</div>",'\n','\n',
                     '[['+dwpath+'|Back to top]]\n','\n','\n','\n','<sub>\n',
                     'Created: %Y-%m-%d','\n','</sub>\n']
            myfile.writelines(lines)
            myfile.close()

if len(sys.argv) < 2:
    print("Usage: ",sys.argv[0]," [/<wiki_root>/<wiki_dir>]data/pages/ns [<'tag1 [tag2]'>]")
elif not os.access(sys.argv[1], os.W_OK):
    print("Directory ",sys.argv[1]," is not writable!")
elif len(sys.argv) == 2:
    tags = " "
    ctemplate(sys.argv[1],tags)
elif len(sys.argv) == 3:    
    ctemplate(sys.argv[1],sys.argv[2]) 
else:
    print("Usage: ",sys.argv[0]," [/<wiki_root>/<wiki_dir>]data/pages/ns [<'tag1 [tag2]'>]")

