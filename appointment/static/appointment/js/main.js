$( document ).ready(function() {

    'use strict';

    $(".date_picker_enabled").on( "click", function() {
        let picker_date_id = this.getAttribute("value");

        $('#id_date_appointment').attr('value', picker_date_id);
        get_free_intervals(picker_date_id);

        $(".date_picker_enabled").each(function() {
            $(this).removeClass("btn-info");
            $(this).addClass("btn-light");
        });

        $(this).removeClass("btn-light");
        $(this).addClass("btn-info");



        // $(".date_picker_enabled").each(function() {
        //     $(this).removeClass("btn-success");
        //     $(this).addClass("btn-secondary");
        // });


        $('#div_for_intervals').html('');
    });


    function get_free_intervals(picker_date_id) {

        var csrftoken = getCookie('csrftoken');

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        var search = {};
        search["pickerdateid"] = picker_date_id;

        $.ajax({
            url: "/getfreeintervals",
            type: "POST",
            dataType: 'json',
            data: search,
            timeout : 100000,
            success: function (data) {
                var dataJSON = JSON.parse(data);
                display_intervals(dataJSON);
            },
            error: function (e) {
                console.log("ERROR: ", e);
            },
            done: function (e) {
                console.log("DONE");
            }
        });
    }


    function display_intervals(dataJSON){
        var elem = $('#div_for_intervals');
        // elem.html('');
        elem.append("<b>Свободное время для записи:</b><br>");
        for (var i = 0; i < dataJSON.length; i++) {
            var new_button = $('<button type="button" class="btn btn-secondary m-2 interval_button" value="'+ dataJSON[i].pk + '">' +  dataJSON[i].fields.time_interval + '</button>');
            elem.append(new_button);
        }
    }

    $("body").on("click", ".interval_button", function(e) {
        var elem = $(this);
        $(".interval_button").each(function() {
            $(this).removeClass("btn-success");
            $(this).addClass("btn-secondary");
        });
        elem.removeClass("btn-secondary");
        elem.addClass("btn-success");

        var pk = this.getAttribute("value");

        $('#id_appointment').attr('value', pk);
    });


    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }




});



