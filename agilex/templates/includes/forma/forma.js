// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

frappe.ready(function() {


	$("select[name='ordenar_por'").change(function() {
		document.location.search = cms.utils.insertURLParam("ordenar_por", this.value);
	});

	cms.utils.infiniteScroll();


});

var msgprint = function(txt) {
	if(txt) $("#contact-alert").html(txt).toggle(true);
}
