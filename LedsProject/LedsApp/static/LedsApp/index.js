"use strict";

$(document).ready(function(){
    for(var id in animations){
        addAnimationToList(animations[id]);
    }
    for(var animationType in animationOptions){

    }

    $(".add-animation").click(function(){
        var animationName = $(this).data("animation");
        buildAnimationModal(animationName);
    });

    $("#addAnimationButton").click(addAnimation);
});

function addAnimationToList(animation) {
    var html = '<li class="list-group-item row" id="animation' + animation.id + '">' +
        '<div class="col-xs-2">' +
        '<button class="btn btn-danger animation-delete" data-id="' + animation.id + '"><span class="glyphicon glyphicon-remove"></span></button>' +
        '<button class="btn btn-primary animation-info" data-id="' + animation.id + '"><span class="glyphicon glyphicon-info-sign"></span></button>' +
        '</div>' +
        '<div class="col-xs-10">' +
        '<h3>' + animation.name + '</h3>';

    for(var option in animation.options){
        if(animation.options.hasOwnProperty(option) && !animationOptions[animation.name]["parameters"][option]["advanced"]) {
            html += '<strong>' + option + ': </strong>' + animation.options[option] + '<br>'
        }
    }

    html += '</div></li>';

    $("#animationslist").append(html);
    $(".animation-delete").unbind("click").click(deleteAnimation);
    $(".animation-info").unbind("click").click(animationInfo);
}

function deleteAnimation(){
    var id = $(this).data("id");
    $.ajax("/removeanimation/" + id, {
        'method': 'DELETE',
        'success': function(result){
            console.log("Much success!");
            console.log(result);
            $("#animation" + id).remove();
        },
        'error': function(result){
            console.log("AAAAHHHHH");
            console.log(result);
        }
    })
}

function animationInfo(){
    var id = $(this).data("id");
}

function buildAnimationModal(animationName){
    console.log(animationName);
    var parameters = animationOptions[animationName]['parameters'];
    var hasAdvanced = false;
    $("#advancedParameters").children().remove();
    $("#advancedParameters").collapse("hide");
    $("#simpleParameters").children().remove();
    for(var parameterName in parameters){
        if(parameters.hasOwnProperty(parameterName)) {
            var parameter = parameters[parameterName];
            var html = '<div class="form-group">' +
                '<label>' + parameterName + '</label>' +
                '<input class="form-control parameter-input" data-parameter-name="' + parameterName + '" ';

            switch (parameter.type) {
                case 'INTEGER':
                case 'POSITION':
                    html += 'type="number" step="1" ';
                    break;
                case 'FLOAT':
                    html += 'type="number" step="any" ';
                    break;
                case 'STRING':
                    html += 'type="text" ';
                    break;
                case 'COLOR':
                    html += 'type="color" ';
                    break;
            }

            if (parameter.type === 'INTEGER' || parameter.type === 'FLOAT') {
                if (parameter.minimum) {
                    html += 'min="' + parameter.minimum + '" ';
                }
                if (parameter.maximum) {
                    html += 'max="' + parameter.maximum + '" ';
                }
            }

            if (parameter.default) {
                html += 'value="' + parameter.default + '" ';
            }

            html += '>';
            if (parameter.description) {
                html += '<small>' + parameter.description + '</small>';
            }
            html += '</div>';
            if (parameter.advanced) {
                hasAdvanced = true;
                $("#advancedParameters").append(html);
            } else {
                $("#simpleParameters").append(html);
            }
        }
    }
    if(hasAdvanced){
        $("#advancedPanel").removeClass("hidden");
    }else{
        $("#advancedPanel").addClass("hidden");
    }

    $("#addAnimationButton").data("animation-name", animationName);
    $("#addAnimationModal").modal("show");
}

function addAnimation(){
    var parameters = {};
    var animationName = $(this).data("animation-name");
    $(".parameter-input").each(function(){
        var input = $(this);
        var parameterName = input.data("parameter-name");
        var parameterType = input.attr("type");
        var value = input.val();
        if(parameterType === 'INTEGER' || parameterType === 'POSITION' || parameterType === 'FLOAT'){
            parameters[parameterName] = parseFloat(value);
        }else if(parameterType === 'STRING'){
            parameters[parameterName] = value;
        }else if(parameterType === 'COLOR'){
            parameters[parameterName] = hexToRgb(value);
        }
    });
    $.ajax({
        'url': '/addanimation',
        'method': 'PUT',
        'data': JSON.stringify({'name': animationName, 'data': parameters}),
        'success': function(results){
            console.log(results);
            addAnimationToList(results);
            $("#addAnimationModal").modal("hide");
        },
        'error': function(results){
            console.log("AAAAHHHH");
            console.log(results);
        }
    });
    console.log(parameters);
}

function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? [
        parseInt(result[1], 16),
        parseInt(result[2], 16),
        parseInt(result[3], 16)
    ] : null;
}