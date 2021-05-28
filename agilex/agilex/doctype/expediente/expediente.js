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

			frm.add_custom_button(__("Actualiza todas las transcripciones (m&eacute;todo masivo)"),
				function() {
					frappe.confirm("Esta operación puede tardar unos minutos, dependiendo del número de transcripciones del expediente y de la longitud de cada una. Puede seguir trabajando en la aplicación, recibirá un aviso en pantalla al terminar. ¿Está seguro de que desea continuar?",
						function () {
							frappe.call({
								method: "agilex.agilex.utils.actualiza_todas_las_transcripciones",
								args: {
									"expediente": frm.doc.name
								},
								callback: function(r) {
									if(!r.message) {
										frappe.throw(__("Este expediente no tiene ninguna transcripción"));
									} else {
										frappe.msgprint("Operación completada. Se han actualizado las siguientes transcripciones:<br>" + r.message);
									}
								}
							});
						},
						function () {

						}
					);
					
				}
			);	
		}
	},
	after_save: function(frm) {
		agilex.utils.rename_doc(frm.doc.doctype,frm.doc.name,frm.doc.expediente_name)
	},
	tipo_de_documento: function(frm) {
		var name;
		if(frm.doc.__islocal) {
			name = "";
		} else {
			name = frm.doc.name;
		}

		if (!helper.IsNullOrEmpty(frm.doc.tipo_de_documento)) {
			frappe.call({
				method: "agilex.agilex.utils.obtener_codigo_expediente",
				args: {
					"tipo_de_documento": frm.doc.tipo_de_documento,
					"name": name
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
	}
	
});
