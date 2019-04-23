from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Clasificaci&oacute;n"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"name": "Tipo de Documento",
					"label": "Tipos de documento"
				},
				{
					"type": "doctype",
					"name": "Cuadro de Clasificacion",
					"label": "Cuadro de clasificaci&oacute;n (no se usa)"
				}
			]
		},
		{
			"label": _("Elementos codicol&oacute;gicos"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"name": "Tipo de Papel",
					"label": "Tipos de papel",
				},
				{
					"type": "doctype",
					"name": "Disposicion del Texto",
					"label": "Disposici&oacute;n del texto"
				},
				{
					"type": "doctype",
					"name": "Tipo de Letra",
					"label": "Tipos de letra"
				},
				{
					"type": "doctype",
					"name": "Presentacion",
					"label": "Presentaci&oacute;n"
				},
				{
					"type": "doctype",
					"name": "Tipo de sello",
					"label": "Tipos de sello",
				},
				{
					"type": "doctype",
					"name": "Estado de Conservacion",
					"label": "Estado de conservaci&oacute;n"
				}
			]
		},
		{
			"label": _("Listas"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"name": "Desplegable",
					"label": "Desplegables"
				},
				{
					"type": "doctype",
					"name": "Desplegable Opciones",
					"label": "Opciones de los desplegables"
				}
			]
		}
		
	]
