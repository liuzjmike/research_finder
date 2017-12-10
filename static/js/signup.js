$("#role input[type=radio]").click(function (e) {
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
});