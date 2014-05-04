$(function() {
    $("#typemenu").hide();
    $("#typemenu").menu();
    $("#typemenu").draggable();

    rangy.init();
    cssAppliermarkedtext = rangy.createCssClassApplier("markedtext", {normalize: true});
    cssApplierfunctionalityandbehavior = rangy.createCssClassApplier("functionalityandbehavior", {normalize: true});
    cssApplierconcepts = rangy.createCssClassApplier("concepts", {normalize: true});
    cssApplierdirectives = rangy.createCssClassApplier("directives", {normalize: true});
    cssApplierpurposes = rangy.createCssClassApplier("purposes", {normalize: true});
    cssApplierqualityattributes = rangy.createCssClassApplier("qualityattributes", {normalize: true});
    cssAppliercontrolflow = rangy.createCssClassApplier("controlflow", {normalize: true});
    cssApplierstructure = rangy.createCssClassApplier("structure", {normalize: true});
    cssApplierpatterns = rangy.createCssClassApplier("patterns", {normalize: true});
    cssAppliercodeexamples = rangy.createCssClassApplier("codeexamples", {normalize: true});
    cssApplierenvironment = rangy.createCssClassApplier("environment", {normalize: true});
    cssApplierexternal = rangy.createCssClassApplier("external", {normalize: true});
    cssAppliernoninformation = rangy.createCssClassApplier("noninformation", {normalize: true});


    $("#typemenu li").click(color_selection);

    $('#thebutton').click(function () {

    /*
        var data = JSON.stringify(data_to_send);
        $.ajax({
            url: '/extractor/vote/',
            type: 'post',
            data: {
                data: data,
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
        */
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

function color_selection() {
    //dirty js function name hack
    var s = $(this).attr("class");
    var appliername = s.substring(0, s.indexOf(' '));
    var functioname = 'cssApplier' + appliername;
    var fn = window[functioname];
    fn.applyToSelection();
    cssAppliermarkedtext.applyToSelection();

    $("#typemenu").hide();

    rangy.getSelection().removeAllRanges();

 /*  var sel = rangy.getSelection();
   sel.detach();

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
    });*/
};