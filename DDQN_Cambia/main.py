import numpy as np
import time 
from DuelingDDQN.DuelingDDQN import Agent
from environment import Environment
from DuelingDDQN.utils import plot_learning_curve
from DuelingDDQN.utils import plot_learning_curve_ro
import os


def play_game():
    env = Environment()
    agent = Agent(gamma=0.99, epsilon=0.01, lr=5e-4, n_actions=5, input_dims=[11], mem_size=1000000, batch_size=64,
                eps_min=0.01, eps_dec=5e-6, replace=1000, chkpt_dir='DuelingDDQN/tmp/dueling_ddqn')
    agent.load_models()
    observation = env.reset()
    done = False
    print("Your two cards are {} and {}".format(env.masterBoard[6], env.masterBoard[7]))
    while not done: 
        print("The master board is: ", env.masterBoard)
        print(observation)
        action = agent.choose_action(observation)
        observation_, reward, done = env.step(action)
        # agent.remember(observation, action, reward, observation_, done)
        # agent.learn()
        observation = observation_
    print("The final board is ", env.masterBoard)


if __name__ == '__main__':
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    play_game()
    trial_number = input('Input the trial number: ')
    env = Environment()
    
    start_time = time.time()
    num_games = 30000
    load_checkpoint = True

    agent = Agent(gamma=0.99, epsilon=0.5, lr=5e-4, n_actions=5, input_dims=[11], mem_size=1000000, batch_size=64,
                eps_min=0.01, eps_dec=5e-6, replace=1000, chkpt_dir='DuelingDDQN/tmp/dueling_ddqn')

    if (load_checkpoint):
        agent.load_models()


    filename = 'Value'
    figure_file = 'DuelingDDQN/plots/' + 'V' + str(trial_number) + '-' + 'Score_' + filename + '.png'
    figure_file0 = 'DuelingDDQN/plots/' + 'V' + str(trial_number) + '-' + 'Action_' + filename + '.png'
    figure_file1 = 'DuelingDDQN/plots/' + 'V' + str(trial_number) + '-' + 'Epsilon_' + filename + '.png'
    figure_file2 = 'DuelingDDQN/plots/' + 'V' + str(trial_number) + '-' + 'Loss_' + filename + '.png'
    figure_file3 = 'DuelingDDQN/plots/' + 'V' + str(trial_number) + '-' + 'Last100Actions_' + filename + '.png'
    figure_file4 = 'DuelingDDQN/plots/' + 'V' + str(trial_number) + '-' + 'Num_Actions' + '.png'
    figure_file5 = 'DuelingDDQN/plots/' + 'V' + str(trial_number) + '-' + 'AverageScore_' + filename + '.png'

    # figure_file5 = 'DuelingDDQN/plots/' + 'V' + str(trial_number) + '-' + 'Oppo_Action_' + filename + '.png'
    # figure_file6 = 'DuelingDDQN/plots/' + 'V' + str(trial_number) + '-' + 'Last100OppoActions_' + filename + '.png'
    # figure_file7 = 'DuelingDDQN/plots/' + 'V' + str(trial_number) + '-' + 'Oppo_CoopProb_' + filename + '.png'
    figure_file6 = 'DuelingDDQN/plots/' + 'V' + str(trial_number) + '-' + 'Wins_' + filename + '.png'
    figure_file7 = 'DuelingDDQN/plots/' + 'V' + str(trial_number) + '-' + 'WinPercentage_' + filename + '.png'
    figure_file8 = 'DuelingDDQN/plots/' + 'V' + str(trial_number) + '-' + 'Last100WinPercentage_' + filename + '.png'
    figure_file9 = 'DuelingDDQN/plots/' + 'V' + str(trial_number) + '-' + 'Num_Moves' + '.png'
    # figure_file9 = 'DuelingDDQN/plots/' + 'V' + str(trial_number) + '-' + 'ActualGameScore_' + filename + '.png'



    score_history = []
    average_score_history = []
    eps_history = []
    action_history = []
    loss_history = []
    last_10_episodes = []
    num_actions = []
    last_100_games = []

    for i in range(num_games):
        done = False
        score = 0
        observation = env.reset()
        action_counter = 0

        while not done: 
            # print(observation)
            action = agent.choose_action(observation)
            action_history.append(action)

            observation_, reward, done = env.step(action)

            agent.remember(observation, action, reward, observation_, done)
            loss = agent.learn()
            if loss != False:
                loss_history.append(loss)

            score += reward
            observation = observation_
            action_counter += 1

        if i >= num_games - 10:
            your_actions = action_history[-action_counter:] + [" Win ", bool(env.win_history[-1])]
            # oppo_actions = np.array(env.oppo_actions[-action_counter:])
            # overall = np.stack((your_actions, oppo_actions))
            last_10_episodes.append(your_actions)
        score_history.append(score)
        avg_score = np.mean(score_history[-100:])
        average_score_history.append(avg_score)
        last_100_games.append(np.mean(env.win_history[-100:]))
        num_actions.append(action_counter)
        print('episode ', i, 'score %.2f' % score,
                'trailing 100 games avg %.3f' % avg_score, 'action counter %.3f' % action_counter)
        print('----------------------')
        if (i > 10 and i % 100 == 99):
            agent.save_models()

        eps_history.append(agent.epsilon)

        if (i % 25 == 0 and i > 25):
                x = [i+1 for i in range(len(score_history))]
                plot_learning_curve_ro(x, score_history, figure_file)
                plot_learning_curve(x, eps_history, figure_file1)
                # plot_learning_curve_ro(x, env.actual_score_history, figure_file9)

                x = [i+1 for i in range(len(average_score_history))]
                plot_learning_curve(x, average_score_history, figure_file5)

                x = [i+1 for i in range(len(num_actions))]
                plot_learning_curve_ro(x, num_actions, figure_file4)
                x = [i+1 for i in range(len(env.episode_lengths))]
                plot_learning_curve_ro(x, env.episode_lengths, figure_file9)
                x = [i+1 for i in range(len(action_history))]
                plot_learning_curve_ro(x, action_history, figure_file0)

                # x = [i+1 for i in range(len(env.oppo_actions))]
                # plot_learning_curve_ro(x, env.oppo_actions, figure_file5)
                # x = [i+1 for i in range(len(env.oppo_probs))]
                # plot_learning_curve_ro(x, env.oppo_probs, figure_file7)
                x = [i+1 for i in range(len(loss_history))]
                plot_learning_curve(x, loss_history, figure_file2)

                x = [i+1 for i in range(len(env.win_history))]
                plot_learning_curve_ro(x, env.win_history, figure_file6)
                x = [i+1 for i in range(len(env.win_percentage))]
                plot_learning_curve(x, env.win_percentage, figure_file7)
                x = [i+1 for i in range(len(last_100_games))]
                plot_learning_curve(x, last_100_games, figure_file8)


    x = [i+1 for i in range(100)]
    plot_learning_curve_ro(x, action_history[-100:], figure_file3)
    # plot_learning_curve_ro(x, env.oppo_actions[-100:], figure_file6)
    end_time = time.time()
    print("The last 10 episodes were \n")
    for i in range(10):
        print(last_10_episodes[i], '\n')
    print("The amount of time for {} actions is {}".format(len(action_history), end_time - start_time))
