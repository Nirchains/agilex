// Copyright (c) 2019, Pedro Antonio Fernández Gómez and contributors
// For license information, please see license.txt
frappe.ui.form.on('Expediente', {
	refresh: function (frm) {
		if(!frm.doc.__islocal) {
			frm.add_custom_button(__("Ver documentos y transcripciones"),
				function() {
					frappe.route_options = {
						"Transcripcion": frm.doc.name
					};
					frappe.set_route("List", "Transcripcion");
				}
			);	
		}
	},
	after_save: function(frm) {
		agilex.utils.rename_doc(frm.doc.doctype,frm.doc.name,frm.doc.expediente_name)
	},
	tipo_de_documento: function(frm) {
		frappe.call({
			method: "agilex.agilex.utils.obtener_codigo_expediente",
			args: {
				"tipo_de_documento": frm.doc.tipo_de_documento,
				"name": frm.doc.name
			},
			callback: function(r) {
				if(!r.message) {
					//frappe.throw(__("No se encuentra la lista de combinaciones que forman el producto"))
				} else {
					frm.set_value('expediente_name',r.message);
				}
			}
		});
	}
});
