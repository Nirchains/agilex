// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

frappe.ready(function() {

	$(window).scroll(function() {
     	var isElementInView = cms.utils.isElementInView($(".btn-more"), false);

		if (isElementInView) {
			$('#portfolioLoadMoreLoader').addClass('portfolio-load-more-loader-showing').show();

		    $(".btn-more").click();

		    $('#portfolioLoadMoreLoader').removeClass('portfolio-load-more-loader-showing').hide();
		} 
	});




	

});

var msgprint = function(txt) {
	if(txt) $("#contact-alert").html(txt).toggle(true);
}
