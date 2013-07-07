import copy

SCRABBLE_DICTIONARY = ['spur', 'sour', 'spud', 'stud', 'stun', 'a', 'dog', 'terrible', 'hopeless']
WORD_LENGTH = 4
LADDER_LENGTH = 5

class Word():

    LETTER_SCORE_DICTIONARY = {
                'a': 1, 'b': 3, 'c': 3,  'd': 2,
                'e': 1, 'f': 4, 'g': 2, 'h':4,
                'i': 1, 'j': 8, 'k': 5, 'l':1,
                'm':3, 'n':1, 'o':1, 'p':3, 'q':10,
                'r':1, 's':1, 't':1, 'u':1, 'v':4,
                'w':4, 'x':8, 'y':4, 'z':10
                }

    def __init__(self, str1):
        self.word = str1.lower()
        self.value = self.__calculate_value()

    def __calculate_value(self):
        score = 0
        for letter in self.word:
            score += self.LETTER_SCORE_DICTIONARY[letter]
        return score

    def __str__(self):
        return self.word + ", " + str(self.value)

class Dictionary():

    def __init__(self, list1, int1):
        self.original_word_list = list1
        self.word_length = int1
        self.words = [Word(word) for word in self.__filter_on_wordlength()]

    def __filter_on_wordlength(self):
        return [word for word in self.original_word_list if len(word) == self.word_length]

    def contains(word):
        if word in self.words:
            return True
        return False

class Ladder():

    def __init__(self, required_length = 0):
        # If the requested ladder length is invalid, ignore ladder length as a criterion
        self.ladder_length_matters = self.is_valid_ladder_length(required_length)
        self.required_length = required_length # never used
        self.half_length = (self.required_length - 1) / 2 # half of the length, rounded down. This is only used when the ladder has a required length
        self.ladder = []
        self.descending = False
        self.length = -1

    def is_scrabble_ladder(self):
        if self.length == len(self.ladder):
            return True
        return False

    def add_word_without_check(self, word):
        self.ladder.append(word)
        if not self.descending and len(self.ladder) > 1 and word.value < self.ladder[-2].value: #self.ladder[-2] represents the last word in the ladder before the new one was added
            self.descending = True
            self.length = len(self.ladder) * 2 - 3

    def word_is_valid_addition(self, word):
        # set a useful variable
        current_length = len(self.ladder)

        # the ladder is empty, so any word works
        if current_length == 0:
            return True

        # set another useful variable
        last_word = self.ladder[-1]

        # check similarity of words
        difference = False
        for n in range(len(word.word)):
            if word.word[n] != last_word.word[n]:
                if difference:
                    return False
                else:
                    difference = True

        # If the ladder requires a certain length, compare word values differently:
        if self.ladder_length_matters:
            if word.value > last_word.value and current_length <= self.half_length:
                return True
            if word.value < last_word.value and current_length > self.half_length:
                return True
            return False

        # New word's value is greater, and the ladder hasn't reached the "peak" yet
        if word.value > last_word.value and not self.descending:
            return True

        # Word has a lower value and the ladder is at least 2 words long
        if word.value < last_word.value and len(self.ladder) > 1:
            return True

        return False

    def score(self):
        score = 0
        for word in self.ladder:
            score += word.value
        return score

    def equals(self, ladder1):
        if len(self.ladder) != len(ladder1.ladder):
            return False
        flag1 = True
        for n in range(len(self.ladder)):
            if self.ladder[n].word != ladder1.ladder[n].word:
                flag1 = False
        a_list = list(ladder1.ladder)
        flag2 = True
        for n in range(len(self.ladder)):
            if self.ladder[n].word != a_list[n].word:
                flag1 = False
        return flag1 or flag2

    def is_valid_ladder_length(self, int1):
        return False if int1 < 1 or int1 % 2 == 0 else True

    def __str__(self):
        return_string = "This Ladder has Length " + str(len(self.ladder)) + " and contains: "
        for word in self.ladder:
            return_string += str(word) + ", "
        return return_string

    def __repr__(self):
        return self.__str__()


