# -*- coding: utf-8 -*-
#!/usr/bin/python
from urllib2 import urlopen
from timetable.models import Department, Event, EventType, FieldOfStudy, Instructor, Location, Modul, ModulFieldOfStudy, Semester, ModulType
import os, sys, re

class BAInfParser():
	def fetch(self):
		department, created = Department.objects.get_or_create(name='Institut für Informatik')

		r = urlopen('http://www.informatik.uni-leipzig.de/ifi/studium/studiengnge/ba-inf/ba-inf-module.html')
		with open('/tmp/ba-inf.pdf', 'w') as f:
			f.write(r.read())
		os.system('pdf2txt.py -o /tmp/a.out /tmp/ba-inf.pdf');

		fobj = open("/tmp/a.out", "r")

		counter=0
		counter2 =0
		founddate=0

		index=1
		flag=0
		flagInhalt=0

		liste = []
		liste2 = []
		titles =[]
		numbers=[]

		letzteZeile='leer'

		title=''
		lp='0'
		inhalt=''
		modultype=''

		for line in fobj: 
			liste.insert(counter, line)
			counter+=1

			#modulnummer
			if counter==1:
				number=line

			#Leistungspunkte
			if '5 LP = 150 Arbeitsstunden (Workload)' in line:index+=1; lp=5
			if '10 LP = 300 Arbeitsstunden (Workload)' in line:index+=1; lp=10

			#modultitel bachelor

			#inhalt
			if line.strip() == 'Teilnahmevoraus-': flagInhalt=0
			if flagInhalt==1: inhalt += line
			if line.strip() =='Inhalt': flagInhalt=1


			#???if counter==20: print line	#institut

			letzteZeile=line

			#str = line
			match = re.search(r'\d\d?\.\s\w+\s\d{4}', line)
			# If-statement after search() tests if it succeeded
			#if match:                      
				#print 'found', match.group() ## 'found word:cat'
				#founddate+=1
				#print founddate

			if 'Vertiefungsmodul'==line.strip(): modultype='Vertiefungsmodul'
			if 'Ergänzungsfach'==line.strip(): modultype='Ergänzungsfach'
			if 'Kernmodul'==line.strip(): modultype='Kernmodul'
			if 'Seminarmodul'==line.strip(): modultype='Seminarmodul'
			if 'Ergänzungsfach Medizinische Informatik'==line.strip(): modultype='Ergänzungsfach Medizinische Informatik'


			#neuer eintrag
			if 'Modulnummer' in line:
				flag+=1

				#if index != flag: print title+ str(index) + ' '+str(flag)
				#print lp
		
				#print inhalt

				counter=0
				liste2=liste
				liste[:]=[]
				#print title
				if counter2>0:
					titles.append(title.strip()	)
					numbers.append(number.strip())
					#print titles[counter2-1]+numbers[counter2-1]
				counter2+=1


				type, created = ModulType.objects.get_or_create(name=modultype)

				modul, created = Modul.objects.get_or_create(number=number.strip())
				if created or not modul.name:
					modul.name = title.strip()
				modul.lp=lp
				modul.modultype=type
				modul.description=inhalt
				modul.department = department
				#modul.fields='no clue what that is'
				modul.save()






				title=''
				number=''
				lp='0'
				inhalt=''
				modultype=''

		fobj.close()



