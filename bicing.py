#!/usr/bin/python

import urllib
import xml.etree.ElementTree as ET

sock = urllib.urlopen("http://wservice.viabicing.cat/getstations.php?v=1")
xmlSource = sock.read()
sock.close()

root = ET.fromstring(xmlSource)

#print xmlSource
    
for n in root.findall('station'):
  if int(n.find('bikes').text) >= 1:
	print "Carrer:: "+ n.find('street').text
	print "Bicis lliures: "+ n.find('bikes').text
	
	
	
	       
  
  
  
  
