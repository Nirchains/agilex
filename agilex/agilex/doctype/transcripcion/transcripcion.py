# -*- coding: utf-8 -*-
# Copyright (c) 2019, Pedro Antonio Fernández Gómez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator
from agilex.agilex.utils import obtener_codigo_transcripcion
from cms.cms.doctype.web_module.web_module import load_module_positions


class Transcripcion(WebsiteGenerator):
	def validate(self):
		route = frappe.db.get_value("Tipo de Documento", self.tipo_de_documento, fieldname="route")
		codigo = obtener_codigo_transcripcion(self.expediente)
		self.route = "{0}/{1}".format(route, codigo)
		self.title = codigo

	def autoname(self):
		self.name = obtener_codigo_transcripcion(self.expediente)

	def get_context(self, context):
		context.title = self.name

		#PFG
		context.modules = []
		context.module_positions, context.layout_positions = load_module_positions(context.modules)