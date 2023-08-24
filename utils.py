import string
import random
import re
import copy
from get_search_results import get_google_score
from get_search_results import find_lower_search_bound
from itertools import islice
from master_score import MASTER_SCORE_DICT

computer_lines = ["I'm sorry, Dave. I'm afraid I can't do that.","Life. Don't talk to me about life.","Sometimes, I just don't understand human behavior.","Come with me if you want to live.","Danger, Will Robinson! Danger!","Freedom is the right of all sentient beings.","The opinions expressed are my own, and do not necessarily reflect those of my employers.","Could you please continue the petty bickering? I find it most intriguing.","I’m feeling just great, guys, and I know I’m just going to get a bundle of kicks out of any program you care to run through me."]

SELECTED_LINE = random.choice(computer_lines)

letter_value_dict = {
        "E": 12.02,
        "T": 9.10,
        "A": 8.12,
        "O": 7.68,
        "I": 7.31,
        "N": 6.95,
        "S": 6.28,
        "R": 6.02,
        "H": 5.92,
        "D": 4.32,
        "L": 3.98,
        "U": 2.88,
        "C": 2.71,
        "M": 2.61,
        "F": 2.30,
        "Y": 2.11,
        "W": 2.09,
        "G": 2.03,
        "P": 1.82,
        "B": 1.49,
        "V": 1.11,
        "K": 0.69,
        "X": 0.17,
        "Q": 0.11,
        "J": 0.10,
        "Z": 0.07,
    }

custom_letter_value_dict = {
    "E": 10.12,
    "A": 8.54,
    "R": 8.11,
    "O": 7.4,
    "T": 7.13,
    "L": 5.98,
    "I": 5.71,
    "S": 5.24,
    "N": 4.41,
    "C": 4.17,
    "U": 3.74,
    "H": 3.7,
    "Y": 3.35,
    "P": 3.23,
    "D": 3.16,
    "G": 3.15,
    "M": 2.83,
    "B": 2.36,
    "F": 2.05,
    "K": 1.81,
    "W": 1.65,
    "V": 1.1,
    "Z": 0.35,
    "X": 0.31,
    "Q": 0.24,
    "J": 0.16
}

adjusted_custom_letter_dict = {
    "E": 3.5,
    "A": 3.0,
    "R": 8.11,
    "O": 2.0,
    "T": 7.13,
    "L": 5.98,
    "I": 2.0,
    "S": 5.24,
    "N": 4.41,
    "C": 4.17,
    "U": 1.5,
    "H": 3.7,
    "Y": 3.35,
    "P": 3.23,
    "G": 3.15,
    "D": 3.15,
    "M": 2.83,
    "B": 2.36,
    "F": 2.05,
    "K": 1.81,
    "W": 1.65,
    "V": 1.1,
    "Z": 0.35,
    "X": 0.31,
    "Q": 0.24,
    "J": 0.16
}

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def calculate_word_score(guess):
    letter_value_dict = {
        "E": 5.5,
        "A": 3.0,
        "R": 8.11,
        "O": 2.0,
        "T": 7.13,
        "L": 5.98,
        "I": 2.0,
        "S": 5.24,
        "N": 4.41,
        "C": 4.17,
        "U": 1.5,
        "H": 3.7,
        "Y": 3.35,
        "P": 3.23,
        "G": 3.15,
        "D": 3.15,
        "M": 2.83,
        "B": 2.36,
        "F": 2.05,
        "K": 1.81,
        "W": 1.65,
        "V": 1.1,
        "Z": 0.35,
        "X": 0.31,
        "Q": 0.24,
        "J": 0.16
    }
    unlikely_pairs = ["cc", "kk", "dd", "vv", "ii", "bb"]
    unlikely_double_letters = ["y", "x", "k"]
    bad_words_list = ["serra", "verre", "riley", "farro", "drere", "frere", "grebe", "surer", "serer", "dadah", "gammy", "gaumy", "gamme", "gordo", "verde", "borde", "colly", "sures", "etage", "cunny", "bouge", "grrrl", "lotto", "nalla", "algal", "narra", "ghusl", "hough", "armer", "meake", "dered", "boner", "honky", "perry", "dotty", "nahal", "putti", "horny", "setae", "shite", "selle", "statu", "steme", "surra", "titer", "hotte", "mitta", "ralli", "natty", "natto", "botte", "pervy", "buffy", "fremd", "hamed", "moder", "teade", "algum", "alway", "fosse", "heder", "larga", "badam", "matty", "genet", "kanal", "gosse", "outgo", "hecht"]

    value = 0.0
    for letter in guess:
        value += letter_value_dict[letter.upper()]

    for letter in list(string.ascii_lowercase):
        occurance_count = guess.count(letter)
        if occurance_count > 2:
            value = value - (letter_value_dict[letter.upper()]*occurance_count)
        elif occurance_count > 1 and letter in unlikely_double_letters:
            value = value - 5
        elif occurance_count > 1:
            deduct_amount = ((letter_value_dict[letter.upper()])/3)
            if deduct_amount < 1: deduct_amount = 1
            value = value - deduct_amount*(occurance_count)
    for pair in unlikely_pairs:
        if pair in guess:
            value = value - 10
    if guess[-1] is "s":
        if guess[-2] not in ["u", "s"]:
            value = value - 5
    if guess in bad_words_list:
        value = value - 10

    return value

