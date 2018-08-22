

function loaddata() {
    data0 = [];
    var a = 0;var n=0;
    var week = new Array('일', '월', '화', '수', '목', '금', '토');

    for( i in _data['일자별'] ) {
        data0.push(_data['일자별'][i]);
    }
    for( i in data0) {

        n = parseInt(data0[i]['총거래액']) / parseInt(data0[i]['영수건수'])
        d = new Date(data0[i]['영업일자']).getDay()

        gridList[i] = {};
        gridList[i]['일자'] = data0[i]['영업일자'];
        gridList[i]['요일'] = week[d];
        gridList[i]['영업일수'] = 1;
        gridList[i]['총매출'] = data0[i]['총거래액'];
        gridList[i]['총할인'] = data0[i]['총할인액'];
        gridList[i]['실매출'] = data0[i]['실거래액'];
        gridList[i]['가액'] = data0[i]['판매이익'];
        gridList[i]['부가세'] = data0[i]['세금'];
        gridList[i]['영수건수'] = data0[i]['영수건수'];
        gridList[i]['판매건수'] = data0[i]['판매건수'];
        gridList[i]['일반'] = data0[i]['총할인액'];
        gridList[i]['영업일자'] = Math.round(n);
        gridList[i]['영수단가'] = data0[i]['총할인액'];
//        gridList[i].a = data0[i]['영업일자'];
//        gridList[i].a = data0[i]['영업일자'];
//        gridList[i].a = data0[i]['영업일자'];

        for (j in data0[i]['분류별']) {
            gridList[i]['실매출'+j] = data0[i]['분류별'][j]['실거래액'];
            gridList[i]['수량'+j] = data0[i]['분류별'][j]['영수건수'];
        }

        for (k in data0[i]['상품별']) {
            gridList1[a] = {};
            gridList1[a]['일자'] = data0[i]['영업일자'];
            gridList1[a]['대분류'] = _data['상품분류'][data0[i]['상품별'][k]['ppi']]
            gridList1[a]['상품코드'] = k
            gridList1[a]['상품명'] = _data['상품목록'][k]
            gridList1[a]['수량'] = data0[i]['상품별'][k]['영수건수']
            gridList1[a]['총매출액'] = data0[i]['상품별'][k]['총거래액']
            gridList1[a]['총할인액'] = data0[i]['상품별'][k]['총할인액']
            gridList1[a]['실매출액'] = data0[i]['상품별'][k]['실거래액']

            a++;
        }

    }

}