// Copyright (c) 2019, Pedro Antonio Fernández Gómez and contributors
// For license information, please see license.txt
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
		}
	},
	presentacion_critica: function(frm) {
		//var newString = frm.doc.presentacion_critica.replace(/({\d+})/g, cur_frm.cscript.transcripcion.replacer);
		//console.log("new: " + newString)
		//console.log(newString); // XXzzzz - XX , zzzz
	}
});


cur_frm.cscript.transcripcion = {
	replacer: function(str, p1, offset, s) {
		var n_linea = p1.replace(/[{}]/g,'');
		return str.replace(p1, "<span class='linea'>" + n_linea + "</span>");
	}
}
