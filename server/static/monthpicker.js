

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


//$("#dates").val( today());
//$("#datee").val( today());


var picker = new ax5.ui.picker();

$(document.body).ready(function () {

    picker.bind({
        target: $('[data-picker-date="month"]'),
        direction: "top",
        content: {
            width: 200,
            margin: 10,
            type: 'date',
            config: {
                    mode : "year", selectMode: "month"
            },
            formatter: {
                pattern: 'date(month)',
                yearTmpl: "%s년",
                months: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],

            }
        },
        onStateChanged: function () {

        },
        btns: {
            thisMonth: {
                label: "당월", onClick: function () {
                    this.self
                            .setContentValue(this.item.id, 0, Month())
                            .setContentValue(this.item.id, 1, Month())
                            .close();
                }
            },
            ok: {label: "닫기", theme: "default"}
         }
    });

});
