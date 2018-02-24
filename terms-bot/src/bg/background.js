//example of using a message handler from the inject scripts
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
  	chrome.pageAction.show(sender.tab.id);
  	var xhr = new XMLHttpRequest();

  	// this will change if we host somewhere
	xhr.open("POST", 'http://127.0.0.1:5000/background.py', false);

	//Send the proper header information along with the request
	xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhr.withCredentials = false;
	// xhr.send(JSON.stringify(request));
	xhr.send(request.data);

	// xhr.rsponse contains the summary from background.py
	var summary = xhr.response

	// document.getElementById('x').innerHTML = summary;
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
		  chrome.tabs.sendMessage(tabs[0].id, {resp: tabs[0]}, function(response) {
		    // nothing
		  });
	});
  });