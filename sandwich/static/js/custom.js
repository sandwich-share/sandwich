$(document).ready(function(){
    $("#query_form").on("submit", function(e) {
        e.preventDefault();
        $.post("/search", {search:
            $(this).find("input[type=text]").val()}, function(data){
                $("#content").html(data);
            });
    })
    setInterval(function(){
        $.get("localhost:9000/neighbours", function(data){
          $("#neighbours").html(data);
        })
    }, 5000)
})
