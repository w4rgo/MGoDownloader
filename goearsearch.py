# -*- coding: utf-8 -*-
#GOEAR API 
#Author: Francisco Ruiz Valdés (W4rGo)
#
#Version 1.4
#
#TODO - Caracteres especiales hacen que el comando wget no se lanze bien

import urllib2
import sys
import os
#regex
import re
#r = re.compile('Master(.*?)thon')
#m = r.search(str1)
#if m:
    #lyrics = m.group(1)
import unicodedata

#urllib.urlretrieve ("http://www.example.com/songs/mp3.mp3", "mp3.mp3")
class Song:
    numsongs=0 #variable estatica compartida por todas las instancias
    def __init__(self,name=0,code=0,link=0,group=0):
        Song.numsongs+=1  #incrementamos el contador estático
        self.name=name
        self.code=code
        self.num=Song.numsongs
        self.link=link
        self.group=group
        
    def downloadSong(self,folder):
        threads=False
        codigo = self.code
        folder = folder.replace(" ","-")
        linkxml = "http://www.goear.com/tracker758.php?f=" + codigo
        texto = downloadHTML(linkxml)
        textoCortadoAntes = texto.split("<song path=\"")
        textoCortadoDespues = textoCortadoAntes[1].split("\" bild=")
        url = textoCortadoDespues[0]
        segplan=""
        if threads :
            segplan = " %"
        mp3file = urllib2.urlopen(url)
        output = open(folder+ "/" u""+self.name.strip().replace(" ","-") + ".mp3" ,'wb')

        output.write(mp3file.read())
        output.close()
        
        #command=u"wget " + url + " -O " + folder + "/" + u""+self.name.strip().replace(" ","-") + ".mp3" + segplan
        
        #subprocess.call(["wget", url ,"-O",folder,"/",""+u""self.name.strip().replace(" ","-")+ ".mp3"])
        #os.system(command)
 #       os.system(u"wget " + url + " -O " + folder + "/" + u""+self.name.strip().replace(" ","-") + ".mp3" )
##    def getLyrics(self,folder):
##        url = "http://www.goear.com/"+self.link
##        print url
##        page = downloadHTML(url)
##        regExp = re.compile("<pre>"+"(.*?)"+"</pre>")
##            lyrics = regExp.search(page)
##        print lyrics.group(1)
##        #if lyrics is not None:
##        f= open(folder + "/" + self.name, 'w')
##        f.write(page)
##        #	else:
##        #		print "No lyrics"
    def __str__(self): 	#sobrecarga de print
        return str(self.num) + ": " + str(self.name)+" - "+str(self.group) + " - " + str(self.code)

def elimina_tildes(cadena):
	cadena = cadena.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","nh")
	cadena = cadena.replace("Á","A").replace("É","E").replace("Í","I").replace("Ó","O").replace("Ú","U").replace("Ñ","NH")
	cadena = cadena.replace("&","").replace("acute;","").replace("excl;","").replace("quot;","").replace("tilde;","").replace("cedil;","")
	return cadena
#def elimina_tildes_u(cadena):
 #   s = ''.join((c for c in unicodedata.normalize('NFD',unicode(cadena,"UTF-8")) if unicodedata.category(c) != 'Mn'))
  #  return s.decode()

def downloadHTML(url):
	httpFile= urllib2.urlopen ( urllib2.Request ( url))
	httpBody= httpFile.read ()
	httpFile.close()
	return httpBody
	
def downloadGroup(selected,songs, folder):
	if not os.path.exists(folder):
    		os.makedirs(folder)
	if len(selected) == 0:
		for song in songs:
			song.downloadSong(folder)
		#	song.getLyrics(folder)
	for i in selected:
		songs[i].downloadSong(folder)
		#songs[i].getLyrics(folder)


def retrieveList(keyword,numOfPages):
	step=numOfPages
	songs=[]
	parar = 1
	pagenum=1
	keyword = keyword.replace(" ","-")
	while parar:
		page = downloadHTML("http://www.goear.com/search/"+ keyword + "/" + str(pagenum)+"/")
		songsInPage=getSongsInPage(page)
		
		for song in songsInPage:
			print song

		if len(songsInPage)==0:
			parar=0

		if songs != []: 
			songs.extend(songsInPage)
		else:
			songs = songsInPage

		#if(__name__ == '__main__'):
		if (pagenum >= numOfPages):
			return songs
		pagenum += 1
	return songs

def getSongsInPage(page):
	#<a title="Escuchar La Leyenda del Hada y el Mago - rata blanca" href="listen/2c4f40c/la-leyenda-del-hada-y-el-mago-rata-blanca"><span class="songtitleinfo">La Leyenda del Hada y el Mago</span> - <span class="groupnameinfo">rata blanca</span></a>
	
	#Song info part
	begin="<a title=\""
	end="</span></a>"

	regExp = re.compile(begin +"(.*?)"+ end)
	songsInfo = regExp.findall(page)
	songs=[]
	for songInfo in songsInfo:
		
		regExp = re.compile("<span class=\"songtitleinfo\">"+"(.*?)"+ "</span>")
		title = regExp.search(songInfo)
		
		regExp = re.compile("- <span class=\"groupnameinfo\">"+"(.*?)"+"</span></a>")
		group = regExp.search(songInfo)
			
		regExp = re.compile("href=\""+"(.*?)"+ "\">")
		link = regExp.search(songInfo)

		regExp = re.compile("href=\"listen/"+"(.*?)"+ "/")
		code = regExp.search(songInfo)		
		if group is not None:
			group = group.group(1)
		else:
			group="No Group"
		song = Song(elimina_tildes(title.group(1)),code.group(1),elimina_tildes(link.group(1)),elimina_tildes(group))

		songs.append(song)

	return songs
def stringToNumArray(array):

	if array == "":
		return []
	split = array.split(",")
	returnArray=[]
	for entry in split:
		returnArray.append(int(entry.replace(" ","")))
	return returnArray

def getSongByNum(songList,num):
    if len(songList) == 0:
        return None
    for song in songList:
        if int(song.num) == int(num):
            return song
    return None

if(__name__ == '__main__'):

#ejemplo de codigo: 5af64d5
	busqueda = ""
	busqueda = raw_input('Introduce una palabra clave: ')

	songs = retrieveList(busqueda,1)

	adescargar = stringToNumArray(raw_input('Introduce los numeros de las canciones que te interesan separados por comas: '))
	
	downloadGroup(adescargar, songs, directory)

