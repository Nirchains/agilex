# -*- coding: utf-8 -*-
# Copyright (c) 2019, Pedro Antonio Fernández Gómez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from agilex.agilex.utils import obtener_codigo_expediente

class Expediente(Document):
	def on_update(self):
		pass
		#if self.name != self.expediente_name and not self.is_new():
		#	frappe.rename_doc(self.doctype, self.name, self.expediente_name)

	def autoname(self):
		self.name = obtener_codigo_expediente(self.tipo_de_documento, self.name)
