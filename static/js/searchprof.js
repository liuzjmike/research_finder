$(document).ready(function() {
    $.ajax({
        url: '{{ url_for("search_prof") }}'
    }).done(function (data) {
        $('#professor').autocomplete({
            source: data,
            minLength: 2
        });
    });
}