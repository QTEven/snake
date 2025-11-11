# 简单 Python 贪吃蛇游戏 (tkinter)

这是一个使用 `tkinter` 实现的轻量级贪吃蛇小游戏，单文件 `snake.py`，适合在 Windows 的 Python 环境下运行。

要点：
- 使用 `tkinter.Canvas` 绘制网格、蛇与食物
- 键盘方向键控制（Up/Down/Left/Right），按 `R` 重启
- 吃到食物得分 +10，每满 50 分会稍微加速

运行要求：
- Python 3.x
- Windows 上通常自带 `tkinter`，若缺失请安装 Python 的 tcl/tk 支持

在 PowerShell 中运行：

```powershell
# 切换到项目目录
cd 
# 运行游戏
python .\snake.py
```

如果游戏窗口未出现或报错，请确认 Python 能导入 tkinter：

```powershell
python -c "import tkinter; print('tkinter OK')"
```

后续改进建议：
- 添加音效和菜单
- 支持触控/鼠标控制或更平滑的动画
- 保存最高分到本地文件

请运行试用并告诉我你想增加哪些功能（例如：关卡、音效、加分道具等）。

---

## 浏览器可玩版本（PyScript）

我另外添加了一个基于 PyScript 的浏览器可玩版本，文件：`index.html`。

本地运行（推荐使用静态服务器）：

```powershell
cd 。。。
python -m http.server 8000
# 然后在浏览器打开 http://localhost:8000/index.html
```

部署到 GitHub Pages：把项目推到 GitHub，启用 Pages 即可直接通过链接分享给他人。


注意：PyScript 首次加载需要从网络下载 WebAssembly 与依赖，加载时间会比本地 Python 稍长。
