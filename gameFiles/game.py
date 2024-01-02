from gameFiles.Card import Card
from gameFiles.Noble import Noble
from gameFiles.data import colours

# Splendor colour order:
# - White
# - Blue
# - Green
# - Red
# - Black

tier_1 = [
    Card(1, 'blue', 0, black=3),
    Card(1, 'blue', 0, white=1, black=2),
    Card(1, 'blue', 0, green=2, black=2),
    Card(1, 'blue', 0, white=1, green=2, red=2),
    Card(1, 'blue', 0, blue=1, green=3, red=1),
    Card(1, 'blue', 0, white=1, green=1, red=1, black=1),
    Card(1, 'blue', 0, white=1, green=1, red=2, black=1),
    Card(1, 'blue', 1, red=4),

    Card(1, 'red', 0, white=3),
    Card(1, 'red', 0, blue=2, green=1),
    Card(1, 'red', 0, white=2, red=2),
    Card(1, 'red', 0, white=2, green=1, black=2),
    Card(1, 'red', 0, white=1, red=1, black=3),
    Card(1, 'red', 0, white=1, blue=1, green=1, black=1),
    Card(1, 'red', 0, white=2, blue=1, green=1, black=1),
    Card(1, 'red', 1, white=4),

    Card(1, 'black', 0, green=3),
    Card(1, 'black', 0, green=2, red=1),
    Card(1, 'black', 0, white=2, green=2),
    Card(1, 'black', 0, white=2, blue=2, red=1),
    Card(1, 'black', 0, green=1, red=3, black=1),
    Card(1, 'black', 0, white=1, blue=1, green=1, red=1),
    Card(1, 'black', 0, white=1, blue=2, green=1, red=1),
    Card(1, 'black', 1, blue=4),

    Card(1, 'white', 0, blue=3),
    Card(1, 'white', 0, red=2, black=1),
    Card(1, 'white', 0, blue=2, black=2),
    Card(1, 'white', 0, blue=2, green=2, black=1),
    Card(1, 'white', 0, white=3, blue=1, black=1),
    Card(1, 'white', 0, blue=1, green=1, red=1, black=1),
    Card(1, 'white', 0, blue=1, green=2, red=1, black=1),
    Card(1, 'white', 1, green=4),

    Card(1, 'green', 0, red=3),
    Card(1, 'green', 0, white=2, blue=1),
    Card(1, 'green', 0, blue=2, red=2),
    Card(1, 'green', 0, blue=1, red=2, black=2),
    Card(1, 'green', 0, white=1, blue=3, green=1),
    Card(1, 'green', 0, white=1, blue=1, red=1, black=1),
    Card(1, 'green', 0, white=1, blue=1, red=1, black=2),
    Card(1, 'green', 1, black=4)
]

tier_2 = [
    Card(2, 'blue', 1, blue=2, green=2, red=3),
    Card(2, 'blue', 1, blue=2, green=3, black=3),
    Card(2, 'blue', 2, blue=5),
    Card(2, 'blue', 2, white=5, blue=3),
    Card(2, 'blue', 2, white=2, red=1, black=4),
    Card(2, 'blue', 3, blue=6),

    Card(2, 'red', 1, white=2, red=2, black=3),
    Card(2, 'red', 1, blue=3, red=2, black=3),
    Card(2, 'red', 2, black=5),
    Card(2, 'red', 2, white=3, black=5),
    Card(2, 'red', 2, white=1, blue=4, green=2),
    Card(2, 'red', 3, red=6),

    Card(2, 'black', 1, white=3, blue=2, green=2),
    Card(2, 'black', 1, white=3, green=3, black=2),
    Card(2, 'black', 2, white=5),
    Card(2, 'black', 2, green=5, red=3),
    Card(2, 'black', 2, blue=1, green=4, red=2),
    Card(2, 'black', 3, black=6),

    Card(2, 'white', 1, green=3, red=2, black=2),
    Card(2, 'white', 1, white=2, blue=3, red=3),
    Card(2, 'white', 2, red=5),
    Card(2, 'white', 2, red=5, black=3),
    Card(2, 'white', 2, green=1, red=4, black=2),
    Card(2, 'white', 3, white=6),

    Card(2, 'green', 1, white=2, blue=3, black=2),
    Card(2, 'green', 1, white=3, green=2, red=3),
    Card(2, 'green', 2, green=5),
    Card(2, 'green', 2, blue=5, green=3),
    Card(2, 'green', 2, white=4, blue=2, black=1),
    Card(2, 'green', 3, green=6)
]

tier_3 = [
    Card(3, 'blue', 3, white=3, green=3, red=3, black=5),
    Card(3, 'blue', 4, white=7),
    Card(3, 'blue', 4, white=6, blue=3, black=3),
    Card(3, 'blue', 5, white=7, blue=3),

    Card(3, 'red', 3, white=3, blue=5, green=3, black=5),
    Card(3, 'red', 4, green=7),
    Card(3, 'red', 4, blue=3, green=6, red=3),
    Card(3, 'red', 5, green=7, red=3),

    Card(3, 'black', 3, white=3, blue=3, green=5, red=3),
    Card(3, 'black', 4, red=7),
    Card(3, 'black', 4, green=3, red=6, black=3),
    Card(3, 'black', 5, red=7, black=3),

    Card(3, 'white', 3, blue=3, green=3, red=5, black=3),
    Card(3, 'white', 4, black=7),
    Card(3, 'white', 4, white=3, red=3, black=6),
    Card(3, 'white', 5, white=3, black=7),

    Card(3, 'green', 3, white=5, blue=3, red=3, black=3),
    Card(3, 'green', 4, blue=7),
    Card(3, 'green', 4, white=3, blue=6, green=3),
    Card(3, 'green', 5, blue=7, green=3)
]