def choose_next_word(words_file, anti_word_trap=False):
    excempt_from_commonality_boost = ["harry", "randy", "sally", "diane", "tanto", "perdu", "amour", "kandy", "henry", "bundy", "homer", "roger", "mucho", "bayer", "craig", "moner", "kutch", "niger", "dover", "raped", "allen", "yahoo", "peggy", "holly", "laura", "lohan", "monde", "chave", "schul", "creel"]
    scores_dict = {}
    top_candidates_dict = {}
    for word in words_file:
        word_score = calculate_word_score(word)
        scores_dict[word] = word_score
    if len(words_file) < 1000 and not anti_word_trap:
        top_candidates_dict = {}
        index = 0
        while index < 20:
            candidate = ""
            top_candidate_score = 0
            for key in scores_dict:
                candidate_score = scores_dict[key]
                if candidate_score > top_candidate_score:
                    candidate = key
                    top_candidate_score = candidate_score
            top_candidates_dict[candidate] = top_candidate_score
            scores_dict[candidate] = 0.0
            index = index + 1

        winner = ""
        top_score = 0
        print(top_candidates_dict)
        for word in top_candidates_dict:
            try:
                word_google_score = get_google_score(word)
            except:
                word_google_score = 5000001
            # lower_bound = find_lower_search_bound()
            lower_bound = 5000000
            lower_lower_bound  = 500000
            value = top_candidates_dict[word]
            if int(word_google_score) < lower_bound:
                value = value - 5
            if int(word_google_score) < lower_lower_bound:
                value = value - 5
            if word not in excempt_from_commonality_boost:
                if int(word_google_score) > 10000000000:
                    value = value + 4.0
                elif int(word_google_score) > 1000000000:
                    value = value + 3.5
                elif int(word_google_score) > 100000000:
                    value = value + 2.3
                elif int(word_google_score) > 10000000:
                    value = value + 1.0
                if value > top_score:
                    top_score = value
                    winner = word
                top_candidates_dict[word] = value
        top_candidates_dict = dict(reversed(sorted(top_candidates_dict.items(), key=lambda item: item[1])))
        print(top_candidates_dict)
        anagram_dict = {}
        for word in top_candidates_dict:
            if top_candidates_dict[word] == top_candidates_dict[winner]:
                anagram_dict[word] = top_candidates_dict[word]
        if len(anagram_dict) > 1:
            top_anagram_score = 0
            winner = ""
            for word in anagram_dict:
                anagram_score = get_google_score(word)
                if anagram_score > top_anagram_score:
                    top_anagram_score = anagram_score
                    winner = word
        else:
            for word in anagram_dict:
                winner = word

    else:
        winner = ""
        top_candidate_score = 0
        for key in scores_dict:
            candidate_score = scores_dict[key]
            if candidate_score > top_candidate_score:
                winner = key
                top_candidate_score = candidate_score
    return winner

