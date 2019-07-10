# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from agilex.agilex.utils import can_edit

def get_context(context):
	#context.doc = frappe.get_doc("About Us Settings", "About Us Settings")

	context.expedientes = {}
	context.title = "Organigrama"

	context.parents = [{"name": _("Home"), "route": "/"},
						{"name": _("Corpus"), "route": "/corpus/organigrama"}
					  ]

	context.can_edit = can_edit()

	context.tipos_de_documento = frappe.get_list("Tipo de Documento", 
		fields=["name", "codigo","route"], 
		filters = {"published":1},
		order_by = "codigo",
		ignore_permissions=True)

	for tdoc in context.tipos_de_documento:
		context.expedientes[tdoc.codigo] = frappe.get_list("Expediente", 
			fields=["name", "signatura"], 
			order_by = "CAST(name as unsigned)",
			filters = {"tipo_de_documento": tdoc.name},
			ignore_permissions=True)

		for expediente in context.expedientes[tdoc.codigo]:
			expediente.descripcion = frappe.get_list("Expediente Descripcion",
				fields=["descripcion"],
				order_by = "idx",
				filters = {"parentfield": "descripcion_tabla", "parenttype": "Expediente", "parent": expediente.name},
				ignore_permissions=True)

			#expediente.documentos = frappe.get_list("Transcripcion",
			#	fields = ["name", "title", "signatura", "anio", "route"],
			#	order_by = "name",
			#	filters = {"expediente": expediente.name})

			query = """\
				select
					t1.route, t1.title, left(t1.title, 200) as title_res, t1.name, t1.anio,
					t1.signatura
				from `tabTranscripcion` t1
				where ifnull(t1.published,0)=1
				and t1.expediente = '%(expediente)s'
				order by CAST(t1.name as unsigned) asc
				""" % {
					"expediente": expediente.name
				}

			#frappe.log_error(query)

			expediente.documentos = frappe.db.sql(query, as_dict=1)

	return context