triples = {('black', 'blue', 'white'),
           ('black', 'green', 'blue'),
           ('black', 'green', 'white'),
           ('black', 'red', 'blue'),
           ('black', 'red', 'green'),
           ('black', 'red', 'white'),
           ('green', 'blue', 'white'),
           ('red', 'blue', 'white'),
           ('red', 'green', 'blue'),
           ('red', 'green', 'white')}
pairs = [('black', 'red'),
         ('black', 'blue'),
         ('black', 'white'),
         ('black', 'green'),
         ('red', 'blue'),
         ('red', 'white'),
         ('red', 'green'),
         ('blue', 'white'),
         ('blue', 'green'),
         ('green', 'white')]

# tier_1 = [Card(1, 'blue', 0, **{c: 1 for c in triple}) for triple in triples]
# tier_1 = [Card(1, 'blue', 0, **{c1: 2, c2: 1}) for c1, c2 in pairs]
# tier_1 = [Card(1, 'blue', 0, **{'black': 3, 'white': 1}) for _ in range(4)] + [Card(1, 'blue', 0, **{'green': 3, 'red': 1}) for _ in range(4)]
# tier_1 = [Card(1, 'blue', 0, **{'black': 3, 'white': 1}) for _ in range(5)] + [Card(1, 'blue', 0, **{'green': 3, 'red': 1}) for _ in range(5)] + [Card(1, 'red', 0, **{'white': 3, 'green': 1}) for _ in range(5)] + [Card(1, 'red', 0, **{'red': 3, 'black': 1}) for _ in range(5)]
# tier_2 = []
# tier_2 = [Card(2, 'blue', 1, **{'blue': 6}) for _ in range(5)] + [Card(2, 'red', 1, **{'red': 5}) for _ in range(5)]
# tier_1 = tier_1[:18]
# tier_2 = tier_2[:12]
# tier_3 = []
all_cards = tier_1 + tier_2 + tier_3
# tier_1 = set(tier_1)
# tier_2 = set(tier_2)
# tier_3 = set(tier_3)

cards_by_gem_colour = {'white': [],
                       'blue': [],
                       'green': [],
                       'red': [],
                       'black': []}
for card in all_cards:
    for colour in colours:
        if card.num_required(colour):
            cards_by_gem_colour[colour].append(card)

nobles = [
    Noble(red=4, green=4),
    Noble(black=4, red=4),
    Noble(blue=4, green=4),
    Noble(black=4, white=4),
    Noble(blue=4, white=4),
    Noble(black=3, red=3, white=3),
    Noble(green=3, blue=3, white=3),
    Noble(black=3, red=3, green=3),
    Noble(green=3, blue=3, red=3),
    Noble(black=3, blue=3, white=3)
]


def discard_to_n_gems(gems, target, current_possibility={}, possibilities=None,
                      colours=['white', 'blue', 'green', 'red', 'black']):
    if possibilities is None:
        return discard_to_n_gems(gems, target, current_possibility, colours=colours, possibilities=[])
    num_gems = sum(gems.values())

    if num_gems == target:
        possibilities.append(current_possibility)
        return possibilities
    if not colours:
        return possibilities
    assert num_gems >= target

    orig_current_possibility = {c: n for c, n in current_possibility.items()}

    colours = colours[:]
    colour = colours.pop()

    num_gems_of_colour = gems.get(colour, 0)
    for i in range(0, min(num_gems_of_colour, num_gems - target) + 1):
        current_gems = {c: n for c, n in gems.items()}
        current_gems[colour] -= i
        current_possibility = {c: n for c, n in orig_current_possibility.items()}
        current_possibility[colour] = -1 * i
        discard_to_n_gems(current_gems, target,
                          current_possibility=current_possibility,
                          possibilities=possibilities,
                          colours=colours)

    return possibilities


def choose_3(colours):
    choices = []
    for i, colour_1 in enumerate(colours):
        for j, colour_2 in enumerate(colours[i + 1:]):
            j += i + 1
            for k, colour_3 in enumerate(colours[j + 1:]):
                choices.append((colour_1, colour_2, colour_3))
            if len(colours) == 2:
                choices.append((colour_1, colour_2))
        if len(colours) == 1:
            choices.append((colour_1,))

    return choices


def gems_dict_to_list(d):
    return (['white' for _ in range(d.get('white', 0))] +
            ['blue' for _ in range(d.get('blue', 0))] +
            ['green' for _ in range(d.get('green', 0))] +
            ['red' for _ in range(d.get('red', 0))] +
            ['black' for _ in range(d.get('black', 0))] +
            ['gold' for _ in range(d.get('gold', 0))])
