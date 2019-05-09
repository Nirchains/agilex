// Copyright (c) 2019, Pedro Antonio Fernández Gómez and contributors
// For license information, please see license.txt

frappe.ui.form.on('Desplegable', {
	refresh: function (frm) {
		if(!frm.doc.__islocal) {
			frm.add_custom_button(__("Ver opciones"),
				function() {
					frappe.route_options = {
						"desplegable": frm.doc.name
					};
					frappe.set_route("List", "Desplegable Opciones");
				}
			);	
		}
	}
});
