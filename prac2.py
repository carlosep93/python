#!/usr/bin/python

import sys
import urllib
import math
import xml.etree.ElementTree as ET
import csv
from collections import defaultdict
from decimal import Decimal

sock = urllib.urlopen("http://wservice.viabicing.cat/getstations.php?v=1")
xmlSource = sock.read()
sock.close()

root = ET.fromstring(xmlSource)

columns = defaultdict(list)



def distancia(lat1,long1, lat2, long2):
	r = 6317
	dlat = ((lat2-lat1)*math.pi)/180
	dlong = ((long2-long1)*math.pi)/180
	lat1 = (lat1*math.pi)/180
	lat2 = (lat2*math.pi)/180
	
	a = (math.sin(dlat/2))**2 + math.cos(lat1) * math.cos(lat2) * (math.sin(dlong/2))**2 
	c = 2* math.atan2(math.sqrt(a),math.sqrt(1-a))
	d = r*c
	return d

def comprovar(attr,rest):
	if attr[0] == '(' or type(attr) == tuple:
		ret = True
		if attr[0] == '(':
			attr = eval(attr)
		for i in range(0, len(attr)):
			ret = ret and comprovar(attr[i],rest)

	elif attr[0] == '[' or type(attr) == list:
		ret = False
		if attr[0] == '[':
			attr = eval(attr)
		for i in range(0, len(attr)):
			ret = ret or comprovar(attr[i],rest)

	else:
		if attr[0] == "'":
			attr = eval(attr)
		if attr in rest:
		 	ret = True
		else:
			ret = False
	return ret		 	


def insertar (list,tuple):
	if list == []:
		list.append(tuple)
	else :
		i = 0
		j = len(list)-1
		found = False	
		while i <= j and not found:
			m = (i + j)/2
			if m >= len(list)-1:
				break
			if list[m][1] <= tuple[1] and list[m+1][1] >= tuple[1]:
				list.insert(m+1,tuple)
				found = True
			elif list[m][1] <= tuple[1] and list[m+1][1] <= tuple[1]:
				i = m+1
			else:
				j = m -1					
		if not found:
			if list[0][1] >= tuple[1]:
				list.insert(0,tuple)
			else:	
				list.append(tuple)

def printlist (list):
	#s = ""
	#for i in range(0,len(list)):
	#	s = s + " " + list[i][0]
	#return s
	print "  <ul>"
	for i in range(0,len(list)):
		print "    <li>", list[i][0], "(", list[i][2], ")", "</li>" 
	print "  </ul>"



with open('restaurants.csv') as f:
	reader = csv.DictReader(f)
	for row in reader:
		for (k,v) in row.items():
			columns[k].append(v)



print "<!DOCTYPE html>"
print "<meta charset=\"utf-8\">" 
print "<html>"
print "<head>"
print "<style>"
print "table,th,td {"
print "border:1px solid black;"
print "border-collapse:collapse;"
print "}"
print "th,td"
print "{"
print "padding:5px;"
print "}"
print "</style>"
print "</head>"
print "<body>"
print ""
print "<p> Els nombres entre parentesi son el nombre de places o bicicletes lliures </p>"
print "<table>"
print "<tr>"
print "  <th>Nom</th>"
print "  <th>Adreca</th>"
print "  <th>Latitut</th>"
print "  <th>Longitut</th>"
print "  <th>Telefon1</th>"
print "  <th>Telefon2</th>"
print "  <th>Barri</th>"
print "  <th>Districte</th>"
print "  <th>Estacions bicing places lliures </th>"
print "  <th>Estacions bicing bicis lliures </th>"
print "</tr>"

for i in range(0,len(columns['Nom'])):
	if comprovar(sys.argv[1],columns['Nom'][i]):
		lat = float(columns['Latitut'][i])
		long = float(columns['Longitut'][i])
		laparcament = []
		lbicis = []
		for n in root.findall('station'):
			latb = float(n.find('lat').text)
			longb = float(n.find('long').text)
			d = distancia(lat,long,latb,longb)
			if d <= 1:
				if int(n.find('slots').text) > 0:
					insertar(laparcament,(n.find('street').text,d,int(n.find('slots').text)))
	    		if int(n.find('bikes').text) > 0:	
	    			insertar(lbicis,(n.find('street').text,d,int(n.find('bikes').text)))		
		print "<tr>"
		print "  <td>", columns['Nom'][i], "</td>"
		print "  <td>", columns['Adreca'][i], "</td>"
		print "  <td>", columns['Latitut'][i], "</td>"
		print "  <td>", columns['Longitut'][i], "</td>"
		print "  <td>", columns['Telefon1'][i], "</td>"
		print "  <td>", columns['Telefon2'][i], "</td>"
		print "  <td>", columns['Barri'][i], "</td>"
		print "  <td>", columns['Districte'][i], "</td>"
		print "  <td>" 
		printlist(laparcament) 
		print "  </td>"
		print "  <td>" 
		printlist(lbicis)
		print "  </td>"
		print "</tr>"			
    		
print "</table>"
print "</body>"
print "</html>"







