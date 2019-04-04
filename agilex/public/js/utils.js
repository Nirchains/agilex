frappe.provide("agilex.utils");

$.extend(agilex.utils, {
	rename_doc: function(doctype, docname, newname, callback) {
		if (docname != newname) {
			return frappe.call({
				method:"frappe.model.rename_doc.rename_doc",
				args: {
					doctype: doctype,
					old: docname,
					"new": newname,
					"merge": false
				},
				callback: function(r,rt) {
					if(!r.exc) {
						$(document).trigger('rename', [doctype, docname,
							r.message || args.newname]);
						if(locals[doctype] && locals[doctype][docname])
							delete locals[doctype][docname];
						if(callback)
							callback(r.message);
					}
				}
			});
		}
	},

});
