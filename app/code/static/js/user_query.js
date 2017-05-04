$(document).ready(function() {
    var attr;

    // Get the statistics from anonymization backend service
    var stats;
    $.ajax({
            url: '/getkanonresult',
            type: 'GET',
            success: function(data) {
                // Print the statistics into a table
                var lines = data.split( "\n" );
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
    
    // Method that processes the query and prints the results
    function submitUserQuery(evt) {
    	$.ajax({
            url: '/userQuery',
            type: 'POST',
            data: {
                'query': $('#userQuery').val()
            },
            success: function(data) {
                var json = JSON.parse(data);
                if ("db1" in json) {
                    // Print data into db1 table
                    var html = '<tbody>\r\n';
                    var org = json.db1;
                    if(Array.isArray(org)) {
                        for(var row in org) {                        
                            html += '<tr>\r\n';
                            for(var item in org[row]) {
                                html += '<td>' + org[row][item] + '</td>\r\n';
                            }
                            html += '</tr>\r\n' ;
                        }
                        html += '</tbody>'
                        $('#result1').html(html);
                    } else {
                        var html = '<div class="alert alert-danger"><strong>Error! </strong>' + org + '</div>';
                        $('#error-box-query').html(html);  
                    }
                }
                if ("db2" in json && json.db2.length > 1) {
                    // Print data into db2 table
                    var html = '<tbody>\r\n';
                    var org = json.db2;

                    if(Array.isArray(org)) {
                        for(var row in org) {                        
                            html += '<tr>\r\n';
                            for(var item in org[row]) {
                                html += '<td>' + org[row][item] + '</td>\r\n';
                            }
                            html += '</tr>\r\n' ;
                        }
                        html += '</tbody>'
                        $('#result2').html(html);
                    } else {
                        var html = '<div class="alert alert-danger"><strong>Error! </strong>' + org + '</div>';
                        $('#error-box-query').html(html);  
                    }
                }
            },
            error: function(error) {
                console.log(error);
                var html = '<div class="alert alert-danger"><strong>Error!</strong> There was an error performing the query.' + error + '</div>';
                $('#error-box-query').html(html);  
            }
        });
    }
});