const snake = new Vue({
    el: '#gameBar',
    data: {
        width: 40,
        height: 40,
        direction: 39, // 默认方向是右
        map: [],
        obstacle: [],
        food: [],
        snake: [],
        head: '',
        dead: false,
        game: {},
        out: false,
        pause: true
    },
    methods: {
        whatIsThis: function (item) {
            if (this.obstacle.indexOf(item) >= 0) {
                return 'obstacle'
            }
            if (this.food.indexOf(item) >= 0) {
                return 'snakeFood'
            }
            if (this.snake.indexOf(item) >= 0) {
                return item == this.head ? 'snakeHead' : 'snakeBody'
            }
        },
        gameStart: () => snake.game.start(),
        gamePause: () => snake.game.pause()
    },
    mounted: function () {
        this.game = new Snake(this)
    }
});
