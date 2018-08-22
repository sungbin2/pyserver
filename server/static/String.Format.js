String.prototype.format = function ()
{
    var s = this;
    for (var i = 0; i < arguments.length; i++)
    {
        var r = new RegExp('\\{' + i + '\}', 'g');
        s = s.replace(r, arguments[i]);
    }
    return s;
};