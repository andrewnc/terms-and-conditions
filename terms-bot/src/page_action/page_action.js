chrome.tabs.query({'active': true, 'currentWindow': true}, function (tab) {
    chrome.tabs.sendMessage(tab[0].id, {tag: "from_popup"}, function (response) {
    	document.getElementById("summary_data").innerHTML = response.data;
    });
});



