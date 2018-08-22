

function getDateStr(myDate){
    return (myDate.getFullYear() + '-' + ("0" + (myDate.getMonth() + 1)).slice(-2)  + '-' + ("0" + myDate.getDate()).slice(-2));
}

/* 오늘 날짜를 문자열로 반환 */
function today() {
  var d = new Date()
  return getDateStr(d)
}

var now = new Date();

$("#dates").val( today());

var picker = new ax5.ui.picker();

$(document.body).ready(function () {

    picker.bind({
        target: $('[data-ax5picker="basic"]'),
        direction: "top",
        content: {
            width: 200,
            margin: 10,
            type: 'date',
            config: {
                control: {
                    left: '<i class="fa fa-chevron-left"></i>',
                    yearTmpl: '%s',
                    monthTmpl: '%s',
                    right: '<i class="fa fa-chevron-right"></i>'
                },
                lang: {
                    yearTmpl: "%s년",
                    months: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
                    dayTmpl: "%s"
                }
            }
        },
        onStateChanged: function () {

        },
        btns: {
            today: {
                label: "오늘", onClick: function () {
                    this.self
                            .setContentValue(this.item.id, 0, today())
                            .close();
                }
            },
            ok: {label: "닫기", theme: "default"}
         }
    });

});
