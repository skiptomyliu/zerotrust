
'use strict';

var username = 'hurricaneliu'
var token = ''

chrome.runtime.onInstalled.addListener(function() {
  fetch('http://localhost:8888/', {
  	method: 'get',
  	headers: {
      "x-ztrust-username": username
    }
  }).then(r => r.text()).then(result => {
    console.log(result);
    console.log(username);
    token = result;
  });
});


chrome.webRequest.onBeforeSendHeaders.addListener(
  function(details) {
  	console.log(details.requestHeaders)
    details.requestHeaders.push({'name':'aloha', 'value':'mahalo'})
    details.requestHeaders.push({'name':'x-ztrust-token', 'value':token})
    details.requestHeaders.push({'name':'x-ztrust-username', 'value':username})
    return { requestHeaders: details.requestHeaders };
  },
  {urls: ['http://localhost:10000/*']},
  ['blocking', 'requestHeaders', 'extraHeaders']
);
