$(document).ready(function() {
    $.ajax({
        url: '{{ url_for("search_dept") }}'
    }).done(function (data) {
        $('#department').autocomplete({
            source: data,
            minLength: 2
        });
    });
}