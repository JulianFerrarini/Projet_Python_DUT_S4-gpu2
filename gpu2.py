def sendmail(fichierTXT,sujet,email, fichierVCS):	
	
	
	toaddr = email#-----------------------------------------------------email destinataire
 
	msg = MIMEMultipart()
 
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Projet python"#-----------------------------------sujet du mail
	fichierTXT = open(fichierTXT,"r")
	body = fichier.read()
 
	msg.attach(MIMEText(body, 'plain'))
 
	filename = fichierVCS
	attachment = open(fichierVCS, "rb")#--------------------------------fichier piece jointe
 
	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
	msg.attach(part)
 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "alarmeRT06")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
	
	
def suppr(i):#----------------------------------------------------------supprimer fichier txt et vcs 
	os.remove(i+".txt")
	os.remove(i+".vcs")

def createEmail(i):#----------------------------------------------------creation d email
	Email= i +"123456789"+("@unice.fr")
	return(Email)

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time 
import csv
import os

fromaddr = "alarme.incendiert@gmail.com"#-------------------------------email de boite envoie
FICHIERS=[] #-----------------------------------------------------------listes fichiers a traiter
AutreFichier=0 # -------------------------------------------------------si utilisateur veut ajouter des fichiers a traiter => 1 sinon 0
while AutreFichier ==0:
	print("fichiers disponibles:")
	for fic in os.listdir("vcs"):
		print(fic) #----------------------------------------------------on affiche la liste des fichiers vcs disponibles dans le repertoire vcs
	fichier=input("entrer le nom du fichier :  ") # --------------------l utilisateur choisit le fichier qu il veut traiter
	if fichier not in os.listdir("vcs"):
		print("le fichier n'est pas disponible")
	else :
		if fichier in FICHIERS : #--------------------------------------on regarde si l utilisateur a deja selectionner ce fichier
			repFichier=input("fichier deja ajoute voulez vous continuer ? oui/non  ")
			if repFichier == "oui":
				FICHIERS.append(fichier)#-------------------------------on ajoute le fichier a la liste des fichiers a traiter si utilisateur decide de continuer
		else : #--------------------------------------------------------si le fichier n a pas encore ete selectionner
			FICHIERS.append(fichier)#-----------------------------------on ajoute le fichier a la liste des fichiers a traiter 
		rep=input("voulez vous entrer un autre fichier ? oui/non  ") #--on demande si utilisateur veut entrer un autre fichier
		if rep=="non": 
			AutreFichier=1 #------------------------------------------------ce qui correspond a l utilisateur ne veut pas d'autre fichier / sinon on reprend la boucle 
		
		
