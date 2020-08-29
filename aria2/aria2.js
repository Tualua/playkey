function makeid(length) {
   var result           = '';
   var characters       = 'abcdef0123456789';
   var charactersLength = characters.length;
   for ( var i = 0; i < length; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
   }
   return result;
}

function aria_args(token, method, id, params) {
    var json_str = JSON.stringify([token, params]);
    var params = json_str.toBytes().toString('base64').split('=').join('%3D');
    return "method=aria2." + method + "&id=" + id +"&params="+params;
}

function aria2_download(r) {
    var token = "token:aaa";
    var diffurl = "http://diff.playkey.net:81" + r.uri;
    var aria2_args = aria_args(token, "addUri", r.variables.request_id, [diffurl]);
    var args_get_downloads = aria_args(token, "tellActive", makeid(16), ['gid', 'status', 'files']);
    var fileName = r.uri.toString().substring(1);
    r.subrequest("/aria2", args_get_downloads).then(rDownloads => {
        var dictDownloads = {};

        function convtodict(value) {
            var fname1 = value.files[0].uris[0].uri.split('/');
            var fname2 = fname1[fname1.length - 1];
            dictDownloads[fname2] = [value.gid, value.status];
        }
        var statusDownloads = JSON.parse(rDownloads.responseBody);
        statusDownloads.result.forEach(convtodict);
        var checkDownloads = {}
        checkDownloads['name'] = fileName
        if (fileName in dictDownloads) {
            r.error(`File ${fileName} already downloading!`);
            checkDownloads["gid"] = dictDownloads[fileName][0];
            checkDownloads["downloading"] = true;
            if (dictDownloads[fileName][1] == "error") {
                r.error(`Error in download ${checkDownloads["gid"]}! Filename: ${fileName}`);
                checkDownloads["error"] = true;
            } else {
                checkDownloads["error"] = false;
            }
        } else {
            checkDownloads["downloading"] = false;
            checkDownloads["error"] = false;
        }
        //r.error(JSON.stringify(checkDownloads, null, 1));
        return checkDownloads;
    }, err => {r.error(err.message);}).then(file_status => {
        //r.error(JSON.stringify(file_status, null, 1))
        if (file_status["downloading"]) {
            if (file_status["error"]) {
                r.error(`Removing download ${file_status["gid"]} from aria2!`);
                remove_args = aria_args(token, "forceRemove", makeid(16), [file_status["gid"]]);
                r.subrequest("/aria2", remove_args).then(res => { r.return(404); });
            } else {
                r.return(404);
            }
        } else {
            r.error(`File ${fileName} not found! Creating download in aria2!`);
            r.subrequest("/aria2", aria2_args).then(res => { r.return(404); });
        }
    })
}


function aria2_status(r) {
    var token = "token:aaaa";
    var args_get_downloads = aria_args(token, "tellActive", makeid(16), ['gid', 'status', 'files'])
    var status = r.subrequest("/aria2", args_get_downloads).then(function(res) {
        function getgid(value) {
                var fileuri = value.files[0].uris[0].uri.split('/');
                return [value.gid, value.status, fileuri[fileuri.length - 1]];
            }
        var status = JSON.parse(res.responseBody);
        var gids = status.result.map(getgid);
        r.return(200, JSON.stringify(gids, null, 1))
   });
}


export default {aria2_download, aria2_status};
