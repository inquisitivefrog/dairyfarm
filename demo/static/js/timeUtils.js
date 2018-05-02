function currentDate() {
    var t = new Date();
    var year = t.getFullYear();
    var month = t.getMonth() + 1;
    var day = t.getDate();
    var hour = t.getHours();
    var min = t.getMinutes();
    var sec = t.getSeconds();
    var today = new Date(Date.UTC(year, month, day, hour, min, sec));
    var yyyy = today.getFullYear();
    var mm = today.getMonth() + 1;
    var dd = today.getDate();
    if (dd < 10) {
        dd = "0" + dd;
    }
    if (mm < 10) {
        mm = "0" + mm;
    }
    var today = yyyy + "-" + mm + "-" + dd;
    return today;
} 

function convertDate(d) {
    console.log("orig date: " + String(d));
    // convert YYYY-mm-dd to dd/mm/YYYY
    var year = d.slice(0, 4);
    var month = d.slice(5, 7);
    var day = d.slice(8, 10);; 
    var today = month + "/" + day + "/" + year;
    return today;
}
