# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe
import frappe.defaults
import re
from frappe.utils import nowdate, cstr, flt, cint, now, getdate
from frappe.modules.utils import scrub
from frappe.model.naming import make_autoname
from frappe import throw, _
from bs4 import BeautifulSoup

#obtiene un código del tipo ddd-ddd
@frappe.whitelist()
def obtener_codigo_expediente(tipo_de_documento, name):
	if name:
		return name
	else:
		codigo_tipo_de_documento = frappe.db.get_value("Tipo de Documento", tipo_de_documento, fieldname="codigo") or ''
		codigo_tipo_de_documento = formatea_serie(codigo_tipo_de_documento, 3)

		contador = cint(frappe.db.count("Expediente", {"tipo_de_documento": tipo_de_documento, "name": ("!=", name or "")})) + 1
		contador = formatea_serie(contador, 3)

		return "{0}-{1}".format(codigo_tipo_de_documento, contador)

#obtiene un código del tipo ddd-ddd-ddd
def obtener_codigo_transcripcion(expediente, name):
	if name:
		return name
	else:
		contador = cint(frappe.db.count("Transcripcion", {"expediente": expediente, "name": ("!=", name or "")})) + 1
		contador = formatea_serie(contador, 3)
		return "{0}-{1}".format(expediente, contador)

#Actualizado masivo
def actualiza_expedientes():
	expedientes = frappe.get_all('Expediente')

	for expediente in expedientes:
		#exp = frappe.get_doc("Expediente", expediente.get("name"))
		name = expediente.get("name")
		print("{0}".format(name))
		partes = name.split("-")
		ntdoc = cint(partes[0])
		ntdoc = formatea_serie(ntdoc, 3)
		nexp = cint(partes[1])
		nexp = formatea_serie(nexp, 3)
		
		new_name = "{0}-{1}".format(ntdoc, nexp)
		print(new_name)

		print("------")

		frappe.rename_doc('Expediente', name, new_name, force=True)

		frappe.db.set_value('Expediente', new_name, 'expediente_name', new_name)
		frappe.db.commit()
		#exp.save()

#Actualizado masivo
def actualiza_transcripciones():
	transcripciones = frappe.get_all('Transcripcion')

	for transcripcion in transcripciones:
		trans = frappe.get_doc("Transcripcion", transcripcion.get("name"))
		exp = frappe.get_doc("Expediente", trans.get("expediente"))
		name = transcripcion.get("name")
		print("{0}".format(name))
		partes = name.split("-")
		ntdoc = cint(partes[0])
		ntdoc = formatea_serie(ntdoc, 3)
		nexp = cint(partes[1])
		nexp = formatea_serie(nexp, 3)
		ntr = cint(partes[2])
		ntr = formatea_serie(ntr, 3)
		
		new_name = "{0}-{1}-{2}".format(ntdoc, nexp, ntr)
		print(new_name)

		print("------")

		frappe.rename_doc('Transcripcion', name, new_name, force=True)
		
		route = frappe.db.get_value("Tipo de Documento", exp.get("tipo_de_documento"), fieldname="route")
		route = "{0}/{1}".format(route, new_name)

		frappe.db.set_value('Transcripcion', new_name, 'tipo_de_documento', exp.get("tipo_de_documento"))
		frappe.db.set_value('Transcripcion', new_name, 'route', route)
		frappe.db.commit()
		#exp.save()

def formatea_serie(numero, digitos):
	return ('%0'+str(digitos)+'d') % numero

