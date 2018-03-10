// Saves options to chrome.storage
function save_options() {
    var developerMode = document.getElementById('developer_mode').checked;
    var serverIp = document.getElementById('server_ip').value;
    var port = document.getElementById('port').value;
    chrome.storage.sync.set({
        developerMode: developerMode,
        serverIp: serverIp,
        port: port
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
    // Use default value color = 'red' and likesColor = true.
    chrome.storage.sync.get({
        developerMode: false,
        serverIp: "",
        port: ""
    }, function (items) {
        document.getElementById('developer_mode').checked = items.developerMode;
        document.getElementById('server_ip').value = items.serverIp;
        document.getElementById('port').value = items.port;
    });
}

document.addEventListener('DOMContentLoaded', restore_options);
document.getElementById('save').addEventListener('click',
    save_options);