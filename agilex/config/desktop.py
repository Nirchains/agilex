# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "AGILEX",
			"color": "#30c57a",
			"icon": "octicon octicon-book",
			"type": "module",
			"label": _("AGILEX")
		},
		{
			"module_name": "Configuracion Agilex",
			"color": "grey",
			"icon": "octicon octicon-gear",
			"type": "module",
			"label": _("Configuracion Agilex")
		}
	]
