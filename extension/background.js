
'use strict';

var token=''
chrome.runtime.onInstalled.addListener(function() {
  fetch('http://localhost:8888/').then(r => r.text()).then(result => {
    console.log(result);
    token = result;
  });
});


chrome.webRequest.onBeforeSendHeaders.addListener(
  function(details) {
  	console.log(details.requestHeaders)
    details.requestHeaders.push({'name':'aloha', 'value':'mahalo'})
    details.requestHeaders.push({'name':'x-ztrust-token', 'value':token})
    return { requestHeaders: details.requestHeaders };
  },
  {urls: ['http://localhost:8080/*']},
  ['blocking', 'requestHeaders', 'extraHeaders']
);
