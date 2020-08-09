
function int_to_rgb(k, max) {
    var a = k/max;
    var backcol = [255, 255, 221]
    var forecol = [247, 231, 180]
    //var forecol = [0, 0, 0]
    var r = backcol[0] - Math.floor((backcol[0] - forecol[0])*a);
    var g = backcol[1] - Math.floor((backcol[1] - forecol[1])*a);
    var b = backcol[2] - Math.floor((backcol[2] - forecol[2])*a);

    var str = "rgb(" + r.toString()+","+ g.toString()+","+ b.toString()+")";
    return str;
}

function get_color(zx, zy, cx, cy, n){
    var max_iter = 100;
    var k = 0;
    while (zx*zx + zy*zy < 4 && k < max_iter) {
        var zxtemp = Math.pow(zx*zx + zy*zy, n/2)*Math.cos(n*Math.atan2(zy,zx)) + cx;
        zy = Math.pow(zx*zx + zy*zy, n/2)*Math.sin(n*Math.atan2(zy,zx)) + cy;                
        zx = zxtemp;
        k += 1;
    }
    if (k == max_iter) {
        return k;
    }
    else{
        fraction = 1 - Math.log(Math.log(Math.pow(zx*zx + zy*zy,0.5)))/Math.log(n)
        return k + fraction;
    }
}

function ij_to_xy(i,j){
    return [i+1500, j+500]
}

function draw_pixel(cont, colinf,max_k){
    var xy = ij_to_xy(colinf[0],colinf[1]);
    cont.fillStyle = int_to_rgb(colinf[2], max_k);
    cont.fillRect(xy[0], xy[1], 1, 1 );
}
function make_julia(cont, cx, cy, n) {
    var c_abs = 1;
    if (typeof(cx)==='undefined') cx = - c_abs + 2*c_abs*Math.random();
    if (typeof(cy)==='undefined') cy = - c_abs + 2*c_abs*Math.random();
    if (typeof(n)==='undefined') n = Math.floor(Math.random()* (6) + 1);
    var collist = []
    console.log(cx, cy, n)
    var size = 500;
    var dividend = (1/2)*size

    for (i= -size; i < size; i++) {
        for (j = -size; j < size; j++) {
            collist.push([i, j, get_color(i/dividend, j/dividend, cx, cy, n)])
        }
    }
    var num_pix = collist.length;
    var max = 0.0;
    var mean = 0.0;
    for (var n = 0; n < num_pix; n++) {
        if (collist[n][2] > max){
            max = collist[n][2];
        }
        mean += collist[n][2];
    }
    mean /= num_pix;
    for (var m =0; m < num_pix; m ++){
        draw_pixel(cont, collist[m], mean);
    }
}


