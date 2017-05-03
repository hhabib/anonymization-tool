var attributes = [];

$(document).ready(function() {

    //Retrieve stored attributes from backend.
    $.getJSON($SCRIPT_ROOT + '/_python2array', function(data){
        attributes = data.result;

        // Print attributes
        var html = '<form><tbody>';
  
        for(var attr in attributes) {
            html += '<tr>\r\n';
            html += '<td>' + attributes[attr] + '</td>\r\n<td><select class=\"form-control\" id=\"' + attributes[attr] + '\" style=\"width: 300px\">\r\n<option value=\"insensitive\">Sensitive</option><option value=\"suppression\">Quasi-identifier (suppression)</option>\r\n\r\n<option value=\"numericgeneralization\">Quasi-Identifier (numeric-generalization)</option>\r\n</select></td>\r\n';
            html += '</tr>\r\n<br>';
        }
        html += '</tbody></form>';
    
        $('#attrList').html(html);

     });

    // Enable Bootstrap tooltips
    $('[data-toggle="tooltip"]').tooltip(); 
    
});

// Pass user input to backend
function submit() { 
    var attrCategorization = {};
    var identifyingAttr = [];
    var sensitiveAttr = [];
    var insensitiveAttr = [];
    var numericgeneralization = [];
    var suppression = [];
    var klevel = document.getElementById("klevel").value;
    for (var attr in attributes) {
        var selection = document.getElementById(attributes[attr]).value;
        
        if (selection == 'identifying') {
            identifyingAttr.push(attributes[attr]);
        } 

        if (selection == 'sensitive') {
            sensitiveAttr.push(attributes[attr]);
        }

        if (selection == 'insensitive') {
            insensitiveAttr.push(attributes[attr]);
        }

        if (selection == 'numericgeneralization') {
            numericgeneralization.push(attributes[attr]);
        }

        if (selection == 'suppression') {
            suppression.push(attributes[attr]);
        }
    }

    attrCategorization["identifying"] = identifyingAttr;
    attrCategorization["sensitive"] = sensitiveAttr;
    attrCategorization["insensitive"] = insensitiveAttr;
    attrCategorization["numericgeneralization"] = numericgeneralization;
    attrCategorization["suppression"] = suppression;
    attrCategorization["k"] = klevel;

    $.getJSON($SCRIPT_ROOT + '/_categorization2python', {
        attrCategorization: JSON.stringify(attrCategorization)
    }, function(data){
        console.log(data.result)
    });

    window.location = "./results.html";
}
