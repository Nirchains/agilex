# -*- coding: utf-8 -*-
# Copyright (c) 2019, Pedro Antonio Fernández Gómez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.website.website_generator import WebsiteGenerator
from frappe.website.render import clear_cache
from frappe.utils import today, cint, global_date_format, get_fullname, strip_html_tags, markdown
from agilex.agilex.utils import obtener_codigo_transcripcion, obtener_html, obtener_texto_plano_desde_html, obtener_html_tp, actualiza_formas_pc

class Transcripcion(WebsiteGenerator):
	def validate(self):
		route = frappe.db.get_value("Tipo de Documento", self.tipo_de_documento, fieldname="route")
		codigo = obtener_codigo_transcripcion(self.expediente, self.name)
		self.route = "{0}/{1}".format(route, codigo)

		self.presentacion_critica_html = obtener_html(self.presentacion_critica)
		self.presentacion_critica_texto_plano = obtener_texto_plano_desde_html(self.presentacion_critica_html)

		self.transcripcion_paleografica_html = obtener_html_tp(self.transcripcion_paleografica)
		self.transcripcion_paleografica_texto_plano = obtener_texto_plano_desde_html(self.transcripcion_paleografica_html)
	
	def on_update(self):
		formas = actualiza_formas_pc(self.presentacion_critica_texto_plano, self.name)
	
	def autoname(self):
		self.name = obtener_codigo_transcripcion(self.expediente, self.name)

	def get_context(self, context):
		context.parents = [
			{"name": _("Home"), "route":"/"},
			{"name": "Corpus", "route": "/corpus/doc"},
			{"label": context.tipo_de_documento, "route":frappe.db.get_value("Tipo de Documento", context.tipo_de_documento, fieldname="route")}
		]


def get_list_context(context=None):

	list_context = frappe._dict(
		source = "templates/includes/transcripcion/transcripcion.html",
		get_list = get_transcripcion_list,
		children = get_children(),
		hide_filters = False,
		title = _('Transcripciones')
	)

	list_context.parents = [{"name": _("Home"), "route": "/"},
							{"name": _("Corpus"), "route": "/corpus/doc"}]

	return list_context

def get_transcripcion_list(doctype, txt=None, filters=None, limit_start=0, limit_page_length=20, order_by=None):
	conditions = []
	if filters:
		if filters.tipo_de_documento:
			conditions.append('t1.tipo_de_documento="%s"' % frappe.db.escape(filters.tipo_de_documento))
		
	if txt:
		conditions.append('(t1.name like "%{0}%" or t1.title like "%{0}%")'.format(frappe.db.escape(txt)))

	#if conditions:
	frappe.local.no_cache = 1

	query = """\
		select
			t1.route, t1.title, left(t1.title, 200) as title_res, t1.name, t1.tipo_de_documento, t1.anio,
			t1.signatura
		from `tabTranscripcion` t1
		where ifnull(t1.published,0)=1
		%(condition)s
		order by t1.name asc
		limit %(start)s, %(page_len)s""" % {
			"start": limit_start, "page_len": limit_page_length,
				"condition": (" and " + " and ".join(conditions)) if conditions else ""
		}

	#frappe.log_error(filters)

	transcripciones = frappe.db.sql(query, as_dict=1)

	return transcripciones

def get_children():
	query = """select route as name,
		tipo_de_documento_name as title from `tabTipo de Documento`
		where published = 1
		and exists (select name from `tabTranscripcion`
			where `tabTranscripcion`.tipo_de_documento=`tabTipo de Documento`.name and published=1)
		order by title asc"""
	
	return frappe.db.sql(query, as_dict=1)