class Ladders():

    # if ladder_length isn't valid (it is < 3 or even), any ladder length is valid
    def __init__(self, words, word_length, ladder_length = 0):
        self.dictionary = Dictionary(words, word_length)
        self.ladder_length = ladder_length
        self.HIGHEST_SCORE = 0
        self.HIGHEST_SCORE_LADDERS = []

    def calculate_highest_score(self):

        def method_helper(dictionary, ladder):
            print(ladder)
            #base case
            if ladder.is_scrabble_ladder():
                print("found one")
                # The ladder has the same value as the current high score
                if ladder.score() == self.HIGHEST_SCORE:
                    #check for reverse duplicates
                    for ladder1 in self.HIGHEST_SCORE_LADDERS:
                        if ladder1.equals(ladder):
                            print("DUPLICATE")
                            return
                    self.HIGHEST_SCORE_LADDERS.append(ladder)
                    print("ADDED ONE")
                # The ladder has a higher value than the current high score
                if ladder.score() > self.HIGHEST_SCORE:
                    print("NEW HIGH SCORE")
                    self.HIGHEST_SCORE = ladder.score()
                    self.HIGHEST_SCORE_LADDERS = [ladder]
                return
            #if the ladder isn't complete, check more combinations
            for n in range(len(dictionary.words)):
                if ladder.word_is_valid_addition(dictionary.words[n]):
                    #make a new ladder and add the word
                    new_ladder = copy.deepcopy(ladder)
                    new_ladder.add_word_without_check(dictionary.words[n])
                    #make a new dictionary that doesn't contain the word that was just added
                    new_dictionary = copy.deepcopy(dictionary)
                    new_dictionary.words.pop(n)
                    #call the helper method again
                    method_helper(new_dictionary, new_ladder)

        # if the ladder length is 1, find the highest value words, otherwise
        # call method_helper to find the highest-value ladders
        if self.ladder_length == 1:
            for word in self.dictionary.words:
                if word.value == self.HIGHEST_SCORE:
                    a_ladder = Ladder()
                    a_ladder.add_word_without_check(word)
                    self.HIGHEST_SCORE_LADDERS.append([a_ladder])
                if word.value > self.HIGHEST_SCORE:
                    self.HIGHEST_SCORE = word.value
                    a_ladder = Ladder()
                    a_ladder.add_word_without_check(word)
                    self.HIGHEST_SCORE_LADDERS = [a_ladder]
        else:
            method_helper(self.dictionary, Ladder(self.ladder_length))
        # print the results
        self.print_results()
        
    def print_results(self):
        print("\n\n")
        print("#######################################################################")
        print("############################# RESULTS #################################")
        print("#######################################################################")
        # print the requirements
        print("The reverse of a ladder is not printed (example: either (spur spud stud) or (stud spud spur) will display but not both)")
        print("Word Length: " + str(self.dictionary.word_length))
        if Ladder().is_valid_ladder_length(self.ladder_length):
            print("Ladder Length: " + str(self.ladder_length))
        else:
            print("Ladder Length wasn't a factor because an invalid ladder lenght was specified (less than 3 or divisible by 2)")
        if self.HIGHEST_SCORE == 0:
            print("There is no scrabble ladder with the given requirements")
        else:
            print("The highest-scoring ladder's score was: " + str(self.HIGHEST_SCORE))
            print(str(len(self.HIGHEST_SCORE_LADDERS)) + " ladder(s) had this score:")
            for n in range(len(self.HIGHEST_SCORE_LADDERS)):
                print(str(n + 1) + ": " + str(self.HIGHEST_SCORE_LADDERS[n]))
        print("#######################################################################")
        print("#######################################################################")
        print("#######################################################################")

# Create a Ladders object and initialize it with the list of words
# and the maximum word length, then calculate the highest scrabble
# ladder score
bla = Ladders(SCRABBLE_DICTIONARY, WORD_LENGTH, LADDER_LENGTH)
bla.calculate_highest_score()

