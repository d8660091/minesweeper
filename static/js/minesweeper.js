(function(){
  console.log('here');

  const webSocketBridge = new channels.WebSocketBridge();
  webSocketBridge.connect('/minesweeper/');
  webSocketBridge.listen(function(action, stream) {
    console.log('received', action, stream);
  });

  webSocketBridge.socket.addEventListener('open', function() {
    webSocketBridge.send({prop1: 'value1', prop2: 'value1'});
  })
})()
