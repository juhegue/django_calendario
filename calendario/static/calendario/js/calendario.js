'use strict';

var handleCalendarDemo = function() {
    var containerEl = document.getElementById('external-events');
    var Draggable = FullCalendarInteraction.Draggable;
    new Draggable(containerEl, {
            itemSelector: '.fc-event',
            eventData: function(eventEl) {
            return {
                title: eventEl.innerText,
                color: eventEl.getAttribute('data-color')
            };
        }
    });

    var calendarElm = document.getElementById('calendar');

    function actualizaBD(data, accion) {
        var param = {
                data: data,
                accion: accion
            };

        formAjax(url_events, param, function(data) {
            calendar.removeAllEvents();
            calendar.refetchEvents();
        });
    }

    function formulario(start, end, title, id, color, completo, email, e_enviado, movil, m_enviado) {
        var msg_e_enviado, msg_m_enviado;
        e_enviado ? msg_e_enviado = `<small class='text-danger'> <i class="fa fa-exclamation-triangle" aria-hidden="true"></i> ${mail_enviado}.</small>` :msg_e_enviado = '';
        m_enviado ? msg_m_enviado = `<small class='text-danger'> <i class="fa fa-exclamation-triangle" aria-hidden="true"></i> ${movil_enviado}.</small>` :msg_m_enviado = '';
        var html = `
            <form class='row row-cols-lg-auto align-items-center'>
                <input type='hidden' name='id' value='${id}'>
                <div class='col-4'>
                    <div class="custom-control custom-checkbox" style="margin-top:20px">
                        <input type="checkbox" name="completo" class="custom-control-input" id="id_completo" ${completo}>
                        <label class="custom-control-label" for="id_completo">
                            ${dia_comleto}
                        </label>
                    </div>
                    <br>
                </div>
                <div class='col-4'>
                    <div class="custom-control custom-checkbox" style="margin-top:20px">
                        <input type="checkbox" name="email" class="custom-control-input" id="id_email" ${email}>
                        <label class="custom-control-label" for="id_email">
                            ${avisar_email}
                        </label>
                    </div>
                    ${msg_e_enviado}
                    <br>
                </div>
                <div class='col-4'>
                    <div class="custom-control custom-checkbox" style="margin-top:20px">
                        <input type="checkbox" name="movil" class="custom-control-input" id="id_movil" ${movil} ${movil_disable}>
                        <label class="custom-control-label" for="id_movil">
                            ${avisar_movil}
                        </label>
                    </div>
                    ${msg_m_enviado}
                    <br>
                </div>
                <div class='col-12'>
                    <select name='color' id='id_color' class='form-control color-select2' placeholder='${sel_color}' required data-url='${url_events}'>
                        <option></option>
                    </select>
                    <small class='text-secondary'>${color_hexa}</small>
                </div>
                <div class='col-12'  style="margin-top:20px">
                    <div class='input-group mb-3 datetimepicker' id='id_inicio_group'>
                        <input type='text' name='inicio' id='id_inicio' class='form-control' placeholder='${inicio}' value='${start}' required>
                        <div class='input-group-addon input-group-append' style='padding: 0 0 0 0';>
                            <span class='input-group-text'>
                                <i class='fa fa-calendar'></i>
                            </span>
                        </div>
                    </div>
                </div>
                <div class='col-12'>
                    <div class='input-group mb-3 datetimepicker'>
                        <input type='text' name='fin' id='id_fin' class='form-control' placeholder='${final}' value='${end}'>
                        <div class='input-group-addon input-group-append' style='padding: 0 0 0 0';>
                            <span class='input-group-text'>
                                <i class='fa fa-calendar'></i>
                            </span>
                        </div>
                    </div>
                </div>
                <div class='col-12'>
                    <textarea name='titulo' maxlength="250" id='id_titulo' class='form-control' rows='3' placeholder='${des_evento}' required>${title}</textarea>
                </div>
            </form>
        `;

        bootbox.dialog({
            closeButton: false,
            onEscape: function() { return false;},
            //title: 'Evento',
            message: html,
            buttons: {
                del: {
                    label: 'Eliminar',
                    className: 'btn-danger',
                    callback: function (result) {
                        var data = getFormData($('form'));
                        actualizaBD(data, 'borra');
                    }
                },
                cancel: {
                    label: text_cancelar,
                    className: 'btn-secondary',
                    callback: function (result) {
                        calendar.removeAllEvents();
                        calendar.refetchEvents();
                    }
                },
                success: {
                    label: text_aceptar,
                    className: 'btn-primary',
                    callback: function (result) {
                        var data = getFormData($('form'));
                        if (data.titulo == '' || data.inicio == '' || data.color == '') {
                            $('.errorlist').remove();
                            if (data.titulo == '')
                                $('<ul class="errorlist"><li>'+requerido+'.</li></ul>').insertAfter('#id_titulo');
                            if (data.inicio == '')
                                $('<ul class="errorlist"><li>'+requerido+'.</li></ul>').insertAfter('#id_inicio_group');
                            if (data.color == '')
                                $('<ul class="errorlist"><li>'+requerido+'.</li></ul>').insertAfter($('#id_color').next())
                            return false;
                        } else {
                            actualizaBD(data, 'actualiza');
                        }
                    }
                }
            }
        }).on('shown.bs.modal', function(e) {
            $('#id_fin').focus(function() {
                var valida = moment(end, "DD/MM/YYYY HH:mm").isValid();
                if (!end || !valida)
                    $(this).val( $('#id_inicio').val() );
            });
        });

        iniciaColorAjax($('.color-select2'));
        iniciaDatetimepicker($('#id_inicio'), moment(start, 'DD/MM/YYYY HH:mm'));
        iniciaDatetimepicker($('#id_fin'), moment(end, 'DD/MM/YYYY HH:mm'));

        formAjax(url_events, {accion: 'colores'}, function(data) {
            for (var i = 0; i < data.length; i++) {
                if (data[i][1] == color)
                    select2_set_value($('#id_color'), [[data[i][0], data[i][1]]]);
            }
        });
    }

    var calendar = new FullCalendar.Calendar(calendarElm, {
        headerToolbar: {
            left: 'dayGridMonth,timeGridWeek,timeGridDay',
            center: 'title',
            right: 'prev,next today'
        },
        dayMaxEventRows: 6, // máximo de eventos por día
        initialView: 'dayGridMonth',
        editable: true,
        droppable: true,
        themeSystem: 'bootstrap',
        views: {
            timeGrid: {
                eventLimit: 6 // eventos para timeGridWeek/timeGridDay
            }
        },
        locale: languageCode,
        eventSources: [function(info, successCallback, failureCallback) {
            $.ajax({
                url: url_events,
                type: 'POST',
                header: {'X-CSRFToken': csrf_token},
                dataType: 'json',
                data: {
                    start: info.start.toJSON(),
                    end: info.end.toJSON()
                },
                beforeSend: function(xhr, settings){
                    xhr.setRequestHeader('X-CSRFToken', csrf_token);
                },
                complete: function(obj, estado) {
                },
                error: function(obj, estado, error){
                    failureCallback(error);
                },
                success:  function(resul, estado, xhr) {
                    successCallback(resul.data);
                }
            });
        }],
        eventClick: function(info) {
            //alert( JSON.stringify(info, null, 4));
            // pasando la cadena a JSON se puede obtener la longitud de la fecha, para saber si es el día completo o no
            var cadena = JSON.stringify(info),
                pos = cadena.indexOf('"event":'),
                posIni = cadena.indexOf('"start":"', pos),
                posFin = cadena.indexOf('",', posIni),
                lonFecha = cadena.substr(posIni+9,posFin-posIni-9).length,
                title = info.event.title,
                start = moment(info.event.start).format('DD/MM/YYYY HH:mm'),
                end = moment(info.event.end).format('DD/MM/YYYY HH:mm'),
                id = info.event.id,
                color = info.event.backgroundColor,
                completo = '',
                param = {
                    id: id,
                    accion: 'agendaEvento'
                };

            lonFecha == 10 ? completo = 'checked': ''

            formAjax(url_events, param, function(data) {
                var email, movil, e_enviado, m_enviado;
                (data.aviso_email == 'True') ? email = 'checked' : email = '';
                (data.aviso_movil == 'True') ? movil = 'checked' : movil = '';
                (data.email_enviado == 'None') ? e_enviado = false : e_enviado = true;
                (data.movil_enviado == 'None') ? m_enviado = false : m_enviado = true;
                formulario(start, end, title, id, color, completo, email, e_enviado, movil, m_enviado);
            });

        },
        eventReceive: function(info) {
            //alert( JSON.stringify(info, null, 4));
            var data = $(info.draggedEl).data('event'),
                ahora = new Date();
            if (data.id == 0) {
                var title = '',
                    start = moment(info.event.start).format('DD/MM/YYYY HH:mm'),
                    end = '',
                    id = data.id,
                    color = info.event.backgroundColor;
                formulario(start, end, title, id, color, '', '', false, 'checked', false);
            } else {
                data.start = moment(info.event.start).format('DD/MM/YYYY') + ' ' + data.inicio;
                actualizaBD(data, 'receive');
            }
        },
        eventResize: function(info) {
            var data = {
                id: info.event.id,
                inicio: moment(info.event.start).format('DD/MM/YYYY HH:mm'),
                fin: moment(info.event.end).format('DD/MM/YYYY HH:mm'),
            }
            actualizaBD(data, 'resize');
        },
        eventDrop: function(info) {
            var data = {
                id: info.event.id,
                inicio: moment(info.event.start).format('DD/MM/YYYY HH:mm'),
                fin: moment(info.event.end).format('DD/MM/YYYY HH:mm'),
            }
            actualizaBD(data, 'drop');
        },
        dateClick: function(info) {
            var start = moment(info.date).format('DD/MM/YYYY HH:mm');
            formulario(start, '', '', 0, '', '', '', false, 'checked', false);
        }
    });

    calendar.render();
    calendar.setOption('height', 'auto');
};

var Calendar = function () {
	return {
		//main function
		init: function () {
			handleCalendarDemo();
		}
	};
}();

$(function () {
	Calendar.init();
});
