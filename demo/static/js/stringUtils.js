var farmAppString = {getURL: null,
                     getQueryString: null,
                     setQueryString: null};
farmAppString.getURL = function (s) {
    var delimiter = s.search("\\?");
    var tmp = s.slice(0, delimiter);
    // tmp = "http://localhost:8000/assets/api/cows/";
    var comps = tmp.split("//");
    if (comps.length == 2) {
        // drop schema
        comps = comps[1].split(":");
    } else {
        comps = comps[0].split(":");
    }
    if (comps.length > 1) {
        comps = comps[1].split("/");
    } else {
        comps = comps[0].split("/");
    }
    if (parseInt(comps[0]) > 0) {
        comps = comps.splice(1);
    }
    var url = "#/" + comps.join("/");
    return url;
}

farmAppString.getQueryString = function (s) {
    var qs = "";
    var delimiter = s.search("\\?");
    var tmp = s.slice(delimiter + 1);
    var kv_pairs = tmp.split("&");
    for (var i = 0; i < kv_pairs.length; i++) {
        var e = kv_pairs[i].split("=");
        var k = e[0];
        var v = e[1];
        if (k == "limit") {
            qs += "/limit/" + v;
        } 
        if (k == "offset") {
            qs += "/offset/" + v;
        }
    }
    return qs.substring(1) + "/";
}

farmAppString.setQueryString = function (offset, limit) {
    console.log("offset: " + offset);
    console.log("limit: " + limit);
    var qs = "?offset=" + offset + "&limit=" + limit;
    return qs
}

farmAppString.bs2uc = function(s1) {
    var s2 = s1.toLowerCase();
    var s3 = "";
    for (var i = 0; i < s2.length; i++) {
        if (s2[i] == " ") {
            s3 = s3.concat("_");
        } else {
            s3 = s3.concat(s2[i]);
        }
    }
    return s3;
}
