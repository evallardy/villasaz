function aviso(titulo, contenido) {
    $.confirm({
        theme: 'Material',
        title: titulo,
        icon: 'fa fa-info',
        content: contenido,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: 'OK',
                btnClass: 'btn-green',
                keys: ['esc', 'enter']
            }
        }
    });
}
function editaArea(idArea) {
    $("#editaArea").modal("show");
}