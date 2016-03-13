
$(function() {
    //hang on event of form with id=myform
    $("#searchForm").submit(function(e) {

        //prevent Default functionality
        e.preventDefault();

        //get the action-url of the form
        var actionurl = e.currentTarget.action;

        //do your own request an handle the results
        $.ajax({
                url: "/search",
                type: 'post',
                dataType: 'json',
                data: $("#searchForm").serialize(),
                success: function(data) {
                    $('#nav').empty();
                    var arr = data['result'];
                    var table = "<table id='searchResTable'><th>#</th><th>Results</th>";

                    console.log(arr);

                    $("#nav").append(table);
                }
        });

    });

});
