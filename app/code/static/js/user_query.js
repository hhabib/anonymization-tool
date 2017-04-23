$(document).ready(function() {

    // The event listener for the user query
    document.getElementById('btnUserQuery').addEventListener('click', submitUserQuery, false);
    // Method that reads and processes the selected file
    function submitUserQuery(evt) {

        console.log($('#userQuery').val());
        // var query = evt.target.$('#userQuery').val();
        // var form = new FormData();
        // form.append('query', query);

    	$.ajax({
            url: '/userQuery',
            type: 'POST',
                // data: $('form').serialize(),
            data: {
                'query': $('#userQuery').val()
            },
            success: function(data) {
                console.log(data);
                document.getElementById('queryResult').innerHTML = data
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
});