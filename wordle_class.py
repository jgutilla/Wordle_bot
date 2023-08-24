from datetime import datetime, date

class wordle:
    def __init__(self, solution):
        self.solution = solution
        self.number = self.set_wordle_number()

    def set_solution(self, solution):
        self.solution = solution

    def set_wordle_number(self):
        fixed_date = datetime.strptime("2022/11/09", "%Y/%m/%d")
        today_date = datetime.strptime(str(date.today()).replace("-", "/"), "%Y/%m/%d")
        date_difference = abs((today_date - fixed_date).days)
        number = 508 + date_difference
        return number

    def slot_is_empty(self, key):
        return self.return_dict[key] is "E"


    def slot_is_y(self, key):
        return self.return_dict[key] is "T"


    def check_occurances(self, word, check_letter):
        occurances = 0
        for letter in word:
            if check_letter == letter:
                occurances = occurances + 1
        return occurances

    def strip_dupes_from_guess(self, guess):
        for letter in guess:
            occurances = guess.count(letter)
            if occurances > 1:
                guess = guess.replace(letter, "", occurances-1)
        return guess

    def guess(self, guess):
        self.return_dict = {1: 'E', 2: 'E', 3: 'E', 4: 'E', 5: 'E'}
        guess_index = solution_index = 0
        for guess_letter in guess:
            guess_index = guess_index + 1
            for solution_letter in self.solution:
                solution_index = solution_index + 1
                # First check if the letter is in the right spot.
                matching_index = solution_index == guess_index
                matching_letter = solution_letter == guess_letter
                # Right letter, right spot
                if matching_letter and matching_index:
                        self.return_dict[guess_index] = "G"
                # Right letter, wrong spot.
                elif matching_letter and not matching_index:
                    if self.slot_is_empty(guess_index):
                        self.return_dict[guess_index] = "Y"

            solution_index = 0
        guess_no_repeats=""
        for char in guess:
            if char not in guess_no_repeats:
                guess_no_repeats=guess_no_repeats+char

        dupe_letter_list = []
        dupes = 0
        for solution_char in self.solution:
            for guess_char in guess:
                if guess_char == solution_char:
                    if dupes > 0:
                        dupe_letter_list.append(guess_char)
                    else:
                        dupes = dupes + 1
            dupes = 0

        index_strip = 0
        dupes_removed = []
        for letter in guess:
            index_strip = index_strip + 1
            guess_occurances = self.check_occurances(guess, letter)
            solution_occurances = self.check_occurances(self.solution, letter)
            excess_occurances = guess_occurances - solution_occurances
            if letter in dupe_letter_list and letter not in dupes_removed:
                if self.return_dict[index_strip] is "Y" and excess_occurances > 0:
                    excess_occurances = excess_occurances - 1
                    self.return_dict[index_strip] = "E"
                    if excess_occurances == 0:
                        dupes_removed.append(letter)
        return self.return_dict, dupe_letter_list