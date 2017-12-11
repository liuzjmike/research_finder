function show_role_specific_content() {
    let val = $("#role input[type=radio]:checked").val();
    if (val == "faculty") {
        $(".student").hide();
        $(".faculty").fadeIn(600);
    } else if (val == "student") {
        $(".faculty").hide();
        $(".student").fadeIn(600);
    } else {
        $(".faculty").hide();
        $(".student").hide();
    }
}

$(show_role_specific_content);
$("#role input[type=radio]").click(function(e) {
    show_role_specific_content()
});