@frappe.whitelist()
def obtener_html(presentacion_critica):
	if presentacion_critica:
		#obtenemos el patron de los números de línea {dd}
		patron_numeros = re.compile(r'({\d+})') 
		#obtenemos el patron de los corchetes {dd}
		patron_corchetes = re.compile(r'[{}]')
		#obtenemos el patron de los números de hoja {hxxxx}
		patron_numero_hoja = re.compile(r'{h.+?}')

		#obtenemos el patron de las negritas *xxx*
		patron_negrita = re.compile(r'(\*\*.+\*\*)')

		#obtenemos el patron de las cursivas *xxx*
		patron_cursiva = re.compile(r'(\*.+\*)')
		
		#Eliminamos el código que puede ser representado como HTML
		presentacion_critica = BeautifulSoup(presentacion_critica, "lxml").text

		#reemplazamos los números de página por un salto <hr>
		lista_paginas = patron_numero_hoja.findall(presentacion_critica)
		for pagina in lista_paginas:
			presentacion_critica = presentacion_critica.replace(pagina, "<hr class='salto_pagina'><span class='numero_pagina'>{0}</span>".format(pagina))

		lista_numeros = patron_numeros.findall(presentacion_critica)
		#para mejorar la eficiencia, eliminamos los duplicados
		lista_numeros = list(dict.fromkeys(lista_numeros))
		#recorremos los números con formato {dd} para quitarle los corchetes y reemplazar el texto con los estilos necesarios
		for numero in lista_numeros:
			numero_sin_corchetes = patron_corchetes.sub('',numero)
			presentacion_critica = presentacion_critica.replace(numero,"<sup class='linea'>{0}</sup>".format(numero_sin_corchetes))

		lista_negritas = patron_negrita.findall(presentacion_critica)

		for negrita in lista_negritas:
			negrita_html = "<b>{0}</b>".format(negrita.replace("*", ""))
			presentacion_critica = presentacion_critica.replace(negrita,negrita_html)

		lista_cursivas = patron_cursiva.findall(presentacion_critica)

		for cursiva in lista_cursivas:
			cursiva_html = "<i>{0}</i>".format(cursiva.replace("*", ""))
			presentacion_critica = presentacion_critica.replace(cursiva, cursiva_html)


	return presentacion_critica

@frappe.whitelist()
def obtener_html_tp(transcripcion_paleografica):
	if transcripcion_paleografica:
		transcripcion_paleografica = transcripcion_paleografica.replace("<","")
		transcripcion_paleografica = transcripcion_paleografica.replace(">","")
		transcripcion_paleografica = obtener_html(transcripcion_paleografica)

	return transcripcion_paleografica

@frappe.whitelist()
def obtener_texto_plano_desde_html(raw_html):
	cleantext = raw_html
	if cleantext:

		#limpiamos de caracteres innecesarios
		cleantext = cleantext.replace(" | ", " ")
		cleantext = cleantext.replace("|", "")

		#obtenemos el patron de margen, rótulos, etc [xxxx: asdf fdsa]
		patron_margen = re.compile(r'(\[.+?: (.+?)\])')
		#tratamos el margen
		lista_margen = patron_margen.findall(cleantext)
		for margen in lista_margen:
			cleantext = cleantext.replace(margen[0], margen[1])
			#frappe.msgprint("{0}<br>{1}".format(margen[0], margen[1]))

		#limpiamos el texto de código html
		cleantext = re.sub(r'(<(.+?)>.+?<\/(.+?)>)',"", cleantext)

		#reemplazamos los caracteres "/"
		cleantext = cleantext.replace("/", "")

	return cleantext

