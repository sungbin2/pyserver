var sel_gidx = 0;
var sel_idx = 0;
var table2 = [];
var _url = "{{url_for('_system_table2')}}";


$(function () {
    $.getJSON(_url, function (json) {
        table2 = json;
    }).done(function () {
        redraw();
    });


});


function redraw() {
    var $group_menu = $("#group_menu");
    $("#group").empty();
    for (var i in table2) {
        $new_grp = $('<a class="item 그룹 {1}" href="#" onclick="change_idx(this)" > {0} </a>'
            .format(table2[i].그룹명, i == sel_gidx ? 'active' : ''));
        $new_grp.data('gidx', i);
        $("#group").append($new_grp);
    }
    $("#group").append($group_menu);

    $('#btn_gb_add').click(function () {
        table2.push({tbls: [], 그룹명: "새 그룹"});
        redraw();
    });

    $('#btn_gb_l').click(function () {
        if (sel_gidx > 0) {
            var _temp_c = table2[sel_gidx];
            table2[sel_gidx] = table2[sel_gidx - 1];
            table2[sel_gidx - 1] = _temp_c;
            sel_gidx = sel_gidx - 1
        }
        _log(sel_gidx);
        redraw();
    });

    $('#btn_gb_r').click(function () {
        if (sel_gidx < (table2.length - 1)) {
            var _temp_c = table2[sel_gidx];
            table2[sel_gidx] = table2[sel_gidx + 1];
            table2[sel_gidx + 1] = _temp_c;
            sel_gidx = sel_gidx + 1
        }
        _log(sel_gidx);
        redraw();
    });

    $('#btn_add').click(function () {
        table2[sel_gidx].tbls.push(new TBL('새 테이블', 5, 5, 100, 100));
        redraw();
    });

    $('#btn_save').click(function () {
        $('#modal_save')
            .modal({
                onApprove: function () {
                    $.ajax({
                        method: "POST",
                        url: _url,
                        data: JSON.stringify(table2)
                    })
                        .done(function (msg) {
                            if (msg == 'modified')
                                window.location.replace(_url);
                            else
                                alert("alert:" + msg);
                        });
                }
            })
            .modal('show');
    });

    $('#btn_auto').click(function () {
        var _id = $(this).data('id');
        $('#modal_auto')
            .modal({
                onApprove: function () {
                    if (!parseInt($("input[name='autorow']").val())) {
                        alert("상하칸: 올바른 숫자를 입력해주시기 바랍니다");
                        return false;
                    }
                    if (!parseInt($("input[name='autocol']").val())) {
                        alert("좌우칸: 올바른 숫자를 입력해주시기 바랍니다");
                        return false;
                    }
                    if (!parseInt($("input[name='autorowgap']").val())) {
                        alert("간격: 올바른 숫자를 입력해주시기 바랍니다");
                        return false;
                    }
                    /*if (!parseInt($("input[name='autocolgap']").val())) {
                        alert("좌우간격: 올바른 숫자를 입력해주시기 바랍니다");
                        return false;
                    }*/

                    var row = parseInt($("input[name='autorow']").val());
                    var col = parseInt($("input[name='autocol']").val());
                    var gap = parseInt($("input[name='autorowgap']").val());
                    var fWidth = $("#floor").width();
                    var fHeight = $("#floor").height();
                    var cWidth = Math.floor((fWidth - (gap * (col + 1))) / col);
                    var cHeight = Math.floor((fHeight - (gap * (row + 1))) / row);

                    var pos_top = [];
                    var pos_bottom = [];
                    var pos_left = [];
                    var pos_right = [];

                    for (var i = 0; i < row; i++) {
                        pos_top.push((i * (cHeight + gap)) + gap);
                        pos_bottom.push((i * (cHeight + gap)) + cHeight + gap);
                    }
                    for (var i = 0; i < col; i++) {
                        pos_left.push((i * (cWidth + gap)) + gap);
                        pos_right.push((i * (cWidth + gap)) + cWidth + gap);
                    }


                    // for (var _index = 0; _index < table2[sel_gidx].tbls.length; _index++) {
                    //     // delete table2[sel_gidx].tbls[_index];
                    //     table2[sel_gidx].tbls.splice(_index, 1);
                    // }
                    table2[sel_gidx].tbls = [];

                    cnt_num = 0;
                    for (var i = 0; i < row; i++) {
                        for (var j = 0; j < col; j++) {
                            table2[sel_gidx].tbls.push(
                                TBL(++cnt_num + '번 테이블', pos_left[j], pos_top[i], cWidth, cHeight));
                        }
                    }
                    redraw();

                }
            })
            .modal('show');
    });


    var no = 0;
    $("#floor").empty();
    for (var i in table2[sel_gidx].tbls) {
        var temp = table2[sel_gidx].tbls[i];
        if (true) {
            $new_tbl = $('<div class="ui segment"> <div class="ui top attached label">HTML</div> </div>');
            $new_tbl.data('idx', i).css({
                "left": temp.x,
                "top": temp.y,
                "width": temp.width,
                "height": temp.height,
                "position": "absolute",
                "margin": 0,
                "padding": 0
            }).resizable({
                minWidth: 100, minHeight: 100, containment: "parent", stop: function () {
                    AfterMove($(this));
                }
            }).draggable({
                cancel: ".ui.top.attached.label", containment: "parent", stop: function () {
                    AfterMove($(this));
                }
            });
            $new_tbl.children('.label').html((no++) + ' | ' + temp.name +
                ('<div class="ui top right attached label" style="margin:0px;">' +
                    '<i class="pencil alternate 링크 icon 수정" data-idx="{0}"></i> ' +
                    '<i class="close 링크 icon 삭제" data-idx="{0}"></i> ' +
                    '</div>').format(i));
            $("#floor").append($new_tbl);
            temp.번호 = no;
        }
    }

    // $(document).on('click', 'i.수정', function () {
    $('i.수정').click(function () {
        var _idx = $(this).data('idx');
        var a_data = table2[sel_gidx].tbls[_idx];
        for (var each in a_data) {
            var each_ = $("input[name='{0}']".format(each));
            if (each_.parent().hasClass('checkbox')) {
                if (a_data[each] == 'O')
                    each_.parent().checkbox('check');
                else
                    each_.parent().checkbox('uncheck');
            }
            else if (each_.next().hasClass('dropdown icon')) {
                each_.parent().dropdown('set selected', a_data[each]);
            }
            else
                each_.val(a_data[each]);
        }

        $('#modal_modify')
            .modal({
                onApprove: function () {
                    // onDelete("{{ url }}", _id);
                    table2[sel_gidx].tbls[_idx].name = $("input[name='name']").val();
                    redraw();
                }
            })
            .modal('show');
    });

    $('i.삭제').click(function () {
        var _idx = $(this).data('idx');
        // delete table2[sel_gidx].tbls[_idx];
        table2[sel_gidx].tbls.splice(_idx, 1);
        redraw();
    });

}

function AfterMove(o) {
    var temp = table2[sel_gidx].tbls[o.data('idx')];
    temp.x = o.position().left;
    temp.y = o.position().top;
    temp.width = o.width();
    temp.height = o.height();
    // JSON.parse(JSON.stringify(temp))
    for (var i in table2[sel_gidx].tbls) {
        var against = table2[sel_gidx].tbls[i];
        if (o.data('idx') != i) {
            if (collision_detection(temp, against)) {
            }
        }
    }
}

function change_idx(sender) {
    $('a.그룹').removeClass('active');
    $(sender).addClass('active');
    sel_gidx = $(sender).data('gidx');
    redraw();
}

