"use strict";

switch (languageCode) {
    case "ca":
        var tooltips = {
            today: "Vés a avui",
            clear: "Esborra la selecció",
            close: "Tancar el selector",
            selectMonth: "Selecciona el mes",
            prevMonth: "Mes anterior",
            nextMonth: "El mes que ve",
            selectYear: "Selecciona l'any",
            prevYear: "Any anterior",
            nextYear: "L'any que ve",
            selectDecade: "Selecciona una dècada",
            prevDecade: "Dècada anterior",
            nextDecade: "Next Decade",
            prevCentury: "Segle anterior",
            nextCentury: "Segle vinent",
            pickHour: "Hora de selecció",
            incrementHour: "Incrementa l'hora",
            decrementHour: "Disminueix l'hora",
            pickMinute: "Minut de selecció",
            incrementMinute: "Incrementa el minut",
            decrementMinute: "Disminueix el minut",
            pickSecond: "Elecció segon",
            incrementSecond: "Increment segon",
            decrementSecond: "Disminueix segon",
            togglePeriod: "Canvia el període",
            selectTime: "Selecciona l'hora"
        };
        break;
    case "en":
        var tooltips = {
            today: "Go to today",
            clear: "Clear selection",
            close: "Close the picker",
            selectMonth: "Select Month",
            prevMonth: "Previous Month",
            nextMonth: "Next Month",
            selectYear: "Select Year",
            prevYear: "Previous Year",
            nextYear: "Next Year",
            selectDecade: "Select Decade",
            prevDecade: "Previous Decade",
            nextDecade: "Next Decade",
            prevCentury: "Previous Century",
            nextCentury: "Next Century",
            pickHour: "Pick Hour",
            incrementHour: "Increment Hour",
            decrementHour: "Decrement Hour",
            pickMinute: "Pick Minute",
            incrementMinute: "Increment Minute",
            decrementMinute: "Decrement Minute",
            pickSecond: "Pick Second",
            incrementSecond: "Increment Second",
            decrementSecond: "Decrement Second",
            togglePeriod: "Toggle Period",
            selectTime: "Select Time"
        };
        break;
    default:
        var tooltips = {
            today: "Hoy",
            clear: "Borrar Seleccion",
            close: "Cerrar",
            selectMonth: "Selecionar Mes",
            prevMonth: "Mes Anterior",
            nextMonth: "Mes Siguiente",
            selectYear: "Seleccionar Año",
            prevYear: "Año Anterior",
            nextYear: "Años Siguiente",
            selectDecade: "Seleccionar Década",
            prevDecade: "Década Anterior",
            nextDecade: "Década Siguiente",
            prevCentury: "Centuria Anterior",
            nextCentury: "Centuria Siguiente",
            pickHour: "Hora",
            incrementHour: "Incrementar Hora",
            decrementHour: "Decrementar Hora",
            pickMinute: "Minuto",
            incrementMinute: "Incrementar Minuto",
            decrementMinute: "Decrementar Minuto",
            pickSecond: "Segundo",
            incrementSecond: "Incrementar Segundo",
            decrementSecond: "Decrementar Segundo",
            togglePeriod: "Alternar Periodo",
            selectTime: "Seleccionar Hora"
        };
}

function iniciaDatetimepicker($obj, date) {
    $obj.datetimepicker({
        allowInputToggle: true,
        showClose: true,
        showClear: true,
        showTodayButton: true,
        format: "DD/MM/YYYY HH:mm",
        locale: languageCode,
        date: date,
        tooltips: tooltips
    });
}

function iniciaTimepicker($obj, date) {
    $obj.datetimepicker({
        allowInputToggle: true,
        showClose: true,
        showClear: true,
        showTodayButton: true,
        format: 'LT',
        locale: languageCode,
        date: date,
        tooltips: tooltips
    });
}

$(".datetimepicker").each(function(e) {
    iniciaDatetimepicker($(this), new Date());
});

$(".timepicker").each(function(e) {
    iniciaTimepicker($(this), new Date());
});
