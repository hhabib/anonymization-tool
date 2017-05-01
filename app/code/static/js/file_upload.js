$(document).ready(function() {

    // The event listener for the file upload
    document.getElementById('csvFileUpload').addEventListener('change', upload, false);

    // Method that checks that the browser supports the HTML5 File API
    function browserSupportFileUpload() {
        var isCompatible = false;
        if (window.File && window.FileReader && window.FileList && window.Blob) {
            isCompatible = true;
        }
        return isCompatible;
    }

    // Method that reads and processes the selected file
    function upload(evt) {
        if (!browserSupportFileUpload()) {
            alert('The File APIs are not fully supported in this browser!');
        } else {
                var data = null;
                var file = evt.target.files[0];

                // Ajax Post the file to the backend
                var formData = new FormData();
                formData.append('file', file);
                $.ajax({
                       url : '/postcsv',
                       type : 'POST',
                       data : formData,
                       processData: false,  // tell jQuery not to process the data
                       contentType: false,  // tell jQuery not to set contentType
                       success : function(data) {
                           console.log(data);
                       }
                });

                var attributes = null;
                var reader = new FileReader();
                reader.readAsText(file);
                reader.onload = function(event) {
                    var csvData = event.target.result;
                    data = $.csv.toArrays(csvData);
                    attributes = data[0];
                    
                    // Store attributes in backend.
                    $.getJSON($SCRIPT_ROOT + '/_array2python', {
                        attributes: JSON.stringify(attributes)
                    }, function(data){
                        console.log(data.result)
                    });

                    // Print Data
                    var html = '<thead>\r\n<tr>';
                    for(var cell in data[0]) {
                        html += '<th>' + data[0][cell] + '</th>\r\n'
                    }
                    html += '</tr>\r\n</thead>\r\n<tbody>'
                    
                    for(var row in data) {
                        if(row > 0 && row < 5) {
                            html += '<tr>\r\n';
                            for(var item in data[row]) {
                                html += '<td>' + data[row][item] + '</td>\r\n';
                            }
                            html += '</tr>\r\n' ;
                        }
                    }
                    html += '</tbody>'

                    $('#contents').html(html);

                    // Add previous & next buttons
                    $('#navigation').html('<ul class=\"pager\"><li><a href=\"./\">Back</a></li><li><a href=\"./anonymize.html\">Next</a></li></ul>');
                };
                reader.onerror = function() {
                    console.log('Unable to read ' + file.fileName);
                };
            }
    }
}); 