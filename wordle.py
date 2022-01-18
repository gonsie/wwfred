import sys, os

print_ctl = 0
def blockPrint():
    global print_ctl
    print_ctl += 1
    sys.stdout = open(os.devnull, 'w')

def enablePrint(force=False):
    global print_ctl
    print_ctl -= 1
    if not print_ctl or force:
        sys.stdout = sys.__stdout__


from collections import defaultdict
from random import randrange,randint
import time
import pdb

all_words = defaultdict(lambda :0)
letter_freq = defaultdict(lambda :0)
letter_in_pos = [defaultdict(lambda :0) for i in range(5)]
ms_rounds = dict()

alternate_words = dict()

# T = [ (1, [list of words]), (2, list of words)]


def build_dictionary(filename):
    global all_words, T_all_words
    global letter_freq, letter_in_pos

    # build scoring dictionaries
    with open(filename) as file:
        for line in file:
            if line in all_words:
                print(line, "already exists in the set")
            w = line.replace('\n','')
            if len(w) == 5:
                all_words[w]
                for (c,i) in zip(w,range(5)):
                    letter_freq[c] += 1
                    letter_in_pos[i][c] += 1

    print("There are %d words in the dictionary" % len(all_words))

    # score each word
    for w in all_words:
        all_words[w] = sum([letter_freq[c] for c in set(w)])
        for (c,i) in zip(w,range(5)):
            all_words[w] += letter_in_pos[i][c]

def build_rounds_needed():
    global ms_rounds, all_words

    if len(ms_rounds) > 0:
        return

    print("Building rounds needed...")
    ms_rounds = run_all(guess_max_score)

def run_all(strat_f):
    print("Running all words with %s strategy" % strat_f.__name__)
    rounds = dict()
    blockPrint()
    for w in all_words:
        rounds[w] = run_game(strat_f,all_words.copy(),w)
    enablePrint()
    return rounds

def run_1(strat_f):
    print("Running all words with %s strategy" % strat_f.__name__)
    blockPrint()
    reduced = dict()
    for w in all_words:
        reduced[w] = run_1_round(strat_f,all_words.copy(),w)
    enablePrint()
    return reduced


def guess_max_score(words):
    find_max = max(words, key=words.get)
    del words[find_max]
    return find_max

def guess_max_score2(words):
    x_axis = list(set(words.values()))
    x_axis.sort(reverse=True)
    guesses = [w for w in words if words[w] == x_axis[0]]
    if len(guesses) > 2:
        enablePrint(force=True)
        print("There are %d possible words to guess" % len(guesses), guesses)
        pdb.set_trace()
    return guesses[randrange(0,len(guesses))]

def guess_min_score2(words):
    x_axis = list(set(words.values()))
    x_axis.sort()
    guesses = [w for w in words if words[w] == x_axis[0]]
    if len(guesses) > 1:
        print("There are %d possible words to guess" % len(guesses), guesses)
    return guesses[randrange(0,len(guesses))]

def guess_alternate_max_min(words):
    if len(words) == len(all_words):
        guess_alternate.counter = 1
        return guess_max_score2(words)
    elif guess_alternate.counter % 2 == 1:
        guess_alternate.counter += 1
        return guess_min_score2(words)
    else:
        guess_alternate.counter += 1
        return guess_max_score2(words)

def guess_max_out_of_dict(words):
    if len(words) == len(all_words):
        return guess_max_score(words)
    dif = {k:all_words[k] for k in all_words.keys() if k not in words.keys()}
    dif.pop('TARES')
    print("finding best word out of %d" % len(dif))
    return guess_max_score(dif)

def guess_2_not_in_dict(words):
    if len(words) == len(all_words):
        guess_2_not_in_dict.counter = 1
        return guess_max_score2(words)
    elif guess_2_not_in_dict.counter == 1:
        guess_2_not_in_dict.counter += 1
        return guess_max_out_of_dict(words)
    else:
        guess_2_not_in_dict.counter += 1
        return guess_max_score2(words)

