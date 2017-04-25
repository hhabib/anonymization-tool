$(document).ready(function() {

    $.ajax({
            url: '/getkanonresult',
            type: 'GET',

            success: function(data) {
                console.log(data);
                document.getElementById('statistic').innerHTML = data
            },
            error: function(error) {
                console.log(error);
            }
        });



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
                var json = JSON.parse(data)
                if ("db1" in json) {
                    document.getElementById('result1').innerHTML = json.db1;
                }
                if ("db2" in json) {
                    document.getElementById('result2').innerHTML = json.db2;
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
});