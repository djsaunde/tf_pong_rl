# Game-making tutorial from https://www.youtube.com/watch?v=C6jJg9Zan7w.

import os
import turtle


def main():
    window = turtle.Screen()
    window.title('Pong')
    window.bgcolor('black')
    window.setup(width=800, height=600)
    window.tracer(0)

    # Paddle A
    paddle_a = turtle.Turtle()
    paddle_a.speed(0)  # Speed of animation.
    paddle_a.shape('square')
    paddle_a.color('white')
    paddle_a.shapesize(stretch_wid=5, stretch_len=1)
    paddle_a.penup()
    paddle_a.goto(-350, 0)

    # Paddle B
    paddle_b = turtle.Turtle()
    paddle_b.speed(0)  # Speed of animation.
    paddle_b.shape('square')
    paddle_b.color('white')
    paddle_b.shapesize(stretch_wid=5, stretch_len=1)
    paddle_b.penup()
    paddle_b.goto(350, 0)

    # Ball
    ball = turtle.Turtle()
    ball.speed(0)  # Speed of animation.
    ball.shape('square')
    ball.color('white')
    ball.penup()
    ball.goto(0, 0)
    ball.dx = .075
    ball.dy = .075

    # Pen
    pen = turtle.Turtle()
    pen.speed(0)
    pen.color('white')
    pen.penup()
    pen.hideturtle()
    pen.goto(0, 260)
    pen.write('Player A: 0, Player B: 0', align='center', font=('Courier', 24, 'normal'))

    # Score
    score = [0, 0]

    # Paddle movement functions
    def paddle_a_up():
        if paddle_a.ycor() < 250:
            paddle_a.sety(paddle_a.ycor() + 20)


    def paddle_a_down():
        if paddle_a.ycor() > -250:
            paddle_a.sety(paddle_a.ycor() - 20)


    def paddle_b_up():
        if paddle_b.ycor() < 250:
            paddle_b.sety(paddle_b.ycor() + 20)


    def paddle_b_down():
        if paddle_b.ycor() > -250:
            paddle_b.sety(paddle_b.ycor() - 20)


    # Keyboard bindings
    window.listen()
    window.onkeypress(paddle_a_up, 'w')
    window.onkeypress(paddle_a_down, 's')
    window.onkeypress(paddle_b_up, 'Up')
    window.onkeypress(paddle_b_down, 'Down')

    # Main game loop.
    while True:
        window.update()

        # Move the ball
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Boundary conditions
        if ball.ycor() > 290:
            ball.sety(290)
            ball.dy *= -1
            os.system('aplay bounce.wav &')

        elif ball.ycor() < -290:
            ball.sety(-290)
            ball.dy *= -1
            os.system('aplay bounce.wav &')

        # Termination conditions
        if abs(ball.xcor()) > 390:
            if ball.xcor() > 390:
                score[0] += 1
            else:
                score[1] += 1

            ball.goto(0, 0)
            ball.dx *= -1

            pen.clear()
            pen.write(f'Player A: {score[0]}, Player B: {score[1]}', align='center', font=('Courier', 24, 'normal'))

        if 340 < ball.xcor() < 350 and paddle_b.ycor() - 40 < ball.ycor() < paddle_b.ycor() + 40:
            ball.setx(340)
            ball.dx *= -1
            os.system('aplay bounce.wav &')

        elif -350 < ball.xcor() < -340 and paddle_a.ycor() - 40 < ball.ycor() < paddle_a.ycor() + 40:
            ball.setx(-340)
            ball.dx *= -1
            os.system('aplay bounce.wav &')


if __name__ == '__main__':
    main()
