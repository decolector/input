$(document).ready(function(){
	$.couch.urlPrefix = "https://decolector.iriscouch.com/";

	$.couch.info({
		success:function(data){
			console.log("couch info: " + JSON.stringify(data));
		}
	});

	var db = $.couch.db("messages");

	$("#send").click(function(e){
		e.preventDefault();
		var forma = $("#forma")
		var data = formToJSON(forma);
		console.log(JSON.stringify(data));
		db.saveDoc(data, {success: function(data, status, xhr){
			console.log("doc saved: " + JSON.stringify(data));
		}});
	});

	function formToJSON(form){
    	var array = form.serializeArray();
    	var json = {};
    
    	jQuery.each(array, function() {
        	json[this.name] = this.value || '';
    	});
    
    return json;
	}
});	