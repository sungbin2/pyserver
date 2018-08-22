

function getDateStr(myDate){
    return (myDate.getFullYear() + '-' + ("0" + (myDate.getMonth() + 1)).slice(-2)  + '-' + ("0" + myDate.getDate()).slice(-2));
}
function getMonthStr(myDate){
    return (myDate.getFullYear() + '-' + ("0" + (myDate.getMonth() + 1)).slice(-2));
}

/* 오늘 날짜를 문자열로 반환 */
function today() {
  var d = new Date()
  return getDateStr(d)
}

/* 오늘로부터 1주일전 날짜 반환 */
function lastWeek() {
  var d = new Date()
  var dayOfMonth = d.getDate()
  d.setDate(dayOfMonth - 6)
  return getDateStr(d)
}

function last2Week() {
  var d = new Date()
  var dayOfMonth = d.getDate()
  d.setDate(dayOfMonth - 13)
  return getDateStr(d)
}
function Month() {
  var d = new Date()
  var monthOfYear = d.getMonth()
  return getMonthStr(d)
}

/* 1개월전 날짜 반환 */
function lastMonth() {
  var d = new Date()
  var monthOfYear = d.getMonth()
  d.setMonth(monthOfYear - 1)
  return getMonthStr(d)
}
var now = new Date();


$("#dates").val( today());
$("#datee").val( today());


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
                            .setContentValue(this.item.id, 1, today())
                            .close();
                }
            },
            week1: {
                label: "1주", onClick: function () {
                    this.self
                            .setContentValue(this.item.id, 0, lastWeek())
                            .setContentValue(this.item.id, 1, today())
                            .close();
                }
            },
            week2: {
                label: "2주", onClick: function () {
                    this.self
                            .setContentValue(this.item.id, 0, last2Week())
                            .setContentValue(this.item.id, 1, today())
                            .close();
                }
            },
            thisMonth: {
                label: "당월", onClick: function () {
                    this.self
                            .setContentValue(this.item.id, 0, Month() + '-01')
                            .setContentValue(this.item.id, 1, Month()
                                    + '-'
                                    + ax5.util.daysOfMonth(now.getFullYear(), now.getMonth()))
                            .close();
                }
            },
            prevMonth: {
                label: "전월", onClick: function () {
                    this.self
                            .setContentValue(this.item.id, 0, lastMonth() + '-01')
                            .setContentValue(this.item.id, 1, lastMonth()
                                    + '-'
                                    + ax5.util.daysOfMonth(now.getFullYear(), now.getMonth()-1))
                            .close();
                }
            },
            ok: {label: "닫기", theme: "default"}
         }
    });

});
