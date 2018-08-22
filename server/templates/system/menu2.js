var sel_gidx = 0;
var sel_idx = 0;
var _grid = [];
var menu2 = [];
var goods_item = [];
var _url = "{{url_for('_system_menu2')}}";


var pos_top = [];
var pos_bottom = [];
var pos_left = [];
var pos_right = [];


var cellsize_w = 0;
var cellsize_h = 0;


$(function () {
    $.getJSON(_url, function (json) {
        menu2 = json.d;
        goods_item = json.l;
    }).done(function () {
        redraw();
        change_idx(null);
    });

});


function redraw() {
    var $group_menu = $("#group_menu");
    $("#group").empty();
    for (var i in menu2) {
        $new_grp = $('<a class="item 그룹 {1}" href="#" onclick="change_idx(this)" > {0} </a>'
            .format(menu2[i].그룹명, i == sel_gidx ? 'active' : ''));
        $new_grp.data('gidx', i);
        $("#group").append($new_grp);
    }
    $("#group").append($group_menu);

    $('#btn_gb_add').click(function () {
        menu2.push({btns: [], 그룹명: "새 그룹", row: 4, col: 4});
        redraw();
    });

    $('#btn_gb_l').click(function () {
        if (sel_gidx > 0) {
            var _temp_c = menu2[sel_gidx];
            menu2[sel_gidx] = menu2[sel_gidx - 1];
            menu2[sel_gidx - 1] = _temp_c;
            sel_gidx = sel_gidx - 1
        }
        _log(sel_gidx);
        redraw();
    });

    $('#btn_gb_r').click(function () {
        if (sel_gidx < (menu2.length - 1)) {
            var _temp_c = menu2[sel_gidx];
            menu2[sel_gidx] = menu2[sel_gidx + 1];
            menu2[sel_gidx + 1] = _temp_c;
            sel_gidx = sel_gidx + 1
        }
        _log(sel_gidx);
        redraw();
    });

    $('#btn_add').click(function () {
        var _new = new TBL('새 메뉴', 5, 5, cellsize_w, cellsize_h);
        _new.code = 0;
        menu2[sel_gidx].btns.push(_new);
        redraw();
    });

    $('#btn_save').click(function () {
        $('#modal_save')
            .modal({
                onApprove: function () {
                    $.ajax({
                        method: "POST",
                        url: _url,
                        data: JSON.stringify(menu2)
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

                    var row = parseInt($("input[name='autorow']").val());
                    var col = parseInt($("input[name='autocol']").val());
                    var gap = 5;
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


                    // for (var _index = 0; _index < menu2[sel_gidx].btns.length; _index++) {
                    //     // delete menu2[sel_gidx].btns[_index];
                    //     menu2[sel_gidx].btns.splice(_index, 1);
                    // }
                    menu2[sel_gidx].btns = [];
                    menu2[sel_gidx].row = row;
                    menu2[sel_gidx].col = col;

                    cnt_num = 0;
                    for (var i = 0; i < row; i++) {
                        for (var j = 0; j < col; j++) {
                            var _new = new TBL('새 메뉴', pos_left[j], pos_top[i], cWidth, cHeight);
                            _new.code = 0;
                            menu2[sel_gidx].btns.push(_new);
                        }
                    }
                    redraw();
                    change_idx(null);

                }
            })
            .modal('show');
    });


    var no = 0;
    $("#floor").empty();
    for (var i in menu2[sel_gidx].btns) {
        var temp = menu2[sel_gidx].btns[i];
        if (true) {
            $new_tbl = $('<div class="ui segment"> <div class="ui top attached label"></div>' +
                '<div class="ui center aligned basic segment"></div> </div>');
            $new_tbl.data('idx', i).css({
                "left": temp.x,
                "top": temp.y,
                "width": temp.width,
                "height": temp.height,
                "position": "absolute",
                "margin": 0,
                "padding": 0
            }).resizable({
                minWidth: 50, minHeight: 50, containment: "parent", stop: function () {
                    AfterMove($(this));
                }
            }).draggable({
                cancel: ".ui.top.attached.label", containment: "parent", stop: function () {
                    AfterMove($(this));
                }
            });
            $new_tbl.children('.label').html((no++) + ' | ' + temp.code +
                ('<div class="ui top right attached label" style="margin:0px;">' +
                    '<i class="pencil alternate 링크 icon 수정" data-idx="{0}"></i> ' +
                    '<i class="close 링크 icon 삭제" data-idx="{0}"></i> ' +
                    '</div>').format(i));
            $new_tbl.children('.basic').html('{0}<br/>{1}'.format(goods_item[temp.code].품목명, goods_item[temp.code].단가));
            $("#floor").append($new_tbl);
            temp.번호 = no;
        }
    }

    // $(document).on('click', 'i.수정', function () {
    $('i.수정').click(function () {
        var _idx = $(this).data('idx');
        var a_data = menu2[sel_gidx].btns[_idx];
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
                    menu2[sel_gidx].btns[_idx].code = Number(($("input[name='메뉴명']").val()).split("|")[0]);
                    redraw();
                }
            })
            .modal('show');
    });

    $('i.삭제').click(function () {
        var _idx = $(this).data('idx');
        // delete menu2[sel_gidx].btns[_idx];
        menu2[sel_gidx].btns.splice(_idx, 1);
        redraw();
    });

}