class MAInfParser():
	def fetch(self):
		department, created = Department.objects.get_or_create(name='Institut für Informatik')

		r = urlopen('http://www.informatik.uni-leipzig.de/ifi/studium/studiengnge/ma-inf/ma-inf-module.html')
		with open('/tmp/ma-inf.pdf', 'w') as f:
			f.write(r.read())

		os.system('pdf2txt.py -o /tmp/a.out /tmp/ma-inf.pdf');

		fobj = open("/tmp/a.out", "r")

		counter=0
		counter2 =0
		index=0
		founddate=0

		liste = []
		titles =[]
		numbers=[]


		title=''
		flag=0
		letzteZeile=''
		lp='0'
		modultype=''
		verw=''
		 
		for line in fobj: 
			liste.append(line)

			#print line

			#flag
			if 'Modulnummer' in line:
				flag=1


			match = re.search(r'\d\d?\.\s\w+\s\d{4}', line)


			#if match and flag==0:
				#nothing
				#liste[:]=[]		

			if match and flag==1:
				flag=0
				#print str(len(liste)) +liste[12].strip()                     
				#modul komplett in liste

				#test
				#print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
		
				#schleife for
					#if match2 = re.search(r'\w+', letzteZeile) and 'Vertiefungsmodul' in line: print line + letzteZeile
				a=''
				b=''
				flagInhalt=0
				flagException=0
				flagNumber=0
				flagModultitle=0
				flagVerw=0

				inhalt=''
				modulNumber=''
				modulName=''
				modulName2=''
				lp='0'
				modultype=''
				verw=''


				for i in liste:
					#print i
					a=b
					b=i

					if 'Vertiefungsmodul'==i.strip() or 'Ergänzungsfach'==i.strip() or 'Kernmodul'==i.strip() or 'Seminarmodul'==i.strip() or 'Ergänzungsfach Medizinische Informatik'==i.strip():
						modulName=a
						#print modulName
			

					if 'Vertiefungsmodul'==i.strip(): modultype='Vertiefungsmodul'
					if 'Ergänzungsfach'==i.strip(): modultype='Ergänzungsfach'
					if 'Kernmodul'==i.strip(): modultype='Kernmodul'
					if 'Seminarmodul'==i.strip(): modultype='Seminarmodul'
					if 'Ergänzungsfach Medizinische Informatik'==i.strip(): modultype='Ergänzungsfach Medizinische Informatik'

					if flagModultitle==2:modulName2=i;flagModultitle=0;#print modulName2
					if flagModultitle==1: flagModultitle=2
					if i.strip()=='Modultitel': flagModultitle=1



					if flagException==1: 
						#print inhalt
						if i.strip()=='keine': flagInhalt=0
				
					if i.strip()=='Teilnahmevoraus-' and flagInhalt>3: flagInhalt=0
					if flagInhalt>0: inhalt+=i;flagInhalt+=1; flagException=1
					if i.strip()=='Inhalt': flagInhalt=1

					if flagNumber==1: modulNumber=i;flagNumber=0;#print modulNumber
					if 'Modulnummer' == i.strip():
						flagNumber=1

					#Leistungspunkte
					if '5 LP = 150 Arbeitsstunden (Workload)' in i: lp='5'#;print '5'
					if '10 LP = 300 Arbeitsstunden (Workload)' in i: lp='10'#;print '10'



					if modulName.strip()=='': modulName=modulName2
					#if modulName != modulName2: print modulName.strip() + 'xxx' + modulName2.strip()
					

					#Verwendbarkeit
					if flagVerw==2 and i.strip()=='':flagVerw=0
					if flagVerw==2: verw+=i
					if flagVerw==1: flagVerw=2		
					if i.strip()=='Verwendbarkeit':flagVerw=1


				if modulName.strip()=='der Medizin': modulName=modulName2
				type, created = ModulType.objects.get_or_create(name=modultype)

				#print 'yyy'+verw+'xxx'	
				flagVerw=0

				#verwendbarkeit ist noch als String gespeichert -> auseinanderpluecken
				#
				#
				#
				#


				
				modul, created = Modul.objects.get_or_create(number=modulNumber.strip())	
				if created or not modul.name:
					modul.name = modulName.strip()
				if created or not modul.modultype:
					modul.modultype=type
				modul.department = department
				#	print 'xxxx'
					#modul.fields='no clue what that is'		#verwendbarkeit		

				modul.description=inhalt
				modul.lp=int(lp)
				modul.save()

				liste[:]=[]


			letzteZeile=line

		#letztes Modul noch nicht eingetragen
		########
		#class Modul(models.Model):
		#	number = models.CharField(max_length=256, unique=True, null=True)
		#	name = models.CharField(max_length=1024)
		#	lp = models.IntegerField(blank=True, null=True)
		#	modultype = models.ForeignKey(ModulType, blank=True, null=True)
		#	description = models.TextField(blank=True, null=True)
		#	department = models.ForeignKey(Department, blank=True, null=True)
		#	fields = models.ManyToManyField(ModulFieldOfStudy, null=True)


		fobj.close()