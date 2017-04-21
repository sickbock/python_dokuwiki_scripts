#!/usr/bin/python
################################################################################
# Usage: 'create_template.py <dokuwiki_root>/<wiki_dir> "tag1 tag2 .."'
# https://www.dokuwiki.org/namespace_templates#template_files
# Creates a page template in all name spaces without one
# (Resulting pages rely on a few plugins like dw2pdf, toctweak, ..)
#
# Run as the apache user from /etc/cron.d/dokuwiki
# Works with Python 2.6 - 3.6
#
# Joachim la Poutre' 2017
################################################################################
import sys, os

def ctemplate(wikidir,tags):
    """ (str, str) -> file

    Search a Dokuwiki directory (first string) for 
    sub-directories without a '_template.txt', 
    in all these directories create a template using
    the second string for the "tags"

    """

    for dirpath, subdirs, files in os.walk(wikidir):
        if not '_template.txt' in files:
            myfile = open(dirpath+'/_template.txt', 'w')
            lines = ['{{tag>'+tags+' }}\n',';;#\n','[[?do=export_pdf|PDF export]]\n',
                     ';;#\n','~~CLOSETOC~~\n','~~TOC:1-4~~\n','====== @!FILE@ ======\n',
                     '\n','\n','\n','[[|Back to top]] \\ \n','<sub>\n',
                     'Created: %Y-%m-%d by @NAME@\n','</sub>\n']
            myfile.writelines(lines)
            myfile.close()

if len(sys.argv) != 3:
    print("Usage: ",sys.argv[0]," /<wiki_root>/<wiki_dir> <'tag1 [tag2]'>")
elif not os.access(sys.argv[1], os.W_OK):
    print("Directory ",sys.argv[1]," is not writable!")
else:
    ctemplate(sys.argv[1],sys.argv[2]) 
