# -*- coding: utf-8 -*-
# Copyright (c) 2019, Pedro Antonio Fernández Gómez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator

class Forma(WebsiteGenerator):
	def validate(self):
		route = "corpus/forma"
		codigo = self.scrub(self.name)
		self.route = "{0}/{1}".format(route, codigo)

	def autoname(self):
		self.name = "{0}-{1}".format(self.transcripcion, self.forma)

