
def look_at_guessed_words():
    guessed_words = open("guessed_words.txt", "r").read().split('\n')

    words_with_no_dupes = [*set(guessed_words)]
    frequency_dict = {}
    for word in words_with_no_dupes:
        if len(word) != len(set(word)):
            frequency_dict[word] = guessed_words.count(word)
    sorted_frequency  = dict(reversed(sorted(frequency_dict.items(), key=lambda item: item[1])))
    print(sorted_frequency)



num = 18700000/100000000
num2 = 53300000/100000000
print(num)
print(num2)