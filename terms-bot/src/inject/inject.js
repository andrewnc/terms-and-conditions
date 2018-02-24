
var words = new Set(['terms', 'service', 'legal', 'agreement']);

// change data if you want to have something else scraped
var body_text = document.body.innerText;
var text_list = body_text.split(" ");
var send_data = false;

for(var i = 0; i < text_list.length; i++){
	if(words.has(text_list[i].toLowerCase())){
		send_data = true;
		break;
	}
}

if(send_data){
	chrome.runtime.sendMessage({status: 'sending', data:body_text, url: window.location.hostname}, function(response) {
		var readyStateCheckInterval = setInterval(function() {
		if (document.readyState === "complete") {
			clearInterval(readyStateCheckInterval);
			// send info from this function call
			console.log('sending');
		}
		}, 30);
	});


	// summary comes back here
	chrome.runtime.onMessage.addListener(
		function(request, sender, sendResponse) {
			var info = {
				data: request.resp
			}

			// here we log the response, if they want it
			console.log(request.resp);
	});	
}

