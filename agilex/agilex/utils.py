# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe
import frappe.defaults
from frappe.utils import nowdate, cstr, flt, cint, now, getdate
from frappe.modules.utils import scrub
from frappe import throw, _
from bs4 import BeautifulSoup
import re

#obtiene un código del tipo dd-dd
@frappe.whitelist()
def obtener_codigo_expediente(tipo_de_documento):
	codigo_tipo_de_documento = frappe.db.get_value("Tipo de Documento", tipo_de_documento, fieldname="codigo") or ''
	contador = cint(frappe.db.count("Expediente", {"tipo_de_documento": tipo_de_documento})) + 1
	return "{0}-{1}".format(codigo_tipo_de_documento, contador)

#obtiene un código del tipo dd-dd-dd
def obtener_codigo_transcripcion(expediente):
	contador = cint(frappe.db.count("Transcripcion", {"expediente": expediente})) + 1
	return "{0}-{1}".format(expediente, contador)

@frappe.whitelist()
def obtener_html(presentacion_critica):
	#obtenemos el patron de los números de línea
	patron_numeros = re.compile(r'({\d+})') 
	#obtenemos el patron de los corchetes {dd}
	patron_corchetes = re.compiler(r'[{}]')
	#obtenemos el patron de los números de hoja
	patron_numero_hoja = re.compiler(r'{h.+?}')

	lista_numeros = patron_numeros.findall(presentacion_critica)

	#para mejorar la eficiencia, eliminamos los duplicados
	lista_numeros = list(dict.fromkeys(lista_numeros))

	#recorremos los números con formato {dd} para quitarle los corchetes y reemplazar el texto con los estilos necesarios
	for numero in lista_numeros:
		numero_sin_corchetes = patron_corchetes.sub('',numero)
		presentacion_critica = presentacion_critica.replace(numero,"<span class='linea'>{0}</span>".format(numero_sin_corchetes))

	return presentacion_critica

@frappe.whitelist()
def obtener_texto_plano_desde_html(raw_html):
	cleantext = BeautifulSoup(raw_html, "lxml").text

	return cleantext