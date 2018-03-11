chrome.tabs.query({'active': true, 'currentWindow': true}, function (tab) {
    chrome.tabs.sendMessage(tab[0].id, {tag: "from_popup"}, function (response) {
    });
});

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
      if (request.tag === "for_popup") {
          document.getElementById("summary_data").innerHTML = request.data;
      }
  });
