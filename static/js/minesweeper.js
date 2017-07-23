(function(){
  var b = new channels.WebSocketBridge();

  function getNbs(map, x, y) {
    var h = map.length;
    var w = map[0].length;

    var ans = [];
    for (var i = x - 1; i <= x + 1; i++) {
      for (var j = y - 1; j <= y + 1; j++) {
        if (i >= 0 && i < h && j >= 0 && j < w) {
          if (i === x && j === y) continue;
          ans.push({
            x: i,
            y: j,
            val: map[i][j],
          });
        }
      }
    }
    var minesCount = _.filter(ans, {val: -1}).length;
    return {
      nbs: ans,
      meta: {
        minesCount: minesCount,
        Dbclickable: minesCount === map[x][y]
      },
    };
  }

  var vm = new Vue({
    el: '.minesweeper',
    data: {
      connected: false,
      map: [[], [], []],
      w: 30,
      h: 16,
      minesTotal: 99,
    },
    methods: {
      connect: function() {
        if (window.location.pathname === '/') {
          history.replaceState({}, "default", "/1");
          b.connect('/minesweeper/stream/1')
        } else {
          b.connect('/minesweeper/stream' + window.location.pathname)
        }
        b.listen(this.handleMessage);
        b.socket.addEventListener('open', this.handleConnectionOpen)
      },
      handleTileClickLeft: function(x, y, e) {
        if (e.ctrlKey) return;
        // console.log(x, y, 'tile clicked');
        this.requestReveal(x, y);
      },
      handleTileClickRight: function(x, y) {
        // console.log(x, y, 'tile right clicked');
        this.requestMark(x, y);
      },
      handleTileClickMiddle: function(x, y) {
        var res = getNbs(this.map, x, y);
        if (res.meta.Dbclickable) {
          // console.log('reveal multiple points');
          this.requestRevealMultiple(res.nbs);
        } else {
          res.nbs.forEach(function(position) {
            var selector = '#tile-' + position.x + '-' + position.y;
            setTimeout(function() {
              $(selector).removeClass('mousedown');
            }, 100)
          })
        }
      },
      handleTileMousedown: function(x, y, e) {
        if (e.ctrlKey) {
          var res = getNbs(this.map, x, y);
          res.nbs.forEach(function(position) {
            var selector = '#tile-' + position.x + '-' + position.y;
            $(selector).addClass('mousedown');
          })
          return;
        };
        if (e.which === 3) return;
        $(e.target).addClass('mousedown');
      },
      handleRestartClick: function() {
        this.requestRestart()
      },
      handleConnectionOpen: function() {
        // console.log('connection opened');
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
      requestRevealMultiple: function(points) {
        b.send({
          type: 'reveal_multiple',
          data: {
            points: points,
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
      requestRestart: function() {
        b.send({
          type: 'restart',
          data: {
            w: parseInt(this.w),
            h: parseInt(this.h),
            mines_total: parseInt(this.minesTotal),
          },
        });
      },
      handleMessage: function(message) {
        if (message.type === 'game_change') {
          // console.log('game changed');
          this.map = message.data;
        }
      }
    },
    mounted: function() {
      // console.log('component mounted');
      this.connect();
    },
  })

  $(document).mouseup(function(){
    setTimeout(function() {
      $('.mousedown').removeClass('mousedown')
    }, 100)
  });

  // debug
  window.b = b
  window.vm = vm
})()
