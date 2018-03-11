var counter = 0;
chrome.tabs.query({'active': true, 'currentWindow': true}, function (tab) {
    if(counter !== 0){
        //pass
        console.log("nope, already done");
    }else{
        chrome.tabs.sendMessage(tab[0].id, {tag: "from_popup"}, function (response) {
            counter += 1;
        });

    }

});

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
      if (request.tag === "for_popup") {
          document.getElementById("summary_data").innerHTML = request.data;
      }
  });
