'use strict';

function select2_set_value($elemento, valor) {
    if (typeof(valor) != 'undefined') {
        for (var i = 0; i < valor.length; i++) {
            var $opcion = $('<option selected="selected"></option>').val(valor[i][0]).text(valor[i][1]);
            $elemento.append($opcion);
        }
        $elemento.trigger('change');
    }
}

function iniciaChoice($obj) {
    $obj.select2({
        language: languageCode,
        placeholder: $obj.attr('placeholder') ? $obj.attr('placeholder'): '',
        tokenSeparators: [',', ' '],
        minimumInputLength: 0,
        allowClear: true,
        multiple: false,
        templateSelection:  function (data) {
            if (!data.id)
                 return data.text;
            return $('<div>&nbsp;' + data.text  + '</div>');
        },
    });

    /* si tiene el atributo readonly */
    if ($obj.attr('readonly')) {
        $obj.prop('disabled', true);
    }
}


function iniciaChoiceAjax($obj, multiple) {
    var csrftoken = getCookie('csrftoken'),
        data_url = $obj.attr('data-url');

    $obj.select2({
//   select2 mofificable
//        tags: true,
//        createTag: function (params) {
//            return {
//                id: params.term,
//                text: params.term,
//                newTag: true,
//            }
//        },

        language: languageCode,
        //theme: 'bootstrap',
        placeholder: $obj.attr('placeholder') ? $obj.attr('placeholder'): '',
        tokenSeparators: [',', ' '],
        minimumInputLength: 0,
        allowClear: false,
        multiple: multiple,
        ajax: {
            type: 'post',
            beforeSend: function(xhr, settings){
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            },
            delay: 250,
            url: function (params) {
                return data_url;
            },
            dataType: 'json',
            data: function(params) {
                var $obj = $(this[0]),
                    param = $obj.attr('data-param'),
                    forward = $obj.attr('data-forward') || '',
                    ids = forward.split(','),
                    data = {};

                for (var i=0; i < ids.length; i++)
                    data[ids[i]] = $('#id_' + ids[i]).val();

                return {
                    term: params.term || '',
                    page: params.page || 1,
                    forward: JSON.stringify(data),
                    param: param,
                }
            },
            processResults: function (data) {
                return data;
            },
            cache: true,
        },
        templateResult:  function (data) {
            if (!data.id)
                 return data.text;

            //return $('<div><b>' + data.id  + '</b>.- ' + data.text + '</div>');
            return $('<div>' + data.text  + '</div>');
        },
        templateSelection:  function (data) {
            if (!data.id)
                 return data.text;

            // ajuste del tamaño
            var size = $('.select2.select2-container').css('font-size'),
                family = $('.select2.select2-container').css('font-family'),
                style = $('.select2.select2-container').css('font-style'),
                lon = $('#string_span').css({'font-size': size,
                                             'font-family': family,
                                             'font-style': style,
                                             'font-weight': 'bold'}).text(data.text).width() + 10;

            return $('<div style="min-width:' + lon.toString() + 'px;">' + data.text  + '</div>');
        },

    });

    /* si tiene el atributo readonly */
    if ($obj.attr('readonly')) {
        $obj.prop('disabled', true);
    }
}

function iniciaColorAjax($obj) {
    var data_url = $obj.attr('data-url');
    $obj.select2({
        language: languageCode,
        placeholder: $obj.attr('placeholder') ? $obj.attr('placeholder'): '',
        allowClear: true,
        tags: true,
        createTag: function (params) {
            if (esColorHexa(params.term)) {
                return {
                    id: params.term,
                    text: params.term,
                    newTag: true,
                }
            }
        },
        ajax: {
            type: 'post',
            beforeSend: function(xhr, settings){
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
                }
            },
            delay: 250,
            url: function (params) {
                return data_url;
            },
            dataType: 'json',
            data: function(params) {
                return {
                    term: params.term || '',
                    page: params.page || 1,
                    param: 'colores',
                }
            },
            processResults: function (data) {
                return data;
            },
            cache: true,
        },
        templateResult:  function (data) {
            if (!data.id)
                 return data.text;
            return $(`<div class='select2-color-cuadro' style='background-color:${data.text};'></div><div class='select2-color-texto'>${data.text}</div>`);
        },
        templateSelection:  function (data) {
            if (!data.id)
                 return data.text;
            return $(`<div class='select2-color-cuadro' style='background-color:${data.text};'></div><div class='select2-color-texto-selection'>${data.text}</div>`);
        },
    });

    /* si tiene el atributo readonly */
    if ($obj.attr('readonly')) {
        $obj.prop('disabled', true);
    }
}

/* autoresize select2 */
function reset_select2_size(obj) {
    if (typeof(obj)!='undefined') {
        obj.find('.select2-container').parent().each(function() {
            $(this).find('.select2-container').css({"width":"10px"});
        });
        obj.find('.select2-container').parent().each(function() {
            var width = ($(this).width()-5)+"px";
            $(this).find('.select2-container').css({"width":width});
        });
        return;
    }

    $('.select2-container').filter(':visible').parent().each(function() {
        $(this).find('.select2-container').css({"width":"10px"});
    });

    $('.select2-container').filter(':visible').parent().each(function() {
        var width = ($(this).width()-5)+"px";
        $(this).find('.select2-container').css({"width":width});
    });
}


$('.choice-select2').each(function(e) {
    iniciaChoice($(this));
});

$('.choice-simple-select2').each(function(e) {
    iniciaChoiceAjax($(this), false);
});

$('.choice-multiple-select2').each(function(e) {
    iniciaChoiceAjax($(this), true);
});

$('.color-select2').each(function(e) {
    iniciaColorAjax($(this));
});