def guess_2_alternate_words(words):
    if len(words) == len(all_words):
        guess_2_alternate_words.counter = 1
        return guess_max_score2(words)
    elif guess_2_alternate_words.counter == 1:
        guess_2_alternate_words.counter += 1
        return guess_max_score2(alternate_words)
    else:
        guess_2_alternate_words.counter += 1
        return guess_max_score2(words)


def guess_fewest_rounds(words):
    build_rounds_needed()
    subset = {w: ms_rounds[w] for w in words}
    x_axis = list(set(subset.values()))
    x_axis.sort()
    x = x_axis[0]
    print([w for w in subset if subset[w] == x])
    return [w for w in subset if subset[w] == x][0]

def brute_force_guess(word_dict):
    reduced = dict()
    blockPrint()
    for w in all_words:
        wd = word_dict.copy()
        guess_and_check(guess_max_score2,wd,w)
        reduced[w] = len(wd)
    enablePrint()
    return min(reduced, key=reduced.get)

def guess_brute_force(words):
    if len(words) == len(all_words):
        return 'TARES'
    elif len(words) < 100:
        return brute_force_guess(words)
    else:
        return guess_max_score2(words)


def guess_long_tail(words):
    if len(words) > 26:
        return guess_max_score2(words)

# extra
def build_alternate_potential_words(word_dict,guess,hints):
    global alternate_words
    # shorter name?
    words = alternate_words
    if id(words) != id(alternate_words):
        print("ERROR: we wanted the IDs to be identical")

    for (g,h,i) in zip(guess,hints,range(5)):
        if h == 'X':
            for w in [w for w in words if g in w]: del words[w]
        elif h == '~':
            for w in [w for w in words if w[i] != g]: del words[w]
        elif h == ' ':
            for w in [w for w in words if w[i] == g]: del words[w]
    print("\t\t%d alternates" % len(word_dict))


# core game
def check_guess(guess, answer):
    hints = ''
    for (g,a) in zip(guess,answer):
        if g not in answer:
            hints += 'X'
        elif g != a:
            hints += '~'
        else:
            hints += ' '

    print(' '.join(guess))
    print(' '.join(hints))
    return hints

def update_words(guess,hints,words):
    for (g,h,i) in zip(guess,hints,range(5)):
        #print(len(words), "\t", g, h, i)
        if h == 'X':
            for w in [w for w in words if g in w]: del words[w]
        elif h == '~':
            for w in [w for w in words if w[i] == g]: del words[w]
        elif h == ' ':
            for w in [w for w in words if w[i] != g]: del words[w]
    print("\t\t%d remain" % len(words))
    # if (len(words)) < 27:
    #     print(words)

def guess_and_check(strat_f,words,answer):
    tic = time.perf_counter()
    guess = strat_f(words)
    toc = time.perf_counter()
    hints = check_guess(guess,answer)
    toe = time.perf_counter()
    if guess != answer:
        update_words(guess,hints,words)
        if strat_f.__name__ == "guess_2_alternate_words":
            build_alternate_potential_words(words,guess,hints)
        ton = time.perf_counter()

        # print("TIMINGS:")
        # print(f"Guess: {toc - tic:0.4f}")
        # print(f"Check: {toe - toc:0.4f}")
        # print(f"Winno: {ton - toe:0.4f}")

        return False
    else:
        return True

def run_game(strat_f, words, answer):
    rounds = 1
    global alternate_words
    alternate_words = all_words.copy()
    while True:
        if guess_and_check(strat_f,words, answer):
            print("WINNER in %d rounds" % rounds)
            return rounds
        rounds += 1


def interactive(strat_f,words,answer):
    rounds = 0
    while True:
        rounds += 1
        guess = strat_f(words)
        print("Make guess:\n\t %s" % guess)
        hints = input("\t>")
        if len(hints) == 0:
            print("No hint, assuming you won :) (%d rounds)" % rounds)
            break
        update_words(guess, hints.upper(), words)

def run_1_round(strat_f, words, answer):
   guess_and_check(guess_max_score,words, answer)
   return len(words)

