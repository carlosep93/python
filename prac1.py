#!/usr/bin/python

import sys
import re

from HTMLParser import HTMLParser

allrest=[]

class restaurant: 

    def afegir_nom(self,nom):
        self.nom = nom

    def afegir_adreca(self,adreca):
        self.adreca = adreca  

    def afegir_latitut(self,latitut):
        self.latitut = latitut

    def afegir_longitut(self,longitut):
        self.longitut = longitut

    def afegir_telefon1(self,telefon):
    	self.telefon1 = telefon

    def afegir_telefon2(self,telefon):
    	self.telefon2 = telefon    

    def afegir_barri(self,barri):
    	self.barri = barri

    def afegir_districte(self,districte):
    	self.districte = districte


        
# creem una subclasse i sobreescribim el metodes del han
class MHTMLParser(HTMLParser):

    crest = restaurant()
    ctag = ""
    aux = False;

    def handle_starttag(self, tag, attrs):
        self.ctag = tag
        self.aux = False
        if tag == 'v:vcard':
            self.crest = restaurant()

    def handle_endtag(self, tag):
        self.ctag = ""
        if tag == 'v:vcard':
            allrest.append(self.crest)

    def handle_data(self, data):
    	data = re.sub(',','.',data)
        if self.ctag == 'v:fn':
            self.crest.afegir_nom(data)
       	if self.ctag == 'v:street-address':
	    	self.crest.afegir_adreca(data)
        if self.ctag == 'v:latitude':
            self.crest.afegir_latitut(data)
        if self.ctag == 'v:longitude':
            self.crest.afegir_longitut(data) 
        if self.ctag == 'rdf:value':
        	if data[0] == '+':
        		if not hasattr(self.crest,'telefon1'):
        			self.crest.afegir_telefon1(data)
        		else:
        			self.crest.afegir_telefon2(data)
        if self.ctag == 'xv:neighborhood':
        	self.crest.afegir_barri(data)
        if self.ctag == 'xv:district':
        	self.crest.afegir_districte(data)				        

f = open('restaurants.rdf', 'rb') # obre l'arxiu
rdfSource = f.read()                            
f.close()

parser = MHTMLParser()
parser.feed(rdfSource)
print "Nom," + "Adreca," + "Latitut," + "Longitut," + "Telefon1," + "Telefon2," + "Barri," + "Districte"  
for r in allrest:
	s = r.nom + ","
	if hasattr(r,'adreca'):
		s = s +  r.adreca + ","
	else:
		s = s + ","
	if hasattr(r,'latitut'):
		s = s +  r.latitut + ","
	else:
		s = s + ","	
	if hasattr(r,'longitut'):
		s = s +  r.longitut + ","
	if hasattr(r,'telefon1'):
		s = s +  r.telefon1 + ","
	else:
		s = s + ","		
	if hasattr(r,'telefon2'):
		s = s +  r.telefon2 + ","
	else:
		s = s + ","	
	if hasattr(r,'barri'):
		s = s +  r.barri + ","
	else:
		s = s + ","
	if hasattr(r,'districte'):
		s = s +  r.districte + ","
	else:
		s = s + ","			
	print s

