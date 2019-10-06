# -*- coding: utf-8 -*-
# Copyright (c) 2019, Pedro Antonio Fernández Gómez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import re
from frappe import _
from frappe.website.website_generator import WebsiteGenerator
from frappe.website.render import clear_cache
from frappe.utils import today, cint, global_date_format, get_fullname, strip_html_tags, markdown
from frappe.model.naming import make_autoname

class Forma(WebsiteGenerator):
	def validate(self):
		route = "corpus/forma"
		codigo = self.scrub(self.name)
		self.route = "{0}/{1}".format(route, codigo)

	def autoname(self):
		patron_caracteres = re.compile(r'[\.\,\:\;\(\)\[\]\&\-\_\+\=\<\>]')
		texto = patron_caracteres.sub('',self.forma)
		self.name = "{0}-{1}-{2}".format(self.transcripcion, texto,make_autoname('hash', "Forma")).lower()


	def get_context(self, context):
		context.parents = [
			{"name": _("Home"), "route":"/"},
			{"name": "Corpus", "route": "/corpus/forma"},
			{"label": context.tipo_de_documento, "route":frappe.db.get_value("Tipo de Documento", context.tipo_de_documento, fieldname="route")}
		]

def get_list_context(context=None):
	list_context = frappe._dict(
		source = "templates/includes/forma/forma.html",
		get_list = get_forma_list,
		#children = get_children(),
		hide_filters = False,
		title = _('Formas')
	)

	list_context.parents = [{"name": _("Home"), "route": "/"},
							{"name": _("Corpus"), "route": "/corpus/forma"}]

	return list_context

def get_forma_list(doctype, txt=None, filters=None, limit_start=0, limit_page_length=20, order_by=None):
	conditions = []
	if filters:
		if filters.tipo_de_documento:
			conditions.append('t1.tipo_de_documento="%s"' % frappe.db.escape(filters.tipo_de_documento))
		
	if txt:
		conditions.append('(t1.name like "%{0}%" or t1.forma like "%{0}%")'.format(frappe.db.escape(txt)))

	#if conditions:
	frappe.local.no_cache = 1

	query = """\
		select
			t1.route, t1.name, t1.forma, t1.forma_reversa, t1.transcripcion, t1.tipo_de_transcripcion,
			t1.frecuencia_absoluta, t1.frecuencia_relativa, tt.route as route_transcripcion
		from `tabForma` t1
		inner join `tabTranscripcion` tt on t1.transcripcion = tt.name
		where ifnull(t1.published,0)=1
		%(condition)s
		order by CONVERT (t1.forma USING latin2),t1.tipo_de_transcripcion asc
		limit %(start)s, %(page_len)s""" % {
			"start": limit_start, "page_len": limit_page_length,
				"condition": (" and " + " and ".join(conditions)) if conditions else ""
		}

	#frappe.log_error(query)

	formas = frappe.db.sql(query, as_dict=1)

	return formas

def get_children():
	query = """select route as name,
		tipo_de_documento_name as title from `tabTipo de Documento`
		where published = 1
		and exists (select name from `tabTranscripcion`
			where `tabTranscripcion`.tipo_de_documento=`tabTipo de Documento`.name and published=1)
		order by title asc"""
	
	return frappe.db.sql(query, as_dict=1)