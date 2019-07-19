//var kafka = require('kafka-node');
const io = require('socket.io')();
const s_client = require('socket.io-client');
const WebSocket = require('ws');
const fs = require('fs')
//const kclient = new kafka.Client("127.0.0.1:2181");

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

  const consumer_esp = new WebSocket('ws://espserver.esp19w25.local:30001/SASESP/subscribers/detectionProject/contquery/w_score/?format=json&mode=streaming&pagesize=5&schema=true');

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
        var decodedMessage = JSON.parse(JSON.stringify(event));
        //console.log(['data']);
        var json_sample={
              data: {"events":[
                {
                    "event":{
                        "attributes":{
                            "opcode":"insert",
                            "timestamp":"1563421206210819"
                        },
                        "_Object0_":"StaticVehicle",
                        "_P_Object0_":"0.117980",
                        "_Object1_":"MovingVehicle",
                        "_P_Object1_":"0.117870",
                        "_nObjects_":"2",
                        "id":"123",
                        "_image_": "xhsj"
                      }
                }
              ]
            }
          }


        console.log(isJson(decodedMessage.data))
        var detection={}
        if(isJson(decodedMessage.data)){
          var detection=JSON.parse(decodedMessage['data'])
          if(detection.hasOwnProperty('events')){
            detection=detection['events'][0]['event']
            //console.log(detection)
          }
        }

        if(detection){
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

        /*data:{
          "events":[
          {
              "event":{
                  "attributes":{
                      "opcode":"insert",
                      "timestamp":"1563417621487418"
                  },
                  "_Object0_":"StaticVehicle",
                  "_Object0_height":"0.116*/
        //var decodedMessage = JSON.parse(event.data);
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

const port = 8000;
io.listen(port);
console.log('listening on port ', port);
