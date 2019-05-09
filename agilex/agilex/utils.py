# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe
import frappe.defaults
import re
from frappe.utils import nowdate, cstr, flt, cint, now, getdate
from frappe.modules.utils import scrub
from frappe import throw, _
from bs4 import BeautifulSoup

#obtiene un código del tipo dd-dd
@frappe.whitelist()
def obtener_codigo_expediente(tipo_de_documento, name):
	codigo_tipo_de_documento = frappe.db.get_value("Tipo de Documento", tipo_de_documento, fieldname="codigo") or ''
	contador = cint(frappe.db.count("Expediente", {"tipo_de_documento": tipo_de_documento, "name": ("!=", name or "")})) + 1

	return "{0}-{1}".format(codigo_tipo_de_documento, contador)

#obtiene un código del tipo dd-dd-dd
def obtener_codigo_transcripcion(expediente, name):
	contador = cint(frappe.db.count("Transcripcion", {"expediente": expediente, "name": ("!=", name or "")})) + 1
	return "{0}-{1}".format(expediente, contador)

@frappe.whitelist()
def obtener_html(presentacion_critica):
	if presentacion_critica:
		#obtenemos el patron de los números de línea {dd}
		patron_numeros = re.compile(r'({\d+})') 
		#obtenemos el patron de los corchetes {dd}
		patron_corchetes = re.compile(r'[{}]')
		#obtenemos el patron de los números de hoja {hxxxx}
		patron_numero_hoja = re.compile(r'{h.+?}')
		
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

def actualiza_formas_pc(presentacion_critica, transcripcion):
	if presentacion_critica:
		#limpiamos de caracteres innecesarios ", . : ; ..."
		patron_caracteres = re.compile(r'[\.\,\:\;]')
		presentacion_critica = patron_caracteres.sub('',presentacion_critica)

		#convertimos a minúsculas el texto
		presentacion_critica = presentacion_critica.lower()

		#separamos por palabras
		formas_completo = presentacion_critica.split()
		tamano = len(formas_completo)

		formas = list(set(formas_completo))

		for forma in formas:
			name = "{0}-{1}".format(transcripcion, forma)
			if not frappe.db.exists("Forma", name):
				new_forma = frappe.get_doc({
					"doctype": "Forma",
					#"name": name,
					"forma": forma,
					"transcripcion": transcripcion,
					"tipo_de_transcripcion": "Presentación crítica"})

				new_forma.autoname()
				
				new_forma.frecuencia_absoluta = formas_completo.count(forma)
				new_forma.frecuencia_relativa = (new_forma.frecuencia_absoluta/tamano)*100
				new_forma.forma_reversa = new_forma.forma[::-1]

				new_forma.insert()
			else:
				new_forma = frappe.get_doc("Forma", name)

				new_forma.frecuencia_absoluta = formas_completo.count(forma)
				new_forma.frecuencia_relativa = (new_forma.frecuencia_absoluta/tamano)*100
				new_forma.forma_reversa = new_forma.forma[::-1]

				new_forma.save()


@frappe.whitelist()
#Carga plantilla del repositorio de ficheros
def load_transcriptores_por_defecto(parentfield):
	
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
