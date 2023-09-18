'use strict';

var languageCode = 'es';

function zeroFill( number, width ) {
    width -= number.toString().length;
    if ( width > 0 ) {
        return new Array( width + (/\./.test( number ) ? 2 : 1) ).join( '0' ) + number;
    }
    return number + "";
}

function marca1Imput() {    // marca 1º imput
    $('input, select, textarea').each(function(){
        var $this = $(this),
            id = $this.attr('id');

        //if (id && (id != 'id_accesos') & (!$this.is('[readonly]') && $this.is(':visible'))) {
        if (id && (id != 'id_accesos') && (!$this.is('[readonly]')) && $this.is(':visible') && (!$this.is(':disabled'))) {
            if($this.is("select")) {
                $this.select2('open');
                $this.select2('close');
            } else {
                $this.focus().select();
            }
            return false;
        }
    });
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function esColorHexa(valor) {
    if (valor.indexOf('#')==0 && valor.length<8) {
        valor = valor.substr(1).toLowerCase();
        return zeroFill((parseInt(valor, 16).toString(16), 6) === valor);
    }
    return false;
}

function getFormData($form) {
    var unindexed_array = $form.serializeArray(),
        indexed_array = {};

    $.map(unindexed_array, function(n, i) {
        indexed_array[n['name']] = n['value'];
    });

    // añade los choice-multiple-select2, un array con id y text
    $('.choice-multiple-select2').each(function(i){
        var data = $(this).select2('data'),
            array = [];

        for (var i = 0; i < data.length; i++)
            array.push([data[i].id, data[i].text])

        indexed_array[$(this).attr('name')] = array;
    });

    // añade los checbox no marcados
    $('input[type=checkbox]').each(function(e) {
        var $this = $(this),
            id = $this.attr('id');

        if (!$this.is(':checked'))
            indexed_array[id] = null;
    });

    delete indexed_array.csrfmiddlewaretoken;

    return indexed_array;
}

function formAjax(url, param, funcion) {
    var formData = new FormData(),
        json = JSON.stringify(param);

    formData.append('csrfmiddlewaretoken', csrf_token);
    formData.append('param', json);

    $.ajax({
        url: url,
        type: 'POST',
        data: formData,
        dataType: 'JSON',
        processData: false,
        contentType: false,
        success: function(resul){
            if (resul.hasOwnProperty('err') && resul.err) {
                alert(resul.err);
            } else {
                funcion(resul.param);
            }
        },
        error: function(e){
            location.reload();
            //alert('ERROR. ' + e);
        }
    });
}

