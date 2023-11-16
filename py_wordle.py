def generate_empty_score():
    score = {"correct": [None] * 5, "incorrect": [], "required": [], "banned": []}
    for i in range(5):
        score["incorrect"].append([])

    return score


def score_guess(guess, answer):
    print("Scoring guess: ", guess, "against ", answer)
    score = generate_empty_score()

    letter_counts = {}
    for letter in answer:
        if letter not in letter_counts:
            letter_counts[letter] = 0
        letter_counts[letter] += 1


    for i, letter in enumerate(guess):
        if letter in letter_counts and letter_counts[letter]:
            if answer[i] == letter:
                score["correct"][i] = letter
            else:
                score["incorrect"][i].append(letter)
            score["required"].append(letter)
            letter_counts[letter] -= 1
        else:
            score["banned"].append(letter)

    return score


def consolodate_scores(scores):
    print("Consolidating scores")
    new_score = generate_empty_score()

    for i in range(5):
        new_score["incorrect"].append([])


    for score in scores:
        for i in range(5):
            if score["correct"][i]:
                new_score["correct"][i] = score["correct"][i]
            if  len(score["incorrect"][i]):
                for letter in score["incorrect"][i]:
                    new_score["incorrect"][i].append(letter)
        new_score["required"] += score["required"]
        new_score["banned"] += score["banned"]

    return new_score


def passes_filter(w, f):
    for letter in f["banned"]:
        if letter in w:
            return False
    for letter in f["required"]:
        if w.count(letter) != f["required"].count(letter):
            return False


    for i in range(5):
        if len(w) == 5 and len(f) == 5:
            if f["correct"][i]:
                if f["correct"][i] != w[i]:
                    return False

            if f["banned"][i]:
                for b in f["banned"][i]:
                    if b == w[i]:
                        return False

    return True



def filter_words(path, score):
    filtered = []
    i = 1
    with open(path, "r") as f:
        all_words = f.read().split("\n")
        for word in all_words:
            i += 1
            if passes_filter(word, score):
                filtered.append(word)

    return filtered


def get_sorted_guesses(path, score, answer):
    print("Getting Sorted guesses")
    guess_scores = dict()
    all_words = []

    with open(path, "r") as f:
        i = 0
        all_words = f.read().split("\n")

    with open("scores.txt", "w") as f:
        for word in all_words:
            print("Getting word score for ", word, f"({i}/{len(all_words)}): ", end="")
            percent_done = (i + 1) / len(all_words) * 100
            print("%.2f" % percent_done, end="")
            print("% done")
            i += 1
            guess_scores[word] = len(filter_words(path, score_guess(word, answer)))
            f.write(f"{word} {guess_scores[word]}\n")

    return sorted(guess_scores, key=lambda x: guess_scores[x])

def main():
    # test_cases = [["SOARE", "CLINT"], ["AREAS", "STRIP"], ["BOOTS", "ROBOT"]]
    #
    # for test in test_cases:
    #     print(score_guess(test[0], test[1]))
    #     print()


    solution_word = "APPLE"
    first_guess = "NAIEO"
    path = "./guessable.txt"

    all_words = []
    valid_words = []

    sorted = get_sorted_guesses(path, score_guess(first_guess, solution_word), solution_word)
    print(list(sorted)[0])
    print(list(sorted)[-1])


main()



# score = {
# correct = [None, None, "S", None, "E"],
# incorrect = [None, "T", None, None, None],
# required = ["S", "E"],
# banned = ["T"]
# }
#

# nswer = "BOOTS"
# guess = "ROBOT"
# score = {
# correct = [None, None, None, None, None]
# incorrect = [None, None, None, None, None]
# required = {}
# banned = []

# }



# answer = "COMBS"
# guess = "BOOTS"


