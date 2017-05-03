$(document).ready(function() {
    // Get the statistics from anonymization backend service
    var stats;

    $.ajax({
            url: '/getkanonresult',
            type: 'GET',
            success: function(data) {
                // Print the statistics into a table
                console.log(data);
                var lines = data.split( "\n" );
                console.log(lines.length);
                if (lines.length == 1) {
                    var html = '<div class="alert alert-danger"><strong>Error! </strong>' + data + '</div>';
                     $('#error-box').html(html);
                } else {
                    lines.splice(2,0,"");
                    var html = '<tbody><tr><td><b>General Statistics</b></td><td></td></tr>';
                    for(var i = 0; i < lines.length-1; i++) {
                        var newLine = lines[i].replace("=", ":");
                        newLine = newLine.replace("*", "-");
                        newLine = newLine.replace("- Statistics","");
                        newLine = newLine.replace("- Optimal generalization","Optimal Generalization");
                        newLine = newLine. replace("EquivalenceClassStatistics {", "Equivalence Class Statistics");
                        var printLine = newLine.split(":");
                        html += '<tr>\r\n';
                        if(printLine.length > 1) {
                            for(var cell in printLine) {
                                html += '<td>' + printLine[cell] + '</td>';
                            }
                        } else {
                            html += '<td><b>' + printLine[0] + '</b></td><td></td>';
                        }

                        html += '</tr>\r\n' ;
                    }
                    html += '</tbody>'
                    $('#statistic').html(html);
                }
            },
            error: function(error) {
                console.log(error);
                var html = '<div class="alert alert-danger"><strong>Error!</strong> There was an error performing the anonymization.' + error + '</div>'
                $('#error-box').html(html);    
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