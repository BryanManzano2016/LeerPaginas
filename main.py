#!/usr/bin/python3
from daemonize import Daemonize
import urllib
from bs4 import BeautifulSoup
import smtplib

#Archivo que guarda el pid del proceso
pid = "/tmp/horaApp.pid"

'''
Funcion que ejecuta el daemon, la cual abrira un archivo para recibir los datos de una pagina
web y enviara una notificacion cuando sea el segundo 30(referente a la hora con div twd
'''

def main():

    with open("/home/personal/Downloads/horas.txt", "a") as horas:

        contador = 0
        while True:

            #Enlazar la pagina con request y luego la abro con urlopen
            enlace = "https://time.is/es/New_York"
            solicitud = urllib.request.Request(enlace)
            solicitud.add_header('User-agent', 'Mozilla/5.0')
            respuesta = urllib.request.urlopen(solicitud)

            #Leer el contenido de la pagina estatica
            data = respuesta.read()

            #Separar los elementos html y obtengo el requerido
            soup = BeautifulSoup(data, "html.parser")
            hora = soup.find("div", attrs = {"id":"twd"})

            #Escribir en el archivo
            horas.write("[" + hora.text + "], ")

            horaSplit = hora.text.split(":")[2]

            if horaSplit[0] == "0":
                horaSplit = int(horaSplit[1])
            else:
                horaSplit = int(horaSplit)

            if horaSplit == 30:
                #Conectar SMTP y el puerto que es el establecido por gmail
                s = smtplib.SMTP('smtp.gmail.com', 587)

                #Empiezo la conexion TLS
                s.starttls()
                s.login("bryanmanzano2@gmail.com", "FisicaX4")
                message = "Alerta es el segundo --- " + str(horaSplit)
                s.sendmail("bryanmanzano2@gmail.com", "bryanmanzano2@gmail.com", message)

                #Cerrar conexion
                s.quit()

                contador += 1

            if contador == 2:
                exit()

#Crear el daemon con la funcion e iniciarlo
daemon = Daemonize(app="test_app", pid=pid, action=main)
daemon.start()

