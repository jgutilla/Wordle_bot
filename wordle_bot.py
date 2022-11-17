from wordle_class import wordle
import utils
import random
import copy

with open('result.txt', 'w') as f:
        f.write(f"{utils.SELECTED_LINE}\n")

def try_to_win(game, guess, words_file, second_guess_list, second_guess=None):
    rounds = 1
    while True:
        print(len(words_file))
        if rounds == 2 and len(words_file) > 20:
            if second_guess:
                guess = second_guess
            else:
                guess = utils.choose_second_guess(guess, second_guess_list, words_file)
        if rounds > 6:
            with open('result.txt', 'a') as f:
                f.write("X/6" + "\n")
            with open('failed_words.txt', 'a') as k:
                k.write(f"{game.solution}\n")
            print("Failed to solve in 6 rounds or fewer.")
            return 7
        else:
            print(guess)
        if guess == game.solution:
            print({1: 'G', 2: 'G', 3: 'G', 4: 'G', 5: 'G'})
            with open('result.txt', 'a') as f:
                f.write("🟩🟩🟩🟩🟩" + "\n")
                f.write(f"{rounds}/6" + "\n")
            with open('solved_metrics.txt', 'a') as v:
                v.write(f"{rounds}:{len(words_file)}" + "\n")
            print(f"Solved in {rounds} rounds!")
            if rounds == 6:
                with open('6_round_words.txt', 'a') as g:
                    g.write(f"{game.solution}\n")
            return rounds
        else:
            # Always remove pre if present
            if guess in words_file:
                words_file.remove(guess)
            guess = utils.new_guess(game, guess, words_file, rounds)
            rounds = rounds + 1

def play_wordle(first_guess, solution, second_guess=None):
    words_file = open("words.txt", "r").read().split('\n')
    words_list = copy.deepcopy(words_file)
    second_guess_list = copy.deepcopy(words_file)
    print(f"Let's Play Wordle! Solution: {solution} ||| Starting word: {first_guess}")
    print("------------------------------------------------------------")
    game = wordle(solution=solution)
    with open('result.txt', 'a') as f:
        f.write(f"Wordle {game.number}\n")
    if second_guess:
        result = try_to_win(game, first_guess, words_list, second_guess_list, second_guess)
    else:
        result = try_to_win(game, first_guess, words_list, second_guess_list)
    return result

def play_once(first_guess, solution, second_guess):
    play_wordle(first_guess=first_guess, solution=solution, second_guess=second_guess)
    art = open("art.txt", "r").read()
    with open('result.txt', 'a') as f:
        f.write(f"\n\n{art}\n\n\n")

def play_100_rounds(first_guess, second_guess):
    result = 0
    answers_file = open("past_answers.txt", "r").read().split(' ')
    answers_list = copy.deepcopy(answers_file)
    #first_guess = random.choice(words_list)
    x = 1
    while x < 100:
        print(f"Cycle: {x}\n")
        solution_upper = random.choice(answers_list)
        solution = solution_upper.lower()
        try:
            result += play_wordle(first_guess=first_guess, solution=solution, second_guess=second_guess)
            x = x + 1
        except Exception as e:
            with open('efficiency_testing.txt', 'a') as e:
                e.write(f"{first_guess}:{second_guess}. Score: {result/x}\n")
            continue
    with open('efficiency_testing.txt', 'a') as e:
        e.write(f"{first_guess}:{second_guess}. Score: {result/x}\n")

def play_all_rounds(first_guess, second_guess):
    result = 0
    answers_file = open("past_answers.txt", "r").read().split(' ')
    with open('6_round_words.txt', 'w') as f:
        f.write("")
    with open('failed_words.txt', 'w') as f:
            f.write("")
    with open('guessed_words.txt', 'w') as f:
            f.write("")
    with open('solved_metrics.txt', 'w') as f:
            f.write("")
    answers_list = copy.deepcopy(answers_file)
    x = 1
    for solution in answers_list:
        print(f"Cycle: {x}\n")
        solution = solution.lower()
        try:
            result += play_wordle(first_guess=first_guess, solution=solution, second_guess=second_guess)
            x = x + 1
        except Exception as e:
            print(e)
            continue
    with open('efficiency_testing.txt', 'a') as e:
        e.write(f"REGRESSION RUN::: {first_guess}:{second_guess}. Score: {result/x}\n")

def replay_all_6_round_words(first_guess, second_guess):
    result = 0
    answers_file = open("6_round_words.txt", "r").read().split('\n')
    with open('6_round_words.txt', 'w') as f:
        f.write("")
    with open('guessed_words.txt', 'w') as f:
            f.write("")
    with open('solved_metrics.txt', 'w') as f:
            f.write("")
    answers_list = copy.deepcopy(answers_file)
    with open('6_round_words.txt', 'w') as y:
        y.write("")
    x = 1
    for solution in answers_list:
        print(f"Cycle: {x}\n")
        solution = solution.lower()
        try:
            result += play_wordle(first_guess=first_guess, solution=solution, second_guess=second_guess)
            x = x + 1
        except Exception as e:
            print(e)
            continue
def replay_all_failed_words(first_guess, second_guess):
    result = 0
    answers_file = open("failed_words.txt", "r").read().split('\n')
    answers_list = copy.deepcopy(answers_file)
    with open('failed_words.txt', 'w') as f:
        f.write("")
    with open('guessed_words.txt', 'w') as f:
            f.write("")
    with open('solved_metrics.txt', 'w') as f:
            f.write("")
    x = 1
    for solution in answers_list:
        print(f"Cycle: {x}\n")
        solution = solution.lower()
        try:
            result += play_wordle(first_guess=first_guess, solution=solution, second_guess=second_guess)
            x = x + 1
        except Exception as e:
            print(e)
            continue

play_all_rounds(first_guess="crane", second_guess="slipt")
#play_all_rounds(first_guess="tronc", second_guess="aisle")
#play_all_rounds(first_guess="salet", second_guess="crony")
#play_all_rounds(first_guess="taler", second_guess="coins")

#replay_all_6_round_words(first_guess="crane", second_guess="slipt")
#replay_all_failed_words(first_guess="crane", second_guess="slipt")


#play_once(first_guess="crane", second_guess="slipt", solution="there")