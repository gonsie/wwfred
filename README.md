# WWFRED: Words With Friends RegExp Dictionary

A simple command line application to help find words for tile-based word games (e.g., Scrabble or Words With Friends).
Given a dictionary of words, a set of letter tiles, and a regular expression this program generates words that can be made.

This program does not take into account the tile scores.
Nor does it save the state of the board (which would include words on the board and "bonus" point available on the board).

This program simply helps the user find valid words.
All strategic decisions, such as word placement, are left up to the user.

## Dependencies

- python
  - re module

## Usage

Download `wwf-regex.py` and the `masterlist.txt` file.
Then, run the program with python:

```
    $ python wwf-regex.py
```

WWF-REGEX is an interactive, shell-like program.
After typing a command or regular expression, hit the `<ENTER>` key to process the input.

## Available Commands

Internal commands are specified with a leading dash, `-`.
(Almost) All other input is assumed to be a regular expression.

### Setting Tiles in the Hand: `-st`

```
 $ -st abcdefg
tiles are ['a', 'b', 'c', 'd', 'e', 'f', 'g']
```

### Set Maximum Length: `-len`

```
 $ -len 8
max word length is 8
```

### Regular Expressions

```
 $ ^.hi.$      
chip
chit
chid
...
```

Input is typically parsed as a regular expression.
If the length or current hand of tiles is set, only matching entries appear.

See below for more details.

### Ending the Program: `quit`

```
 $ quit
```

The word `quit` is reserved and inputting it will end the program.
No settings or tiles are saved.

## Regular Expressions

This program uses the Python regular expression library: see http://docs.python.org/howto/regex.html.

For more information about regular expressions, see this wikipedia article: http://en.wikipedia.org/wiki/Regular_expression
