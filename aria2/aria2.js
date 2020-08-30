var token = "token:aaaa";

function make_id(length) {
   var result           = '';
   var characters       = 'abcdef0123456789';
   var charactersLength = characters.length;
   for ( var i = 0; i < length; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
   }
   return result;
}

function make_aria2_args(token, method, id, params) {
    var params_b64 = JSON.stringify([token, params]).toBytes().toString('base64').split('=').join('%3D');
    var aria2_method = "aria2." + method;
    return `method=${aria2_method}&id=${id}&params=${params_b64}`
}

function aria2_download(r) {
    var diffurl = "http://diff.playkey.net:81" + r.uri;
    var args_add_uri = make_aria2_args(token, "addUri", r.variables.request_id, [diffurl]);
    var args_get_downloads = make_aria2_args(token, "tellActive", make_id(16), ['gid', 'status', 'files']);
    var file_name = r.uri.toString().substring(1);
    r.subrequest("/aria2", args_get_downloads)
        .then(res_downloads => {
            var status_downloads = {};

            function convtodict(value) {
                var fname1 = value.files[0].uris[0].uri.split('/');
                var fname2 = fname1[fname1.length - 1];
                status_downloads[fname2] = [value.gid, value.status];
            }

            JSON.parse(res_downloads.responseBody).result.forEach(convtodict);
            var checkDownloads = {}
            checkDownloads['name'] = file_name
            if (file_name in status_downloads) {
                r.error(`File ${file_name} already downloading!`);
                checkDownloads["gid"] = status_downloads[file_name][0];
                checkDownloads["downloading"] = true;
                if (status_downloads[file_name][1] == "error") {
                    r.error(`Error in download ${checkDownloads["gid"]}! file_name: ${file_name}`);
                    checkDownloads["error"] = true;
                } else {
                    checkDownloads["error"] = false;
                }
            } else {
                checkDownloads["downloading"] = false;
                checkDownloads["error"] = false;
            }
            return checkDownloads;
    }, err => {r.error(err.message);})
        .then(file_status => {
            if (file_status["downloading"]) {
                if (file_status["error"]) {
                    r.error(`Removing download ${file_status["gid"]} from aria2!`);
                    remove_args = make_aria2_args(token, "forceRemove", make_id(16), [file_status["gid"]]);
                    r.subrequest("/aria2", remove_args).then(res => { r.return(404); });
                } else {
                    r.return(404);
                }
            } else {
                r.error(`File ${file_name} not found! Creating download in aria2!`);
                r.subrequest("/aria2", args_add_uri).then(res => { r.return(404); });
            }
    })
}


function aria2_status(r) {
    var args_get_downloads = make_aria2_args(token, "tellActive", make_id(16), ['gid', 'status', 'files'])
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
