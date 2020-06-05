#!/usr/bin/python
#
# 4 de juny 2020 - joan <joan@riseup.net> 
# joancatala.net
#
# Tinc un hortet, i aquest programa m'organitza les fotos automaticament, aixi les puc compartir
# facilment. Jo faig les fotos i les publique al directori fotos-smartphone, i aquest programa
# ja s'encarrega de copiar aquest directori, redimensionar-ho i mostrar-ho en una pàgina HTML.
# I xim pum.
#

#####################################################################################
# Modulets
#####################################################################################

import time, os
from sty import fg, bg, ef, rs, RgbFg

#####################################################################################
# M'agrada pintar el titol, benvingut a la republica independent del meu terminal
#####################################################################################

os.system('clear')
print ("=========================================================================================================\n")
print ("GENERADOR DE LA GALERIA HTML DE L'HORTET DIY " + bg.yellow + "(Versio 1.0)" + bg.rs + "\n")
print ("=========================================================================================================\n")

#####################################################################################
# Em munte un fitxer "llistat.txt" que despres l'ordene a "llistat_ordenat.txt"
#####################################################################################

fitxer = open ( 'llistat.txt', 'w' )

for base, dirs, files in os.walk('fotos-smartphone'):

    lista=[]
    lista.append(base)
    fitxer.write(base + '\n')

fitxer.close()

# Si el fitxer galeria.php existeix, no fa res (escriu un punt '.', però si no existeix no dona error i continua.)

mode = 'a' if os.path.exists('galeria.php') else 'w'
with open('galeria.php', mode) as f:
    f.write('.')

os.system('rm galeria.php')

os.system('cat llistat.txt  | sort -V > llistat_ordenat.txt')

# Ací li lleve "/home/joan/Documents/hortet" i tambe "-smartphone" a la ruta dels directoris, 
# per a que es visualitze bé a la galeria d'imatges. El directori amb les imatges thumbs sera "fotos"
# L'ordre sed pot estar delimitada amb el caracter / com tambe amb @ o amb :, s@hola@adeu@g reemplaça "hola" per "adeu".
os.system('sed -i "s@-smartphone@@g" llistat_ordenat.txt')
os.system('rm llistat.txt')

print (fg.green + "[0]" + fg.rs + " Comencem a generar les imatges que trobarem al directori fotos-smartphone.")
time.sleep(2)

print (fg.green + "[1]" + fg.rs + " Ja he preparat el fitxer amb el llistat ordenat de directoris de la galeria.")
time.sleep(2)

#####################################################################################
# Em prepare les imatges. Faig un backup i llance un convert masiu
#####################################################################################

print (fg.green + "[2]" + fg.rs + " Preparant directori d'imatges. Aquest procès pot durar un poc...")

# Si existeix publicar.tar.gz, l'esborrem
if os.path.exists('publicar.tar.gz'): 
    os.system('rm -rf publicar.tar.gz')

# Si existeix el directori fotos (que son els antigs thumbs, esborra-ho)
if os.path.exists('fotos'): 
    os.system('rm -rf fotos')

os.system('cp -rf fotos-smartphone fotos')

print (fg.green + "[3]" + fg.rs + " Ara anem a comprimir la resolució de les imatges a mostrar. Aquest procès va a durar un poque més... ")

os.system('find fotos/ -name "*.*" -execdir mogrify -resize 20% {} \;')

print (fg.green + "[4]" + fg.rs + " Els fitxers s'han comprimit correctament!")
time.sleep(2)


#####################################################################################
# Ara pinte cada linea de "llistat_ordenat.txt" i lliste els fitxers de dins
#####################################################################################

# Ara llegire el "listat_ordenat.txt" excepte la primera linea, per a que no em
# mostre els subdirectoris per primera vegada, per aixo "[1:]"
with open('llistat_ordenat.txt') as fp:
    line = fp.readline()[1:]
    cnt = 1
    while line:
        # Ara pinte una linea, es a dir, un directori
        #print(line.strip())

        for base, dirs, files in os.walk(line.strip()):

            # Amb nova base i el rsplig, transforme una ruta completa i nomes pinte el ultim directori
            # per exemple /home/joan/directori sera "directori". Aixi aquest sera el titol de les galeries.
            nova_base = base.rsplit('/', 1)[1]
            ruta_relativa= base.rsplit('/', 1)[1] # per a les galeries d'imatges
            # DEBUG
            #print ("____________________________________________________________________________\n")
            #print (base.rsplit('/', 1)[1])
            #print ("____________________________________________________________________________\n")
            #print (files)
            #print ("\n\n")
            
            #Inserte cada linea a un fitxer HTML
            f=open("galeria.php","a")
            f.write("<p><h1>" + nova_base + "</h1>\n")
            for valor in files:
                f.write('<img class="imatge" src="' + base + '/' + str(valor) + '" alt="Imatge molona del meu hortet DIY" />\n')
            f.write("</p><br /><br />")

        line = fp.readline()
        cnt += 1


# Tanquem el fitxer generador de la pagina HTML
f.close()

# Esborrem el llistat de directoris
os.system('rm llistat_ordenat.txt')

print (fg.green + "[5]" + fg.rs + " Ja hem generat la galeria de fotos en el fitxer galeria.php!")

os.system('tar cfz publicar.tar.gz fotos galeria.php')
print (fg.green + "[6]" + fg.rs + " Ja està llesta la galeria per a ser pujada al servidor web.")
time.sleep(2)

print (fg.green + "[7]" + fg.rs + " PROGRAMA FINALITZAT.\n\n")
