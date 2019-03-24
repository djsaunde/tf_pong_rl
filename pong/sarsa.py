# Game-making tutorial from https://www.youtube.com/watch?v=C6jJg9Zan7w.

import os
import turtle
import numpy as np
import tensorflow as tf

from pong.qvalue import QValue

tf.enable_eager_execution()


def main():
    # Hyper-parameters
    epsilon = 0.1
    alpha = 0.01
    gamma = 0.99
    episodes = 10000

    # Optimization
    optimizer = tf.train.AdamOptimizer(learning_rate=alpha)

    # Game screen
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

    agent_a = QValue()

    # Paddle B
    paddle_b = turtle.Turtle()
    paddle_b.speed(0)  # Speed of animation.
    paddle_b.shape('square')
    paddle_b.color('white')
    paddle_b.shapesize(stretch_wid=5, stretch_len=1)
    paddle_b.penup()
    paddle_b.goto(350, 0)

    agent_b = QValue()

    # Ball
    ball = turtle.Turtle()
    ball.speed(0)  # Speed of animation.
    ball.shape('square')
    ball.color('white')
    ball.penup()
    ball.goto(0, np.random.uniform(-250, 250))
    ball.dx = 2
    ball.dy = 2

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
            paddle_a.sety(paddle_a.ycor() + 10)

    def paddle_a_down():
        if paddle_a.ycor() > -250:
            paddle_a.sety(paddle_a.ycor() - 10)

    def paddle_b_up():
        if paddle_b.ycor() < 250:
            paddle_b.sety(paddle_b.ycor() + 10)

    def paddle_b_down():
        if paddle_b.ycor() > -250:
            paddle_b.sety(paddle_b.ycor() - 10)

    # Main game loop.
    for i in range(episodes):
        # Initial states and actions.
        state_a = np.array(
            [ball.xcor() / 400., ball.ycor() / 300., paddle_a.ycor() / 300.], dtype=np.float32
        )
        state_b = np.array(
            [ball.xcor() / 400., ball.ycor() / 300., paddle_b.ycor() / 300.], dtype=np.float32
        )

        inputs_a = tf.concat(
            [tf.stack([state_a] * 3), tf.eye(3)], axis=1
        )
        inputs_b = tf.concat(
            [tf.stack([state_b] * 3), tf.eye(3)], axis=1
        )

        value_a_ = agent_a(inputs=inputs_a)
        value_b_ = agent_b(inputs=inputs_b)

        action_a = np.random.choice(range(3)) if np.random.uniform() < epsilon else tf.argmax(value_a_, axis=0)
        action_b = np.random.choice(range(3)) if np.random.uniform() < epsilon else tf.argmax(value_b_, axis=0)

        inputs_a = tf.concat([state_a, tf.one_hot(action_a, depth=3)], axis=0)
        inputs_b = tf.concat([state_b, tf.one_hot(action_b, depth=3)], axis=0)

        with tf.GradientTape() as tape_a:
            value_a = agent_a(inputs=inputs_a[None, ...])
        with tf.GradientTape() as tape_b:
            value_b = agent_b(inputs=inputs_b[None, ...])

        grads_a = tape_a.gradient(value_a, agent_a.trainable_variables)
        grads_b = tape_b.gradient(value_b, agent_b.trainable_variables)

        # Select agents' actions epsilon-greedily.
        if np.random.uniform(0, 1) < epsilon:
            action_a = np.random.choice(range(3))
        else:
            action_a = np.argmax(value_a)

        if np.random.uniform(0, 1) < epsilon:
            action_b = np.random.choice(range(3))
        else:
            action_b = np.argmax(value_b)

        done = False
        j = 0
        while not done:
            j += 1
            window.update()

            if action_a == 1:
                paddle_a_down()
            elif action_a == 2:
                paddle_a_up()

            if action_b == 1:
                paddle_b_down()
            elif action_b == 2:
                paddle_b_up()

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

            # Next state and action
            next_state_a = np.array(
                [ball.xcor() / 400., ball.ycor() / 300., paddle_a.ycor() / 300.], dtype=np.float32
            )
            next_state_b = np.array(
                [ball.xcor() / 400., ball.ycor() / 300., paddle_b.ycor() / 300.], dtype=np.float32
            )

            inputs_a = tf.concat(
                [tf.stack([state_a] * 3), tf.eye(3)], axis=1
            )
            inputs_b = tf.concat(
                [tf.stack([state_b] * 3), tf.eye(3)], axis=1
            )

            value_a_ = agent_a(inputs=inputs_a)
            value_b_ = agent_b(inputs=inputs_b)

            action_a = np.random.choice(range(3)) if np.random.uniform() < epsilon else tf.argmax(value_a_)
            action_b = np.random.choice(range(3)) if np.random.uniform() < epsilon else tf.argmax(value_b_)

            inputs_a = tf.concat([state_a, tf.one_hot(action_a, depth=3)], axis=0)
            inputs_b = tf.concat([state_b, tf.one_hot(action_b, depth=3)], axis=0)

            with tf.GradientTape() as tape_a:
                next_value_a = agent_a(inputs=inputs_a[None, ...])
            with tf.GradientTape() as tape_b:
                next_value_b = agent_b(inputs=inputs_b[None, ...])

            next_grads_a = tape_a.gradient(next_value_a, agent_a.trainable_variables)
            next_grads_b = tape_b.gradient(next_value_b, agent_b.trainable_variables)

            # Select agents' actions epsilon-greedily.
            if np.random.uniform(0, 1) < epsilon:
                next_action_a = np.random.choice(range(3))
            else:
                next_action_a = np.argmax(value_a)

            if np.random.uniform(0, 1) < epsilon:
                next_action_b = np.random.choice(range(3))
            else:
                next_action_b = np.argmax(value_b)

            # Termination conditions
            if abs(ball.xcor()) > 390:
                if ball.xcor() > 390:
                    score[0] += 1
                    reward_a = 1
                    reward_b = -1
                else:
                    score[1] += 1
                    reward_a = -1
                    reward_b = 1

                ball.goto(0, np.random.uniform(-250, 250))
                ball.dx *= -1

                pen.clear()
                pen.write(f'Player A: {score[0]}, Player B: {score[1]}', align='center', font=('Courier', 24, 'normal'))

                done = True

                td_error_a = reward_a - value_a
                td_error_b = reward_b - value_b

                optimizer.apply_gradients(
                    zip([td_error_a * grad for grad in grads_a], agent_a.trainable_variables)
                )
                optimizer.apply_gradients(
                    zip([td_error_b * grad for grad in grads_b], agent_b.trainable_variables)
                )
            else:
                reward_a = reward_b = 0

                td_error_a = reward_a + gamma * next_value_a - value_a
                td_error_b = reward_b + gamma * next_value_b - value_b

                optimizer.apply_gradients(
                    zip([td_error_a * grad for grad in grads_a], agent_a.trainable_variables)
                )
                optimizer.apply_gradients(
                    zip([td_error_b * grad for grad in grads_b], agent_b.trainable_variables)
                )

            if not done:
                if 340 < ball.xcor() < 350 and paddle_b.ycor() - 40 < ball.ycor() < paddle_b.ycor() + 40:
                    ball.setx(340)
                    ball.dx *= -1
                    os.system('aplay bounce.wav &')

                elif -350 < ball.xcor() < -340 and paddle_a.ycor() - 40 < ball.ycor() < paddle_a.ycor() + 40:
                    ball.setx(-340)
                    ball.dx *= -1
                    os.system('aplay bounce.wav &')

                state_a = next_state_a
                state_b = next_state_b
                action_a = next_action_a
                action_b = next_action_b
                grads_a = next_grads_a
                grads_b = next_grads_b

        print(f'Episode length: {j} steps.')


if __name__ == '__main__':
    main()
