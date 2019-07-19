var socket = require('socket.io-client')('http://localhost:8000');

socket.on('connect', function(){
  console.log("Connected");
  socket.on('event', function(data){console.log("Event")});
  socket.on("broadcast", function(message) {
    console.log(message)
  });
});

socket.on('disconnect', function(){console.log("Disconnected")});

// Replace the onevent function with a handler that captures all messages
socket.onevent = function (packet) {
  // Compare the list of callbacks to the incoming event name
 console.log(packet)
};