function AfterMove(o) {
    var temp = menu2[sel_gidx].btns[o.data('idx')];
    // temp.x = o.position().left;
    // temp.y = o.position().top;
    // temp.width = o.width();
    // temp.height = o.height();
    temp.x = find_approx(pos_left, o.position().left + 1, false);
    temp.y = find_approx(pos_top, o.position().top + 1, false);
    temp.width = find_approx(pos_right, temp.x + o.width(), true) - temp.x;
    temp.height = find_approx(pos_bottom, temp.y + o.height(), true) - temp.y;
    // JSON.parse(JSON.stringify(temp))
    for (var i in menu2[sel_gidx].btns) {
        var against = menu2[sel_gidx].btns[i];
        if (o.data('idx') != i) {
            if (collision_detection(temp, against)) {
            }
        }
    }
    redraw();
}

function change_idx(sender) {
    if (sender) {
        $('a.그룹').removeClass('active');
        $(sender).addClass('active');
        sel_gidx = $(sender).data('gidx');
    }
    redraw();

    _grid = [];
    pos_top = [];
    pos_bottom = [];
    pos_left = [];
    pos_right = [];


    var row = menu2[sel_gidx].row;
    var col = menu2[sel_gidx].col;
    var gap = 5;
    var fWidth = $("#floor").width();
    var fHeight = $("#floor").height();
    var cWidth = Math.floor((fWidth - (gap * (col + 1))) / col);
    var cHeight = Math.floor((fHeight - (gap * (row + 1))) / row);

    cellsize_w = cWidth;
    cellsize_h = cHeight;


    for (var i = 0; i < row; i++) {
        pos_top.push((i * (cHeight + gap)) + gap);
        pos_bottom.push((i * (cHeight + gap)) + cHeight + gap);
    }
    for (var i = 0; i < col; i++) {
        pos_left.push((i * (cWidth + gap)) + gap);
        pos_right.push((i * (cWidth + gap)) + cWidth + gap);
    }

    for (var i = 0; i < row; i++) {
        for (var j = 0; j < col; j++) {
            _grid.push(TBL('', pos_left[j], pos_top[i], cWidth, cHeight));
        }
    }

    $("#grid").empty();
    for (var i in _grid) {
        var temp = _grid[i];
        $new_tbl = $('<div class="ui disabled segment"> </div>');
        $new_tbl.data('i', i).css({
            "left": temp.x,
            "top": temp.y,
            "width": temp.width,
            "height": temp.height,
            "position": "absolute",
            "margin": 0,
            "padding": 0
        });
        $("#grid").append($new_tbl);
    }
}

