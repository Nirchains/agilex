// Copyright (c) 2019, Pedro Antonio Fernández Gómez and contributors
// For license information, please see license.txt
frappe.provide("agilex.transcripcion");

cur_frm.add_fetch("expediente", "tipo_de_documento", "tipo_de_documento");
cur_frm.add_fetch("expediente", "signatura", "signatura");

frappe.ui.form.on('Transcripcion', {
	refresh: function(frm) {
		//$('textarea[data-fieldname="presentacion_critica"]').css({'height': '1500px'});
		//$('textarea').css({'height': '1500px'});
		
		//Deshabilitamos el corrector
		$('textarea').attr('spellcheck',false);
		
		autosize($('textarea'));

		if(!frm.doc.__islocal) {
			frm.add_custom_button(__("Ver formas"),
				function() {
					frappe.route_options = {
						"transcripcion": frm.doc.name
					};
					frappe.set_route("List", "Forma");
				}
			);	
		} else {
			agilex.transcripcion.import_transcriptores_por_defecto(frm, "transcriptores_por_defecto", "transcriptores")
		}
	},
	presentacion_critica: function(frm) {
		//var newString = frm.doc.presentacion_critica.replace(/({\d+})/g, cur_frm.cscript.transcripcion.replacer);
		//console.log("new: " + newString)
		//console.log(newString); // XXzzzz - XX , zzzz
	}
});


$.extend(agilex.transcripcion, {
	import_transcriptores_por_defecto: function(frm, origin_table, destin_table) {
		frappe.model.clear_table(frm.doc, destin_table);
			frappe.call({
				method: "agilex.agilex.utils.load_transcriptores_por_defecto",
				args: {
					"parentfield": origin_table
				},
				callback: function(r) {
					if(r.message) {
						console.log(r.message);
						$.each(r.message, function(i, item) {
							var d = frappe.model.add_child(frm.doc, "Transcriptores", destin_table);
							frappe.model.set_value(d.doctype, d.name, "transcriptor", item.transcriptor);
						});
					}
					refresh_field(destin_table);
				}
			});
	}
});
