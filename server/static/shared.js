function _log(theArgs) {
    console.log(theArgs);
}

$.fn.form.settings.prompt.ipv4 = '올바른 속성 값을 입력하십시오: {identifier}';
$.fn.form.settings.rules.ipv4 = function (value) {
    splits = value.split('.');
    if (splits.length != 4)
        return false;
    for (var i in splits)
        if (0 > splits[i] * 1 && splits[i] * 1 > 255)
            return false;
    return true;
}

function onApply(_url, id) {
    $.getJSON(_url + '/' + id, function (json) {
        _data = json;
    }).done(function () {
        for (var each in _data) {
            var each_ = $("input[name='{0}']".format(each));
            if (each_.parent().hasClass('checkbox')) {
                if (_data[each] == 'O')
                    each_.parent().checkbox('check');
                else
                    each_.parent().checkbox('uncheck');
            }
            else if (each_.next().hasClass('dropdown icon')) {
                each_.parent().dropdown('set selected', _data[each]);
            }
            else
                each_.val(_data[each]);
        }
    })
}


function onAdd(_url) {
    $.ajax({
        method: "POST",
        url: _url + '/' + '0',
        data: $('#form_modify').serialize()
    })
        .done(function (msg) {
            if (msg == 'added')
                window.location.replace(_url);
            else
                alert("alert:" + msg);
        });
}


function onModify(_url, id) {
    $.ajax({
        method: "PUT",
        url: (id != null ? _url + '/' + id : _url),
        data: $('#form_modify').serialize()
    })
        .done(function (msg) {
            if (msg == 'modified'){
                window.location.replace(_url);
                }
            else
                alert("alert:" + msg);
        });
}


function onDelete(_url, id) {
    $.ajax({
        method: "DELETE",
        url: _url + '/' + id
    })
        .done(function (msg) {
            if (msg == 'deleted')
                window.location.replace(_url);
            else
                alert("alert:" + msg);
        });
}

function getList(_url) {
    $.getJSON(_url, function (json) {
        ichae_net.juitbl_data = json;
    }).done(function () {
        ichae_net.juitbl.update(ichae_net.juitbl_data);

        var juitbl_td = $("#juitbl td");
        for (var i = 0; i < juitbl_td.length; i++) {
            if (juitbl_td[i].innerHTML == "O")
                juitbl_td[i].innerHTML = '<i class="green check circle icon"></i>';
            else if (juitbl_td[i].innerHTML == "X")
                juitbl_td[i].innerHTML = '<i class="red ban icon"></i>';
        }
    })
}


function initialize_form() {
    $("#form_modify input").val("");
    $("#form_modify " + '.ui.checkbox').checkbox('set checked');
    $("#form_modify " + '.ui.checkbox').checkbox('uncheck');
    $("#form_modify " + '.ui.dropdown').dropdown('restore defaults');
}

function onMoveUp(_url, id) {
    $.ajax({
        method: "PUT",
        url: _url + '/' + id + '/moveup',
        data: $('#form_modify').serialize()
    })
        .done(function (msg) {
            if (msg == 'modified')
                window.location.replace(_url);
            else
                alert("alert:" + msg);
        });
}

function onMoveDown(_url, id) {
    $.ajax({
        method: "PUT",
        url: _url + '/' + id + '/movedown',
        data: $('#form_modify').serialize()
    })
        .done(function (msg) {
            if (msg == 'modified')
                window.location.replace(_url);
            else
                alert("alert:" + msg);
        });
}
