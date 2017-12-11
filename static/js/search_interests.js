$(document).ready(function() {
    $.ajax({
        url: '{{ url_for("search_interests") }}'
    }).done(function (data) {
        $('#interests').autocomplete({
            source: data,
            minLength: 2
        });
    });
}