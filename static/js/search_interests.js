// AJAX call for autocomplete 
$(document).ready(function(){
	$("#interests").keyup(function(){
		$.ajax({
		type: "POST",
		url: "search",
		data:'term='+$(this).val(),
		beforeSend: function(){
			$("#").css("background","#FFF url(LoaderIcon.gif) no-repeat 165px");
		},
		success: function(data){
			console.log(data)
			$("#suggesstion-box-interests").show();
			$("#suggesstion-box-interests").html(data);
			$("#interests").css("background","#FFF");
		}
		});
	});
});
//To select country name
function selectCountry(val) {
$("#interests").val(val);
$("#suggesstion-box-interests").hide();
}