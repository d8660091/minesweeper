(function(){
  var b = new channels.WebSocketBridge();

  var vm = new Vue({
    el: '.minesweeper',
    data: {
      connected: false,
      map: [[1, 2, 3], [4,5,6], [-1, -1, -1]],
    },
    methods: {
      connect: function() {
        b.connect('/minesweeper/stream/4')
        b.listen(this.handleMessage);
        b.socket.addEventListener('open', this.handleConnectionOpen)
      },
      handleTileClick: function(x, y) {
        console.log(x, y, 'tile clicked');
        this.requestReveal(x, y);
      },
      handleTileClickRight: function(x, y) {
        console.log(x, y, 'tile right clicked');
        this.requestMark(x, y);
      },
      handleTileClickMiddle: function(x, y) {
        console.log(x, y, 'tile click middle');
      },
      handleConnectionOpen: function() {
        console.log('connection opened');
        this.connected = true;
      },
      requestReveal: function(x, y) {
        b.send({
          type: 'reveal',
          data: {
            x: x,
            y: y,
          }
        });
      },
      requestMark: function(x, y) {
        b.send({
          type: 'mark',
          data: {
            x: x,
            y: y,
          }
        });
      },
      handleMessage: function(message) {
        if (message.type === 'game_change') {
          console.log('game changed');
          this.map = message.data;
        }
      }
    },
    mounted: function() {
      console.log('component mounted');
      this.connect();
    },
  })

  // debug
  window.b = b
  window.vm = vm
})()
