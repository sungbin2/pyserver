function TBL(name, x, y, width, height) {
    var o = {};
    o.name = name;
    o.x = x;
    o.y = y;
    o.width = width;
    o.height = height;
    o.isdel = 'X';
    return o;
}

function collision_detection(rect1, rect2) {
    if (rect1.x < rect2.x + rect2.width &&
        rect1.x + rect1.width > rect2.x &&
        rect1.y < rect2.y + rect2.height &&
        rect1.height + rect1.y > rect2.y) {
        console.log('collision_detected!');
        return true;
    }
    else {
        return false;
    }
}


function find_approx(l, v, flag) {
    var rtn;
    if (v <= l[0])
        rtn = l[0];
    else if (l[l.length - 1] < v)
        rtn = l[l.length - 1];
    else {
        for (var i = 1; i < l.length; i++) {
            if (l[i - 1] < v && v < l[i])
                rtn = flag ? l[i] : l[i - 1];
        }
    }
    return rtn;
}