def run_6_strat_rounds(words, answer):
    # round 1
    if guess_and_check(guess_max_score,words, answer):
        print("WINNER")
        return 1
    # round 2
    if guess_and_check(guess_max_score,words, answer):
        print("WINNER")
        return 2
    # round 3
    if guess_and_check(guess_max_score,words, answer):
        print("WINNER")
        return 3
    # round 4
    if guess_and_check(guess_max_score,words, answer):
        print("WINNER")
        return 4
    # round 5
    if guess_and_check(guess_max_score,words, answer):
        print("WINNER")
        return 5
    # round 6
    if guess_and_check(guess_max_score,words, answer):
        print("WINNER")
        return 6
    print("LOSER")
    return 0


def print_hist(word_dict, title):
    x_axis = list(set(word_dict.values()))
    x_axis.sort()
    print("HISTOGRAM of %s for N words" % title)
    for x in x_axis:
        print(x, len([w for w in word_dict if word_dict[w] == x]))

def print_sample(word_dict, title):
    x_axis = list(set(word_dict.values()))
    x_axis.sort()
    print("SAMPLE Words for %s" % title)
    for x in x_axis:
        print(x, [w for w in word_dict if word_dict[w] == x][:10])

def print_stats(word_dict, title):
    print_hist(word_dict,title)
    print_sample(word_dict,title)


def main(dictionary):
    build_dictionary(dictionary)
    #build_rounds_needed()

    # default strategy
    strategy = guess_max_score2
    print("Strategy is %s" % strategy.__name__)
    mode = run_game
    print("Mode is %s" % mode.__name__)
    print("Run '?' for help")

    # read commands
    while 1:
        cmd = input(" $ ")
        cmd = cmd.upper()

        # exit command
        if cmd.lower() == "quit" or cmd.lower() == "q":
            break

        # do nothing command
        if cmd == "":
            continue

        if cmd == "?":
            print("q | quit\t\tQuit the program")
            print("-strat [strategy]\tChange default strategy")
            print("-mode [mode]\t\tChange default mode")
            print("-runall\t\t\tRun all")
            print("-gc [guess] [answer]\tGuess and Check")
            print("-ps [word]\t\tPrint Score")
            print("-run1\t\t\tRun 1")
            print("-mode [interacvite | run_game]")
            continue

        # special commands
        if cmd[0] == '-':
            cmd = cmd.split(' ')
            cmd[0] = cmd[0].lower()

            # change default strategy
            if cmd[0] == "-strat":
                possibles = globals().copy()
                possibles.update(locals())
                method = possibles.get(cmd[1].lower())
                if not method:
                    print("That stategy does not exist\n")
                else:
                    strategy = method
                print("Strategy is %s" % strategy.__name__)

            elif cmd[0] == "-runall":
                rounds_needed = run_all(strategy)
                print_stats(rounds_needed,"Rounds Needed")

            elif cmd[0] == "-run1":
                reduced_size = run_1(guess_tares)
                print_stats(reduced_size,"TARES -- Reduced size")

            # guess and check
            elif cmd[0] == "-gc":
                guess_and_check(lambda _:cmd[1],all_words.copy(),cmd[2])

            # print scre
            elif cmd[0] == "-ps":
                print("Score is %d" % all_words[cmd[1]])

            elif cmd[0] == "-mode":
                possibles = globals().copy()
                possibles.update(locals())
                method = possibles.get(cmd[1].lower())
                if not method:
                    print("That mode does not exist\n")
                else:
                    mode = method
                print("Mode is %s" % mode.__name__)

            else:
                print("Unknown command :(")

            continue


        if len(cmd) != 5:
            print("Word should be 5 letters\n")
            continue

        if cmd not in all_words:
            print("%s is not in the dictionary\n" % cmd)
            continue

        #run_6_strat_rounds(all_words.copy(), cmd)
        mode(strategy,all_words.copy(),cmd)



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: %s dictionary.txt" % sys.argv[0])
        exit()
    main(sys.argv[1])