for nomFichier in FICHIERS: #-------------------------------------------on traite les fichiers choisis
	NomFichier="vcs/"+nomFichier #--------------------------------------on se place dans le repertoire vcs
	f=open(NomFichier, 'r')#--------------------------------------------on ouvre le fichier
	l=f.readlines()#----------------------------------------------------on lit les lignes
	taille=len(l)#------------------------------------------------------on regarde la taille du fichier nb lignes
	NowDate=time.strftime("%Y%m%d", time.localtime()) #-----------------date actuel
	#print(NowDate)
	d=5#----------------------------------------------------------------les 5 premieres lignes des fichiers vcs ne contiennent pas d information, le premier horraire commence a la ligne 5
	fin=17#-------------------------------------------------------------le premier horraire se termine a la ligne 17
	listePROF=[]#-------------------------------------------------------liste des professeurs
	continuer =0 #------------------------------------------------------si l utilisateur souhaite continuer malgre que la date soit expire
	
	while fin < taille and continuer !=2: #-----------------------------on parcour la fichier par horraire jusqu a la fin du fichier  tant que la variable continuer ne vaut pas 2 (2 => date anterieur et on ne veut pas continuer)
		for i in l[d:fin]: #--------------------------------------------on parcour les lignes d un horraire
			if "DESCRIPTION"  in i :#-----------------------------------on selectionne les infos de la ligne description
				listeD=i.split(":")
				prof=listeD[3]
				prof=prof.split(" ")
				prof=prof[0]
			if "SUMMARY" in i :#----------------------------------------on selectionne les infos de la ligne summary
				listeS=i.split(":")
				listeS=listeS[1].split("/")
				matiere=listeS[0]
				mType=listeS[1]
				groupe=listeS[2]
				periode=listeS[3]
				section=listeS[4]
			if "LOCATON" in i :#----------------------------------------on selectionne les infos de la ligne location
				listeL=i.split(":")
				salle=listeL[1]
			if "DTSTART" in i:#-----------------------------------------on selectionne les infos de la ligne dtstart
				listeDTSTART=i.split(":")
				date=listeDTSTART[1]
				annee= date[0:4]
				mois=date[4:6]
				jour=date[6:8]
				heure=date[9:11]
				heure=int(heure)+2
				minute=date[11:13]
			if "DTEND" in i :#------------------------------------------on selectionne les infos de la ligne dtend
				listeDTEND=i.split(":")
				date2=listeDTEND[1]
				annee2=date2[0:4]
				mois2=date2[4:6]
				jour2=date2[6:8]
				heure2=date2[9:11]
				heure2=int(heure2)+2
				minute2=date2[11:13]
		date=str(annee)+str(mois)+str(jour) # --------------------------on slectionne la date du 1er horraire du fichier
		if date<NowDate and continuer ==0:#-----------------------------on compare cette date avec la date actuelle
			choix=input("fichier : "+nomFichier+" date deja passée voulez vous continuer ? oui/non ")
			if choix == "non" :
				continuer =2
				
			else :
				continuer =1	
		if continuer==1 or continuer ==0 :		
			#print(str(prof) +"à cour le"+ str(jour) + str(mois) + str(annee) + " à " + str(heure) + "h" + str(minute) + " pour la matiere" + str(matiere) +"pour un "+ str(mType)+ "du groupe" + str(groupe))
			nomTXT=prof+".txt"
			nomVCS=prof+".vcs"
			entete=0#---------------------------------------------------entete fichier vcs (5 premieres lignes d un fichier vcs)
			if prof not in listePROF:
				listePROF.append(prof)
				fichierVCS=open(nomVCS,'a')
				fichierTXT=open(nomTXT,'a')
				fichierTXT.close( )
				fichierVCS.close()
			else :
				entete=1
			NomFichier="vcs/"+nomFichier
			f=open(NomFichier, 'r')
			l=f.readlines()
			if entete==0 :#---------------------------------------------si l entete n a pas encore ete ajoute
				fichierVCS=open(nomVCS,'a')#----------------------------on ouvre le fichier vcs
				for n in range (0,4):#----------------------------------on parcour les 5 premieres lignes
					fichierVCS.write(l[n])#-----------------------------on les ajoute au fichier vcs
			else :	
				fichierVCS=open(nomVCS,'a')#ouverture fichier vcs
			fichierTXT=open(nomTXT,'a')#-------------------------------ouverture fichier txt
			fichierTXT.write("Vous avez cours le "+ str( jour )+" " + str( mois ) + " "+str( annee ) + " de " + str(heure) + "h" + str(minute) + " à "+str(heure2)+ "h"+str(minute2)+ " pour la matiere " + str( matiere ) +" pour un "+ str( mType )+ " du groupe " + str( groupe ) +"\n")
			D=d-1#------------------------------------------------------debut paragraphe a ajouter au fichier vcs prof
			FIN=fin-1#--------------------------------------------------fin paragraphe a ajouter au fichier vcs prof
			
			for ligne in range (D,FIN):#--------------------------------on parcour les lignes pour l horraire
				fichierVCS.write(l[ligne])#-----------------------------on les ajoute au fichier vcs du prof
			d=d+12#-----------------------------------------------------on decale de 12 lignes le debut de l horraire suivant 
			fin=fin+12#-------------------------------------------------on decale de 12 lignes la fin de l horraire suivant
			fichierTXT.close( )#----------------------------------------fermeture fichier txt
		
for prof in listePROF:
	nomVCS=prof+".vcs"#-------------------------------------------------non fichier vcs
	fichierVCS=open(nomVCS,'a')#----------------------------------------ouverture fichier vcs de chaque prof
	fichierVCS.write("END:VCALENDAR")#----------------------------------ligne fin fichier vcs
	fichierVCS.close()#-------------------------------------------------on ferme le fichier vcs
Femail=open("ENS/ensProjet.csv",'r')#-----------------------------------fichier email
Lemail=Femail.readlines()#----------------------------------------------lignes email
LISTEemail=[]#----------------------------------------------------------liste email
for nomPROF in listePROF :
	nom=nomPROF+".txt"#-------------------------------------------------non fichier txt avec info cours du prof
	fichier= open (nom,'r')#--------------------------------------------ouverture du fichier txt
	l=fichier.readlines()#----------------------------------------------on lit les lignes
	print(nomPROF)#-----------------------------------------------------affichage nom prof
	for j in l:
		print(j)#-------------------------------------------------------affichage des cours du prof
	for n in LISTEemail:
		if nomPROF in n :#----------------------------------------------si le nom est dans le fichier email
			Email= n.split(";")
			Email= Email[3]
			print(Email)#-----------------------------------------------affichage email
			LISTEemail.append(i)#---------------------------------------on ajoute email a la liste des emails

	if nomPROF not in LISTEemail :#-------------------------------------si le nom prof est pas dans le fichier email
		Email=createEmail(nomPROF)#-------------------------------------creation de l email 
		print(Email)
	toaddrs = Email #---------------------------------------------------definiton email de destination
	fichierTXT = i+".txt"#----------------------------------------------texte a envoyer en mail
	fichierVCS=i+".vcs"#------------------------------------------------piece jointe au mail permettant au prof de telecharger son GPu perso
	#sendmail(fichierTXT, 'Voici mon sujet',toaddrs,fichierVCS) #envoie du mail
for i in listePROF :
	suppr(i)#-----------------------------------------------------------suppression des fichiers 