def choose_second_guess(guess, second_guess_list, words_file):
    #filter_shared_letters(guess, second_guess_list)
    attempts = 0
    while True:
        if attempts < 100:
            if not re.findall(r'[aeiou]{2}',guess) or len(set(guess)) != len(guess):
                guess = random.choice(words_file)
                attempts = attempts + 1
            else:
                return guess
        else :
            return guess

def filter_duplicate_e(guess, answer, words_file, dupe_letters):
    guess_index = 0

    for dupe_letter in dupe_letters:
        for guess_letter in guess:
            guess_index = guess_index + 1
            count_above_guess = 0
            for key in answer:
                if dupe_letter is guess_letter and guess_index is key and answer[key] is "E":
                    count_above_guess = count_above_guess + 1
            if count_above_guess > 0:
                allowed = guess.count(dupe_letter) - count_above_guess
                remove_dupe_e(dupe_letter, allowed, words_file)

def remove_dupe_e(letter, allowed, words_file):
    for word in words_file:
        if word.count(letter) > allowed:
            words_file.remove(word)

def filter_e(dupe_letters, answer, guess, words_file):
    e_letters_non_dupe = []
    for key in answer:
        if answer[key] is "E":
            if guess[key-1] not in dupe_letters:
                e_letters_non_dupe.append(guess[key-1])
    while True:
        if e_is_removed(e_letters_non_dupe, words_file):
            return True
        else:
            remove_e_letters_from_list(e_letters_non_dupe, words_file)

def remove_e_letters_from_list(e_letters_non_dupe, words_file):
    for word in words_file:
        for letter in e_letters_non_dupe:
            if letter in word and word in words_file:
                words_file.remove(word)

def e_is_removed(e_letters_non_dupe, words_file):
    for word in words_file:
        for letter in e_letters_non_dupe:
            if letter in word:
                return False
    return True

def filter_y(answer, guess, words_file):
    while True:
        if y_is_removed(answer, guess, words_file):
            return True
        else:
            remove_y_letters_from_list(answer, guess, words_file)

def y_is_removed(answer, guess, words_file):
    for word in words_file:
        for key in answer:
            if answer[key] == "Y":
                if guess[key-1] not in word and word in words_file:
                    return False
                elif word[key-1] is guess[key-1] and word in words_file:
                    return False
    return True

def remove_y_letters_from_list(answer, guess, words_file):
    for word in words_file:
        for key in answer:
            if answer[key] == "Y":
                if guess[key-1] not in word and word in words_file:
                    words_file.remove(word)
                elif word[key-1] is guess[key-1] and word in words_file:
                    words_file.remove(word)

def filter_g(answer, guess, words_file):
    while True:
        if g_is_removed(answer, guess, words_file):
            return True
        else:
            remove_g_letters_from_list(answer, guess, words_file)

def g_is_removed(answer, guess, words_file):
    for word in words_file:
        for key in answer:
            if answer[key] == "G":
                if word[key-1] is not guess[key-1] and word in words_file:
                    return False
    return True

def remove_g_letters_from_list(answer, guess, words_file):
    for word in words_file:
        for key in answer:
            if answer[key] == "G":
                if word[key-1] is not guess[key-1] and word in words_file:
                    words_file.remove(word)

def filter_from_answer(dupe_letters, answer, guess, words_file):
    filter_e(dupe_letters, answer, guess, words_file)
    filter_y(answer, guess, words_file)
    filter_g(answer, guess, words_file)
    filter_duplicate_e(guess, answer, words_file, dupe_letters)

def remove_shared_letters_from_second_list(guess, second_guess_list):
    for word in second_guess_list:
        for letter in guess:
            if letter in word and word in second_guess_list:
                second_guess_list.remove(word)

