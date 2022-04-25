// Saves options to chrome.storage
function save_options() {
    var developerMode = document.getElementById('developer_mode').checked;
    var protocol = document.getElementById('protocol').value;
    var serverIp = document.getElementById('server_ip').value;
    var port = document.getElementById('port').value;
    var path = document.getElementById('path').value;
    chrome.storage.sync.set({
        developerMode: developerMode,
        protocol: protocol,
        serverIp: serverIp,
        port: port,
        path: path
    }, function () {
        // Update status to let user know options were saved.
        var status = document.getElementById('status');
        status.textContent = 'Options saved.';
        setTimeout(function () {
            status.textContent = '';
        }, 750);
    });
}

// Restores select box and checkbox state using the preferences
// stored in chrome.storage.
function restore_options() {
    chrome.storage.sync.get({
        developerMode: false,
        protocol: "https://",
        serverIp: "legal-leaf.appspot.com",
        port: "443",
        path: "/webapi/summarize"
    }, function (items) {
        document.getElementById('developer_mode').checked = items.developerMode;
        document.getElementById('protocol').value = items.protocol;
        document.getElementById('server_ip').value = items.serverIp;
        document.getElementById('port').value = items.port;
        document.getElementById('path').value = items.path;
    });
}

document.addEventListener('DOMContentLoaded', restore_options);
document.getElementById('save').addEventListener('click',
    save_options);