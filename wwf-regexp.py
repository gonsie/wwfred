import re

def main():
    words = set()
    file = open("masterlist.txt")
    for line in file:
        if line in words:
            print line,"already exists in the set"
        words.add(line.replace('\n', ''))
    
    tiles = []
    plays = []
    max_length = 100
    
    # read commands
    while 1:
        print "still using", tiles
        cmd = raw_input(" $ ")
        
        # exit command
        if cmd.lower() == "quit":
            break
        
        # do nothing command
        if cmd == "":
            continue
        
        # flagged commands
        if cmd[0] == '-':
            cmd = cmd.split(' ')
            
            # set tiles
            if cmd[0] == "-st":
                if len(cmd) != 2:
                    print "blank should be denoted with a space."
                tiles = []
                for c in cmd[1]:
                    tiles.append(c)
                print "tiles are", tiles
            
            # saved words and scores
            elif cmd[0] == "-save" or cmd[0] == "-s":
                plays.append([cmd[2], cmd[1]])
            
            # list saved words
            elif cmd[0] == "-p" or cmd[0] == "-plays":
                plays.sort()
                print plays
            
            # limit length of word
            elif cmd[0] == "-len":
                max_length = int(cmd[1])
                print "max word length is", max_length
            
        # regexp command
        else:
            p = re.compile(cmd.lower(), re.IGNORECASE)
            for word in words:
                m = p.findall(word)
                if m and len(word) <= max_length:
                    if len(tiles) > 0:
                        limit_tiles(word, tiles, cmd)
                    else:
                        print word

def limit_tiles(word, copy, cmd):
    tiles = copy[:]
    alpha = re.compile("[a-z]")
    for c in cmd:
        if c in alpha.findall(c):
            tiles.append(c)
    for c in word:
        if c not in tiles:
            if '.' in tiles:
                tiles.remove('.')
            else:
                return
        else:
            tiles.remove(c)
    print word

if __name__ == "__main__":
    main()
