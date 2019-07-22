const express = require('express');
const app = express();
const http = require('http').createServer(app);
const io = require('socket.io')(http);
const s_client = require('socket.io-client');
const WebSocket = require('ws');
const fs = require('fs')

//app.get('/', function(req, res){
  //res.sendFile(__dirname + '/public/index.html');
//});

argparser = argparse.ArgumentParser(description='Object Detection')
argparser.add_argument('-p', dest='httpport', help='http port number', type=int, required=False)
args = argparser.parse_args()

app.use('/', express.static('public'));

function isJson(str) {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}

let sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

io.on('connection', (socket) => {
  console.log('Socket succesfully connected with id: '+socket.id);
  var count=0

  const consumer_esp = new WebSocket('ws://localhost:30003/SASESP/subscribers/detectionProject/contquery/w_score/?format=json&mode=streaming&pagesize=5&schema=true');

  consumer_esp.onopen = function(event) {
  	// Send an initial message
  	consumer_esp.send('I am the client and I\'m listening!');
  	// Listen for messages
  	consumer_esp.onmessage = function(event) {
  		//console.log('Client received a message',event);
      //var buf = new Buffer(event.value, "binary");
      //io.sockets.emit('broadcast',decodedMessage);
      count++;

      if(event.type == "message") {
        //console.log(event['data']['events'])
        //console.log(JSON.stringify(event));
        //console.log(isJson(event))
        var decodedMessage = JSON.parse(JSON.stringify(event));
        //console.log(['data']);

        //console.log(isJson(decodedMessage.data))
        var js_ts=0
        var detection={}
        if(isJson(decodedMessage.data)){
          var detection=JSON.parse(decodedMessage['data'])
          //console.log(detection)
          if(detection.hasOwnProperty('events')){
            detection=detection['events'][0]['event']
            var ts = detection["attributes"]["timestamp"]
            var js_ts = new Date(ts/1000);
            js_ts=new Date(new Date().getTime() + 2 * (Math.random() - 0.5) * 1000);
            //console.log(detection)
          }
        }

        if(detection){
          //find _ObjectN_ and _PObjectN_
          var total_objects = (Object.keys(detection).length - 5) / 2
          var total_objects_detected = detection['_nObjects_']
          var out = [];
          try {

            for(let i = 0; i < total_objects_detected; i++){
              //console.log(detection)
              console.log("_Object"+i+"_"+":"+ detection["_Object"+i+"_"])
              console.log("_P_Object"+i+"_"+":"+detection["_P_Object"+i+"_"])
              //var dt=new Date(t*1000);
              var row={"id": detection["id"],
                       "timestamp" : js_ts,
                       "object_name" : detection["_Object"+i+"_"],
                       "object_likelihood" : detection["_P_Object"+i+"_"]
                     }
              out.push(row);
              //sleep(10000)
              io.sockets.emit('broadcast',row);
            }

            //const data = fs.writeFileSync('events/event'+count, detection)
            //io.sockets.emit('broadcast',decodedMessage);
            //file written successfully
          } catch (err) {
            console.error(err)
          }
        }

      }
  	};

  	// Listen for socket closes
  	consumer_esp.onclose = function(event) {
  		console.log('Client notified socket has closed',event);
  	};
  	// To close the socket....
  	//socket.close()
  };

  socket.on('connect', function(){
    console.log("connected")
  });

});

app.get('/', function(req, res){
  res.send('<h1>Hello world</h1>');
});


//const port = 8000;
//const port = 80;
//io.listen(port);
if args.httpport:
  http.listen(args.httpport, function(){
    console.log('listening on *:', port);
  });
else:
  http.listen(8080, function(){
    console.log('listening on *:', port);
  });
//console.log('listening on port ', port);
