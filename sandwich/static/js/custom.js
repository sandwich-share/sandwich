$(document).ready(function(){
    $("#query_form").on("submit", function(e) {
        e.preventDefault();
        $.get("/search", {search:
            $(this).find("input[type=text]").val()}, function(data){
                $("#content").html(data);
            });
    })
    $("#peer-list td a").on("click", function(e) {
        e.preventDefault();
        $("#query_form input[type=text]").val("");
        $.get("/search", {host: $(this).attr("data-host")}, function(data){
            $("#content").html(data);
        });
    })
    $(".dl-link").on("click", function(e) {
        e.preventDefault();
        $.get("/download", {url: $(this).attr("data-url")});
    })
})
