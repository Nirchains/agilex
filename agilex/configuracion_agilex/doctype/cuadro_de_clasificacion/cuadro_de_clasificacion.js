// Copyright (c) 2019, Pedro Antonio Fernández Gómez and contributors
// For license information, please see license.txt

frappe.ui.form.on('CUADRO DE CLASIFICACION', {
	onload: function(frm) {
		//frm.list_route = "Tree/Item Group";

		//get query select item group
		frm.fields_dict['parent_cuadro_de_clasificacion'].get_query = function(doc,cdt,cdn) {
			return{
				filters:[
					['CUADRO DE CLASIFICACION', 'is_group', '=', 1],
					['CUADRO DE CLASIFICACION', 'name', '!=', doc.titulo]
				]
			}
		}
	},
});
