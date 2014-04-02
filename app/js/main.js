$(document).ready(function(){
	$.couch.urlPrefix = "https://decolector.iriscouch.com";

	$.couch.info({
		success:function(data){
			console.log("couch info: " + JSON.stringify(data));
		}
	});

	var db = $.couch.db("messages");

	$("#send").click(function(e){
		e.preventDefault();
		var data = $("#forma").serializeArray()[0];
		console.log(JSON.stringify(data));
		db.saveDoc(data, {success: function(data, status, xhr){
			console.log("doc saved: " + JSON.stringify(data));
		}});
	});
	
});	