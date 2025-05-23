from ursina import *

app = Ursina()
window.title = "Brick Breaker Game"
window.color = color.black

# Game state flags
game_started = False
game_over = False

# Paddle
paddle = Entity(model='cube', color=color.azure, scale=(2, 0.4, 0), position=(0, -4), collider='box', enabled=False)

# Ball
ball = Entity(model='sphere', color=color.white, scale=0.3, position=(0, -3.5), collider='box', enabled=False)
ball.velocity = Vec2(3, 4)

# Bricks
bricks = []
colors = [color.red, color.orange, color.green, color.yellow]

for y in range(4):
    for x in range(8):
        brick = Entity(
            model='cube',
            color=colors[y % len(colors)],
            scale=(1.6, 0.5, 0),
            position=(-6 + x * 1.7, 3 - y * 0.6),
            collider='box',
            enabled=False
        )
        bricks.append(brick)

# Score
score = 0
score_text = Text(text=f"Score: {score}", position=(-0.85, 0.45), scale=2, enabled=False)

# Game Over Text
game_over_text = Text(text="Game Over!", origin=(0, 0), scale=3, enabled=False)

# Start or restart game
def start_game():
    global game_started, game_over, score
    game_started = True
    game_over = False
    paddle.enabled = True
    ball.enabled = True
    score_text.enabled = True
    for brick in bricks:
        brick.enabled = True
    ball.position = (0, -3.5)
    ball.velocity = Vec2(3, 4)
    paddle.x = 0
    score = 0
    score_text.text = f"Score: {score}"
    game_over_text.enabled = False
    play_button.enabled = False
    play_again_button.enabled = False

# Play Game button
play_button = Button(text="Play Game", scale=(0.3, 0.1), position=(0, 0), on_click=start_game)

# Play Again button
play_again_button = Button(
    text="Play Again",
    scale=(0.3, 0.1),
    position=(0, -0.2),
    on_click=start_game,
    enabled=False
)

# Game loop
def update():
    global score, game_started, game_over

    if not game_started or game_over:
        return

    # Paddle movement
    if held_keys['left arrow']:
        paddle.x -= 5 * time.dt
    if held_keys['right arrow']:
        paddle.x += 5 * time.dt

    # Clamp paddle position
    paddle.x = clamp(paddle.x, -6.5, 6.5)

    # Move ball
    ball.x += ball.velocity.x * time.dt
    ball.y += ball.velocity.y * time.dt

    # Wall collisions
    if abs(ball.x) > 7:
        ball.velocity.x *= -1
    if ball.y > 5:
        ball.velocity.y *= -1

    # Bottom collision (Game Over)
    if ball.y < -5:
        ball.disable()
        game_over_text.enabled = True
        play_again_button.enabled = True
        game_over = True
        return

    # Paddle collision with dynamic bounce
    if ball.intersects(paddle).hit:
        offset = ball.x - paddle.x
        ball.velocity.y *= -1
        ball.velocity.x += offset * 5  # Add horizontal deflection
        ball.y = paddle.y + 0.3

        # Clamp ball speed
        ball.velocity.x = clamp(ball.velocity.x, -10, 10)
        ball.velocity.y = clamp(ball.velocity.y, -10, 10)

    # Brick collisions
    for brick in bricks:
        if brick.enabled and ball.intersects(brick).hit:
            ball.velocity.y *= -1
            brick.disable()
            score += 1
            score_text.text = f"Score: {score}"
            break

app.run()
