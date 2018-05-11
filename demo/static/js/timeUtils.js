function convertDate(dt) {
    var year = dt.getFullYear();
    var month = dt.getMonth();
    var day = dt.getDate();
    var hour = dt.getHours();
    var min = dt.getMinutes();
    var sec = dt.getSeconds();
    var d = new Date(Date.UTC(year, month, day, hour, min, sec));
    var yyyy = d.getFullYear();
    var mm = d.getMonth() + 1;
    if (mm < 10) {
        mm = "0" + mm;
    }
    var dd = d.getDate();
    if (dd < 10) {
        dd = "0" + dd;
    }
    var date = yyyy + "-" + mm + "-" + dd;
    return date;
} 

function convertDateTime(dt) {
    var year = dt.getFullYear();
    var month = dt.getMonth();
    var day = dt.getDate();
    var hour = dt.getHours();
    var min = dt.getMinutes();
    var sec = dt.getSeconds();
    var d = new Date(Date.UTC(year, month, day, hour, min, sec));
    var yyyy = d.getFullYear();
    var mm = d.getMonth() + 1;
    if (mm < 10) {
        mm = "0" + mm;
    }
    var dd = d.getDate();
    if (dd < 10) {
        dd = "0" + dd;
    }
    var HH = d.getHours();
    if (HH < 10) {
        HH = "0" + HH;
    }
    var MM = d.getMinutes();
    if (MM < 10) {
        MM = "0" + MM;
    }
    var datetime = yyyy + "-" + mm + "-" + dd + "T" + HH + ":" + MM;
    return datetime;
} 

function currentDate() {
    var t = new Date();
    return convertDate(t);
}

function currentDateTime() {
    var t = new Date();
    return convertDateTime(t);
}
function reformatDate(d) {
    // convert YYYY-mm-dd to dd/mm/YYYY
    var year = d.slice(0, 4);
    var month = d.slice(5, 7);
    var day = d.slice(8, 10);; 
    var today = month + "/" + day + "/" + year;
    return today;
}
