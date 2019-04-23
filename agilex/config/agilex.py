from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Expedientes, documentos y formas"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"name": "Expediente",
					"label": "Expedientes",
				},
				{
					"type": "doctype",
					"name": "Transcripcion",
					"label": "Transcripciones",
				},
				{
					"type": "doctype",
					"name": "Forma",
					"label": "Formas"
				}
			]
		},
		{
			"label": _("Configuraci&oacute;n"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"name": "Transcriptores",
					"label": "Transcriptores"
				}
			]
		}
		
	]
