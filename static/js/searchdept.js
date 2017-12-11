// AJAX call for autocomplete 
$(document).ready(function(){
	$("#department").keyup(function(){
		$.ajax({
		type: "POST",
		url: "search",
		data:'term='+$(this).val(),
		beforeSend: function(){
			$("#department").css("background","#FFF url(LoaderIcon.gif) no-repeat 165px");
		},
		success: function(data){
			console.log(data)
			$("#suggesstion-box-dept").show();
			$("#suggesstion-box-dept").html(data);
			$("#department").css("background","#FFF");
		}
		});
	});
});
//To select country name
function selectCountry(val) {
$("#department").val(val);
$("#suggesstion-box-dept").hide();
}