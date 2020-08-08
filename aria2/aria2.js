function aria2_download(r) {
    var token = "token:zDeeVE0nq5Win8YzQxXRfHkCLerHYoaKgfU0kR8DX9A";
    var diffurl = "http://diff.playkey.net:81" + r.uri;
    var json_str = JSON.stringify([token, [diffurl]]);
    var params = json_str.toBytes().toString('base64').split('=').join('%3D');
    var aria2_args = "method=aria2.addUri&id="+r.variables.request_id+"&params="+params;
    r.subrequest("/aria2", aria2_args);
    r.return(404);
}

export default {aria2_download};
