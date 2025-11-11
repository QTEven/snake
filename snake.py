import tkinter as tk
import random

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
INITIAL_SPEED = 120  # 毫秒 per tick

class SnakeGame:
    def __init__(self, master):
        self.master = master
        master.title("贪吃蛇 (tkinter)")

        self.canvas = tk.Canvas(master, width=CELL_SIZE*GRID_WIDTH, height=CELL_SIZE*GRID_HEIGHT, bg="#111")
        self.canvas.pack()

        self.score = 0
        self.direction = 'Right'
        self.speed = INITIAL_SPEED
        self.running = False
        self.paused = False
        self.pause_text = None

        self.master.bind('<Key>', self.on_key)

        self.restart_button = tk.Button(master, text='开始/重启 (R)', command=self.restart)
        self.restart_button.pack(side='left')

        self.score_label = tk.Label(master, text=f'Score: {self.score}')
        self.score_label.pack(side='right')

        self.restart()

    def restart(self):
        self.canvas.delete('all')
        self.score = 0
        self.score_label.config(text=f'Score: {self.score}')
        self.direction = 'Right'
        self.speed = INITIAL_SPEED
        self.running = True
        # 取消暂停状态并移除暂停文本（如果有）
        self.paused = False
        if getattr(self, 'pause_text', None):
            try:
                self.canvas.delete(self.pause_text)
            except Exception:
                pass
            self.pause_text = None

        # 初始化蛇身体（列表 of (x,y)），(0,0) 左上角为 0,0
        start_x = GRID_WIDTH // 4
        start_y = GRID_HEIGHT // 2
        self.snake = [(start_x - i, start_y) for i in range(3)]

        self.place_food()
        self.draw()
        self.master.after(self.speed, self.game_tick)

    def place_food(self):
        empty = set((x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)) - set(self.snake)
        if not empty:
            # 棋盘已被占满，玩家赢了
            self.food = None
            self.running = False
            self.canvas.create_text(CELL_SIZE*GRID_WIDTH/2, CELL_SIZE*GRID_HEIGHT/2,
                                    text=f'你赢了！\n得分: {self.score}\n按 R 重玩',
                                    fill='white', font=('Helvetica', 24), justify='center')
        else:
            self.food = random.choice(list(empty))

    def on_key(self, event):
        key = event.keysym
        # 防止蛇倒退
        opposite = {'Left':'Right','Right':'Left','Up':'Down','Down':'Up'}
        if key in ('Left','Right','Up','Down'):
            if opposite.get(key) != self.direction:
                self.direction = key
        elif key == 'space':
            # 切换暂停/恢复
            if not self.running:
                return
            if not self.paused:
                self.paused = True
                # 在画布上显示暂停文字
                self.pause_text = self.canvas.create_text(CELL_SIZE*GRID_WIDTH/2,
                                                          CELL_SIZE*GRID_HEIGHT/2,
                                                          text='暂停\n按 Space 恢复',
                                                          fill='white', font=('Helvetica', 24), justify='center')
            else:
                # 恢复
                self.paused = False
                if getattr(self, 'pause_text', None):
                    try:
                        self.canvas.delete(self.pause_text)
                    except Exception:
                        pass
                    self.pause_text = None
                # 重新调度游戏循环
                self.master.after(self.speed, self.game_tick)
        elif key.lower() == 'r':
            self.restart()

    def game_tick(self):
        # 如果未运行或已暂停，跳过本次 tick
        if not self.running or self.paused:
            return

        head_x, head_y = self.snake[0]
        moves = {'Left':(-1,0),'Right':(1,0),'Up':(0,-1),'Down':(0,1)}
        dx, dy = moves[self.direction]
        new_head = (head_x + dx, head_y + dy)

        # 碰撞检测：墙或自身
        x, y = new_head
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT or new_head in self.snake:
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 10
            self.score_label.config(text=f'Score: {self.score}')
            # 每吃一定分数加速
            if self.score % 50 == 0 and self.speed > 40:
                self.speed = int(self.speed * 0.9)
            self.place_food()
        else:
            self.snake.pop()

        self.draw()
        self.master.after(self.speed, self.game_tick)

    def draw_cell(self, pos, color):
        x, y = pos
        x1 = x * CELL_SIZE
        y1 = y * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        return self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)

    def draw(self):
        self.canvas.delete('all')
        # 画食物（如果存在）
        if self.food is not None:
            fx, fy = self.food
            self.draw_cell((fx,fy), '#e74c3c')
        # 画蛇头
        hx, hy = self.snake[0]
        self.draw_cell((hx,hy), '#2ecc71')
        # 画蛇身
        for segment in self.snake[1:]:
            self.draw_cell(segment, '#27ae60')

    def game_over(self):
        self.running = False
        self.canvas.create_text(CELL_SIZE*GRID_WIDTH/2, CELL_SIZE*GRID_HEIGHT/2, text=f'游戏结束\n得分: {self.score}\n按 R 重启', fill='white', font=('Helvetica', 24), justify='center')

if __name__ == '__main__':
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