def actualiza_formas(texto, tipo_de_transcripcion, transcripcion_name, eliminar_anteriores=False):
	print("Actualizando formas {0}.".format(tipo_de_transcripcion))

	lformas_ya_guardadas = []
	ldiferencia = []

	formas_ya_guardadas = frappe.db.sql("""select forma from `tabForma`
	where tipo_de_transcripcion=%s and transcripcion=%s order by forma""", (tipo_de_transcripcion, transcripcion_name), as_list=1)

	for f in formas_ya_guardadas:
		lformas_ya_guardadas.append(f[0])

	#frappe.log_error("Formas ya guardadas {0}: {1}".format(tipo_de_transcripcion, lformas_ya_guardadas))

	#limpiamos de caracteres innecesarios ", . : ; ..."
	patron_caracteres = re.compile(r'[\.\,\:\;\(\)\[\]\&\-\—\_\+\=\<\>\…\/\*\º\ª\!\"\'\`]*[0-9]*')
	texto = patron_caracteres.sub('',texto or "")

	#convertimos a minúsculas el texto
	texto = texto.lower()

	#separamos por palabras
	formas_comp = texto.split()


	#eliminamos los que tengan longitud inferior a 2
	formas_completo = [x for x in formas_comp if (len(x)>2)]

	tamano = len(formas_completo)

	formas = list(set(formas_completo))

	#frappe.log_error("Formas {0}: {1}".format(tipo_de_transcripcion, formas))

	#Borrar las formas que ya no existen
	ldiferencia = list(set(lformas_ya_guardadas) - set(formas))
	#frappe.log_error("FDiferencia {0}: {1}".format(tipo_de_transcripcion, ldiferencia))
	
	for forma in ldiferencia or []:
		borra_forma(tipo_de_transcripcion, transcripcion_name, forma)
		#frappe.delete_doc("Forma", frappe.db.sql_list("""select name from `tabForma`
	#where tipo_de_transcripcion=%s and transcripcion=%s and forma=%s""", (tipo_de_transcripcion, transcripcion_name, forma)), for_reload=True)

	for forma in formas or []:
		name = "{0}-{1}".format(transcripcion_name, forma)
		if eliminar_anteriores or not existe_forma(forma, transcripcion_name, tipo_de_transcripcion):
			new_forma = frappe.get_doc({
				"doctype": "Forma",
				"forma": forma,
				"transcripcion": transcripcion_name,
				"tipo_de_transcripcion": tipo_de_transcripcion})

			new_forma.autoname()
			
			new_forma.frecuencia_absoluta = formas_completo.count(forma)
			new_forma.frecuencia_relativa = (new_forma.frecuencia_absoluta/tamano)*100
			new_forma.forma_reversa = new_forma.forma[::-1]

			new_forma.insert()

		else:
			forma_name = obtiene_forma_name(forma, transcripcion_name)
			new_forma = frappe.get_doc("Forma", forma_name)

			new_forma.frecuencia_absoluta = formas_completo.count(forma)
			new_forma.frecuencia_relativa = (new_forma.frecuencia_absoluta/tamano)*100
			new_forma.forma_reversa = new_forma.forma[::-1]

			new_forma.save()

def borra_forma(tipo_de_transcripcion, transcripcion_name, forma):
	frappe.db.sql("""delete from `tabForma`
		where tipo_de_transcripcion=%s and transcripcion=%s and forma=%s""", (tipo_de_transcripcion, transcripcion_name, forma))
	#frappe.delete_doc("Forma", frappe.db.sql_list("""select name from `tabForma`
	#	where tipo_de_transcripcion=%s and transcripcion=%s""", (tipo_de_transcripcion, transcripcion_name)), for_reload=True)

def borra_todas_las_formas():
	frappe.db.sql("""delete from `tabForma`""")

def existe_forma(forma, transcripcion, tipo_de_transcripcion):
	return frappe.db.count("Forma", {"forma": forma, "transcripcion": transcripcion, "tipo_de_transcripcion": tipo_de_transcripcion}) > 0

def obtiene_forma_name(forma, transcripcion):
	"""Returns count of unseen likes"""
	return frappe.db.sql("""select name
			from `tabForma` where 
			forma=%(forma)s
			and transcripcion=%(transcripcion)s
			""", {"forma": forma, "transcripcion": transcripcion})[0][0]

@frappe.whitelist()
#Carga plantilla del repositorio de ficheros
def carga_transcriptores_por_defecto(parentfield):
	
	plantilla = []

	try:
		plantilla = frappe.get_list("Transcripcion Transcriptores", 
								filters={'parent': 'Configuracion del Programa',
										'parenttype': 'Configuracion del Programa',
										'parentfield': parentfield },
								fields="*")
	except Exception as e:
		frappe.msgprint(_("No se ha podido obtener la plantilla"))
		raise e
	
	return plantilla

@frappe.whitelist()
def actualiza_todas_las_transcripciones(expediente=None):
	filters = {}

	mensaje = ""

	if expediente:
		filters["expediente"] = expediente

	transcripciones = frappe.get_list("Transcripcion", fields=["name"], filters = filters)

	for transcripcion in transcripciones:
		trans = frappe.get_doc("Transcripcion", transcripcion.name)
		trans.autogenerar_formas = 1
		print("Guardando transcripcion {0}".format(transcripcion.name))

		trans.save()

		mensaje = "{0}<br>- {1}".format(mensaje, transcripcion.name)

	return mensaje


def can_edit():
	if ("Administrador AGILEX" in frappe.get_roles()):
		return True
	else:
		return False