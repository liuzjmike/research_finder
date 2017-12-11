// AJAX call for autocomplete 
$(document).ready(function(){
	$("#professor").keyup(function(){
		$.ajax({
		type: "POST",
		url: "search",
		data:'term='+$(this).val(),
		beforeSend: function(){
			$("#professor").css("background","#FFF url(LoaderIcon.gif) no-repeat 165px");
		},
		success: function(data){
			console.log(data)
			$("#suggesstion-box-prof").show();
			$("#suggesstion-box-prof").html(data);
			$("#professor").css("background","#FFF");
		}
		});
	});
});
//To select country name
function selectCountry(val) {
$("#professor").val(val);
$("#suggesstion-box-prof").hide();
}