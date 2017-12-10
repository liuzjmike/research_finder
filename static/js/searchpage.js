<script type="text/javascript">
    $(function() {
        $( "#function_name" ).autocomplete({
            source: '{{url_for("autocomplete")}}',
            minLength: 2,
        });
    });
</script>

<form id="function_search_form" method="post" action="">
    {{form.function_name}}
</form>