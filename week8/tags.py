#!/usr/bin/python

import sys, re, subprocess
import collections

# there are python libraries which provide a  better way to fetch web pages
m=[]
m2=[]
flag = 0
for url in sys.argv[1:]:
    if url == "-f":
        flag = 1
    else:
        p = subprocess.Popen(["wget","-q","-O-",url], stdout=subprocess.PIPE)
        for line in iter(p.stdout.readline, ""):
            m += re.findall(r'<[^!][^>]*>', line)
        for html in m:
        	html = re.sub(r'\s[^>]*>', '>', html)
        	html = html.replace("<", ">")
        	html = html.replace("/", ">")
        	html = html.replace(">", "")
        	m2.append(html)
        #print m2
        d = collections.defaultdict(int)
        for tags in m2:
        	tags = tags.lower();
        	d[tags] += 1
        if (flag == 0):
            for key in sorted(d):
            	print "%s %s" % (key, d[key])
        else:
            for key in sorted(d, key=d.get):
                print "%s %s" % (key, d[key])
    

