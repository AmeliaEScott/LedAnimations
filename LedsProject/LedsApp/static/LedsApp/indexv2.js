"use strict";

$(document).ready(function () {
    $("button.add-animation-button").click(function(e){
        console.log("WOW!!");
        let form = $(this).parents("div.add-animation-modal").find("form");
        let valid = form[0].checkValidity();
        console.log(`Valid: ${valid}`);
        form.addClass("was-validated");

        if(valid){
            let data = {};
            let formArray = form.serializeArray();
            for (var i = 0; i < formArray.length; i++){
                data[formArray[i]['name']] = formArray[i]['value'];
            }
            console.log(data);
        } else {
            e.preventDefault();
            e.stopPropagation();
        }
    });

    $("div.add-animation-modal").on("hidden.bs.modal", function (e) {
        $("form").removeClass("was-validated");
    });
});