function confirmacion(titulo, contenido, url_ok, url_nok, texto_ok, texto_nok) {
    $.confirm({
        theme: 'Material',
        title: titulo,
        icon: 'fa fa-info',
        content: contenido,
        columnClass: 'medium',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: 'Si',
                btnClass: 'btn-green',
                action: function(){
                    document.location.href = url_ok;
                    $.alert(texto_ok);
                }
            },
            info1: {
                text: 'No',
                btnClass: 'btn-red',
                keys:['esc'],
                action: function(){
                    if (url_nok != "") {
                        document.location.href = url_nok;
                    }
                    $.alert(texto_nok);
                }
            },
        }
    });
}
function aviso(titulo, contenido) {
    $.confirm({
//        theme: 'Material',
        title: titulo,
        icon: 'fa fa-info',
        content: contenido,
//        columnClass: 'small',
        autoClose: false,
//        typeAnimated: true,
//        cancelButtonClass: 'btn-primary',
//        draggable: true,
//        dragWindowBorder: false,
        buttons: {
            buttonName: {
                text: 'OK',
                btnClass: 'btn-blue',
//                keys:['esc','enter'],
            }
        }
    });
}
function cuadro(objeto_id, objeto_lb) {
    objeto_lb.removeClass("form-check-label");
    objeto_lb.after(objeto_id);
    objeto_id.removeClass("checkboxinput");
    objeto_id.removeClass("form-check-input");
    objeto_id.css("display", "block");
    objeto_id.css("text-align", "center");
    objeto_id.css("width", objeto_lb.css("width"));
//    objeto_id.css("margin-top", "5px");
    objeto_id.css("height", "25px");
}