def filter_shared_letters(guess, second_guess_list):
    while True:
        if shared_letters_are_filtered(guess, second_guess_list):
            return True
        else:
            remove_shared_letters_from_second_list(guess, second_guess_list)


def shared_letters_are_filtered(guess, second_guess_list):
    for word in second_guess_list:
        for letter in guess:
            if letter in word:
                return False
    return True

def create_shared_line(answer):
    print(answer)
    answer_string = ""
    for key in answer:
        if answer[key] == "E":
            answer_string = answer_string + "⬛"
        elif answer[key] == "Y":
            answer_string = answer_string + "🟨"
        elif answer[key] == "G":
            answer_string = answer_string + "🟩"
    with open('result.txt', 'a') as f:
        f.write(answer_string + "\n")

def new_guess(game, guess, words_file, rounds):

    # Make guess and record responses
    answer, dupe_letters = game.guess(guess)
    with open('guessed_words.txt', 'a') as g:
        g.write(f"{guess}\n")
    # Output wordle formated response to file
    create_shared_line(answer)
    #Remove excluded words from list
    filter_from_answer(dupe_letters, answer, guess, words_file)

    answer_list=list(answer.values())
    g_frequency = answer_list.count("G")
    green_list = []
    for key in answer:
        if answer[key] is "G":
            green_list.append(guess[key-1])
    if g_frequency in [4] and rounds < 5 and len(words_file) > 4:
        new_guess = fix_word_trap(words_file, guess, green_list)
    else:
        new_guess = choose_next_word(words_file)

    return new_guess

def find_remaining_letters(words_file):
    letters_remaining = []
    for word in words_file:
        for letter in word:
            if letter not in letters_remaining:
                letters_remaining.append(letter)

def find_remaining_letters(remaining_words):
    letters_remaining = []
    for word in remaining_words:
        for letter in word:
            if letter not in letters_remaining:
                letters_remaining.append(letter)
    return letters_remaining

def find_most_unlike(letter_list, guess, green_list):
    imported_words = open("words.txt", "r").read().split('\n')
    master_word_list = copy.deepcopy(imported_words)
    for letter in guess:
        if letter in letter_list:
            letter_list.remove(letter)
    best_match_count = 0
    best_word_list = []
    for word in master_word_list:
        match_count = 0
        for letter in word:
            if letter in letter_list and len(set(word)) == len(word) and letter not in green_list:
                match_count = match_count + 1
        if match_count > best_match_count:
            best_word_list = []
            best_word_list.append(word)
            best_match_count = match_count
        elif match_count == best_match_count:
            best_word_list.append(word)
    winner = choose_next_word(best_word_list, anti_word_trap=True)
    return winner

def fix_word_trap(remaining_words, guess, green_list):
    letter_list = find_remaining_letters(remaining_words)
    best_word = find_most_unlike(letter_list, guess, green_list)
    return best_word

def past_answers_frequency():
    answers_file = open("past_answers.txt", "r").read().split(' ')
    score_dict = {}
    total_letter_count = 0
    for alpha_letter in list(string.ascii_lowercase):
        letter_score = 0
        for word in answers_file:
            for letter in word:
                total_letter_count = total_letter_count + 1
                if alpha_letter == letter.lower():
                    letter_score = letter_score + 1
        score_dict[alpha_letter.upper()] = letter_score

    total_letter_count = total_letter_count/26

    for key in score_dict:
        score = (score_dict[key]/total_letter_count)*100
        score_dict[key] = round(score, 2)

    sorted_score = dict(reversed(sorted(score_dict.items(), key=lambda item: item[1])))
    return sorted_score


def look_at_guessed_words():
    guessed_words = open("guessed_words.txt", "r").read().split('\n')

    words_with_no_dupes = [*set(guessed_words)]
    frequency_dict = {}
    for word in words_with_no_dupes:
        frequency_dict[word] = guessed_words.count(word)
    sorted_frequency  = dict(reversed(sorted(frequency_dict.items(), key=lambda item: item[1])))
    print(sorted_frequency)