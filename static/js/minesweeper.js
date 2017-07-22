(function(){
  console.log('js start loading');

  var webSocketBridge = new channels.WebSocketBridge();
  // debug
  window.b = webSocketBridge

  webSocketBridge.connect('/minesweeper/stream/4')
  webSocketBridge.listen(function(action, stream) {
    console.log('received message', action, stream);
  });

  webSocketBridge.socket.addEventListener('open', function() {
    console.log('connection opened');
    webSocketBridge.send({
      request: 'reveal',
      data: {
        position: [0, 0],
      }
    });
  })
})()
