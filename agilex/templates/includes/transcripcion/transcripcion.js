// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

frappe.ready(function() {

	$("select[name='tdoc'").change(function() {
		/*
		search = cms.utils.getUrlParameter("txt");
		if (search) {
			$(location).attr("href", "/" + this.value + "?txt=" + search);
		} else {
			if (!this.value) {
				$(location).attr("href", "/corpus/doc");
			} else {
				$(location).attr("href", "/" + this.value );
			}
		}*/
	});

	cms.utils.infiniteScroll();
	

});

var msgprint = function(txt) {
	if(txt) $("#contact-alert").html(txt).toggle(true);
}
