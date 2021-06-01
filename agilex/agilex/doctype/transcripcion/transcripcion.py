# -*- coding: utf-8 -*-
# Copyright (c) 2019, Pedro Antonio Fernández Gómez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.website.website_generator import WebsiteGenerator
from frappe.website.render import clear_cache
from frappe.utils import today, cint, global_date_format, get_fullname, strip_html_tags, markdown
from agilex.agilex.utils import obtener_codigo_transcripcion, obtener_html, obtener_texto_plano_desde_html, obtener_html_tp, actualiza_formas
from six.moves.urllib.parse import quote, urlencode, urlparse
import requests
from frappe.utils import get_url

class Transcripcion(WebsiteGenerator):
	
	renombrando = False

	def validate(self):
		route = frappe.db.get_value("Tipo de Documento", self.tipo_de_documento, fieldname="route")
		codigo = obtener_codigo_transcripcion(self.expediente, self.name)
		self.route = "{0}/{1}".format(route, codigo)

		self.presentacion_critica_html = obtener_html(self.presentacion_critica)
		self.presentacion_critica_texto_plano = obtener_texto_plano_desde_html(self.presentacion_critica_html)

		self.transcripcion_paleografica_html = obtener_html_tp(self.transcripcion_paleografica)
		self.transcripcion_paleografica_texto_plano = obtener_texto_plano_desde_html(self.transcripcion_paleografica_html)
	
	def on_update(self):
		if self.autogenerar_formas:
			#frappe.msgprint("Actualizando formas, por favor, espere a que el proceso se complete ...")
			route = frappe.db.get_value("Tipo de Documento", self.tipo_de_documento, fieldname="route")
			self.route = "{0}/{1}".format(route, self.name)
			#self.save()
			actualiza_formas(self.transcripcion_paleografica_texto_plano, "Transcripción paleográfica", self.name, Transcripcion.renombrando)
			actualiza_formas(self.presentacion_critica_texto_plano, "Presentación crítica", self.name, Transcripcion.renombrando)
			#frappe.msgprint("... se han actualizado las formas")

	def on_submit(self):
		frappe.clear_document_cache("Expediente", self.expediente)
	
	def autoname(self):
		self.name = obtener_codigo_transcripcion(self.expediente, self.name)

	def after_rename(self, old, new, merge=False):
		Transcripcion.renombrando = True
		route = frappe.db.get_value("Tipo de Documento", self.tipo_de_documento, fieldname="route")
		self.route = "{0}/{1}".format(route, new)
		self.save()
		#frappe.clear_cache()

	def get_context(self, context):
		context.parents = [
			{"name": _("Home"), "route":"/"},
			{"name": "Corpus", "route": "/corpus/doc"},
			{"name": context.tipo_de_documento, "route":frappe.db.get_value("Tipo de Documento", context.tipo_de_documento, fieldname="route")}
		]


def get_list_context(context=None):
	title = _('Transcripciones')

	parametros = frappe.local.form_dict.copy()
	tdoc = parametros.tdoc or ""
	tipo_de_documento = parametros.tipo_de_documento or ""
	txt = parametros.txt or ""

	parametros.pop("doctype", None)
	parametros.pop("tdoc", None)

	#frappe.log_error("{0}".format(params))

	filtros = urlencode(parametros)

	if tdoc:
		frappe.flags.redirect_location = "/{0}?{1}".format(tdoc, filtros)
		raise frappe.Redirect

	if tipo_de_documento:
		tdoc = frappe.get_list("Tipo de Documento", 
								filters={'route': 'corpus/doc/{0}'.format(tipo_de_documento)},
								fields="tipo_de_documento_name",
								ignore_permissions=True)
		if tdoc and len(tdoc)==1:
			tipo_de_documento = tdoc[0].tipo_de_documento_name
			title = "Transcripciones de <b>{0}</b>".format(tipo_de_documento)
	

	list_context = frappe._dict(
		source = "templates/includes/transcripcion/transcripcion.html",
		get_list = get_transcripcion_list,
		children = get_children(),
		hide_filters = False,
		title = title
	)

	list_context.parents = [{"name": _("Home"), "route": "/"},
							{"name": _("Corpus"), "route": "/corpus/doc"}
							]

	list_context.tipos_de_documento = frappe.get_list("Tipo de Documento", 
		fields=["name", "codigo","route"], 
		filters = {"published":1}, 
		ignore_permissions=True)

	list_context.tipo_de_documento = tipo_de_documento
	list_context.siglo = frappe.local.form_dict.siglo or ""
	list_context.siglos = frappe.db.sql(""" Select siglo from `tabSiglo` 
		where published = 1
		order by ordinal asc """, as_dict=1)
	list_context.anio_inicio = frappe.local.form_dict.anio_inicio or ""
	list_context.anio_fin = frappe.local.form_dict.anio_fin or ""
	list_context.tipo_de_documento_url = frappe.local.form_dict.tipo_de_documento
	
	return list_context

def get_transcripcion_list(doctype, txt=None, tdoc=None, filters=None, limit_start=0, limit_page_length=20, order_by=None):
	conditions = []
	if filters:
		if filters.tipo_de_documento:
			tdoc = frappe.get_list("Tipo de Documento", 
								filters={'route': 'corpus/doc/{0}'.format(filters.tipo_de_documento)},
								fields="name",
								ignore_permissions=True)
			if tdoc and len(tdoc)==1:
				conditions.append('te.tipo_de_documento=%s' % frappe.db.escape(tdoc[0].name))

	parametros = frappe.local.form_dict
	if parametros:
		if parametros.siglo:
			conditions.append('t1.siglo=%s' % frappe.db.escape(parametros.siglo))
		if parametros.anio_inicio:
			conditions.append('t1.anio >= %s' % frappe.db.escape(parametros.anio_inicio))
		if parametros.anio_fin:
			conditions.append('if(t1.anio_fin=0, t1.anio, t1.anio_fin) <= %s' % frappe.db.escape(parametros.anio_fin))
		
	if txt:
		conditions.append('(t1.name like {0} or t1.title like {0} or t1.signatura like {0})'.format(frappe.db.escape("%" + txt + "%")))

	#if conditions:
	frappe.local.no_cache = 1

	query = """\
		select
			t1.route, t1.title, left(t1.title, 200) as title_res, t1.name, t1.tipo_de_documento, td.route as ruta_tipo_de_documento, t1.anio,
			t1.signatura
		from `tabTranscripcion` t1
		inner join `tabExpediente` te on t1.expediente=te.name
		inner join `tabTipo de Documento` td on te.tipo_de_documento=td.name
		where ifnull(t1.published,0)=1
		%(condition)s
		order by t1.name asc 
		limit %(start)s, %(page_len)s""" % {
			"start": limit_start, "page_len": limit_page_length,
				"condition": (" and " + " and ".join(conditions)) if conditions else ""
		}

	#order by CAST(t1.name as unsigned) asc 

	#frappe.log_error(query)

	transcripciones = frappe.db.sql(query, as_dict=1, debug=True)

	return transcripciones

def get_children():
	query = """select route as name,
		tipo_de_documento_name as title from `tabTipo de Documento`
		where published = 1
		and exists (select name from `tabTranscripcion`
			where `tabTranscripcion`.tipo_de_documento=`tabTipo de Documento`.name and published=1)
		order by title asc"""
	
	return frappe.db.sql(query, as_dict=1)