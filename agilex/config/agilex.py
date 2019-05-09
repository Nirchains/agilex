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
					"label": "<i class='octicon octicon-package'></i> Expedientes",
				},
				{
					"type": "doctype",
					"name": "Transcripcion",
					"label": "<i class='octicon octicon-file-text'></i> Transcripciones",
				},
				{
					"type": "doctype",
					"name": "Forma",
					"label": "<i class='octicon octicon-list-unordered'></i> Formas"
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
					"label": "<i class='octicon octicon-organization'></i> Transcriptores"
				}
			]
		}
		
	]
