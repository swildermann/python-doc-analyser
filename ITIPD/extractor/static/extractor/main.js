$(function() {
    $("#typemenu").hide();
    $("#typemenu").menu();
    $("#typemenu").draggable();
    rangy.init();
    $("#typemenu li").mousedown(classify_selection);

    $('#thebutton').click(function () {
        var data = JSON.stringify(data_to_send);
        $.ajax({
            url: '/extractor/vote/',
            type: 'post',
            data: {
                data:data,
                unit: 10
            },
            success: function () {
                console.log('Success');
                console.log(arguments);
            },
            error: function () {
                console.log('Error!');
                console.log(arguments);
            }
        });
    });

    $('body').mouseup(function(e) {
        var sel = rangy.getSelection();
        if(!isBlank(sel))
        {
            if($("#typemenu").is(':visible')) return;
            show_typemenu(e.pageX+15, e.pageY+5);
        } else {
            $("#typemenu").hide();
        }
    });
});

function isEmpty(str) {
    return (!str || 0 === str.length);
}

function isBlank(str) {
    return (!str || /^\s*$/.test(str));
}

function show_typemenu(x, y) {
    $("#typemenu").css("top", y);
    $("#typemenu").css("left", x);
    $("#typemenu").show();
}

var data_to_send = [];

function classify_selection() {
   var sel = rangy.getSelection();
   var selected_text = sel.toString();
   var selected_html = sel.toHtml();
   var type_id = $(this).attr("id");
   var newentry = "<li thetype='" + type_id + "'>" +
                  "<div class='text'>" + selected_text + "</div>" +
//                          "<div class='html'>" + selected_html + "</div>" +
                  "<div> <b> Typ:" + type_id  + "</b> </div>"+
                  "</li>";
   $("#result").append(newentry);
    data_to_send.push({
        type_id: type_id,
        selected_text: selected_text
    });
};