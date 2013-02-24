#!/usr/bin/env python
import urllib2
import re
import sys
bom = 'http://www.bom.gov.au'
mt_staplton_radar = '/products/IDR663.loop.shtml'
img_regexp = r'(theImageNames\[\d\] = ")(/radar/)(.*\.png)".*'

web_page = urllib2.urlopen(bom+mt_staplton_radar)
directory = './'
if len(sys.argv) > 1:
	directory = sys.argv[1]
for image in re.finditer(img_regexp,web_page.read()):
    open(directory+image.group(3),'wb').write(urllib2.urlopen(bom+image.group(2)+image.group(3)).read())


