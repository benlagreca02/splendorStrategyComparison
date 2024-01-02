import numpy as np

from gameFiles.data import colours, colour_indices
from gameFiles.game import all_cards


class StateVector(object):
    def __init__(self, num_players, vector=None):
        super(StateVector, self).__init__()

        self.num_players = num_players

        self.num_gems_in_play = {2: 4, 3: 5, 4: 7}[num_players]
        self.num_dev_cards = 4
        self.num_nobles = {2: 3, 3: 4, 4: 5}[num_players]

        self.num_cards = len(all_cards)

        if vector is None:
            self.init_vector()
        else:
            self.vector = vector

    def copy(self):
        vector = StateVector(num_players=self.num_players,
                             vector=self.vector.copy())
        vector.supply_gem_indices = self.supply_gem_indices
        vector.player_gem_indices = self.player_gem_indices
        vector.player_played_colours_indices = self.player_played_colours_indices
        vector.player_score_indices = self.player_score_indices
        vector.current_player_indices = self.current_player_indices
        vector.card_cost_indices = self.card_cost_indices
        vector.player_card_cost_indices = self.player_card_cost_indices
        vector.card_points_indices = self.card_points_indices
        vector.player_card_points_indices = self.player_card_points_indices
        vector.tier_max_gems = self.tier_max_gems
        vector.tier_max_points = self.tier_max_points
        vector.tier_min_points = self.tier_min_points
        vector.points_indices = self.points_indices
        vector.no_points_indices = self.no_points_indices
        vector.noble_cost_indices = self.noble_cost_indices
        vector.nobles_present_index = self.nobles_present_index
        vector.card_remaining_cost_indices = self.card_remaining_cost_indices
        vector.player_card_remaining_cost_indices = self.player_card_remaining_cost_indices

        vector.card_colour_indices = self.card_colour_indices
        vector.player_card_colour_indices = self.player_card_colour_indices

        return vector

    def from_perspective_of(self, index, debug=False):
        if index == 0:
            return self.vector

        vector = self.vector
        new_vector = self.vector.copy()
        num_cards = self.num_cards
        num_players = self.num_players

        first_colour = colours[0]

        # # Rotate the cards in hand values
        # start_index = 0
        # end_index = self.supply_gem_indices[colours[0]]
        # player_cards_in_hand = [vector[start_index + 2 + i:end_index:(2 + num_players + num_players)]
        #                         for i in range(num_players)]
        # for i in range(num_players):
        #     cards_in_hand = player_cards_in_hand[(i + index) % num_players]
        #     assert len(cards_in_hand) == num_cards
        #     new_vector[(start_index + 2 + i):end_index:(2 + num_players + num_players)] = cards_in_hand

        # if debug:
        #     import ipdb
        #     ipdb.set_trace()

        # # Rotate the cards played values
        # start_index = 0
        # end_index = self.supply_gem_indices[colours[0]]
        # player_cards_played = [vector[start_index + 2 + num_players + i:end_index:(2 + num_players * 2)]
        #                        for i in range(num_players)]
        # for i in range(num_players):
        #     cards_played = player_cards_played[(i + index) % num_players]
        #     assert len(cards_played) == num_cards
        #     new_vector[(start_index + 2 + num_players + i):end_index:(2 + num_players * 2)] = cards_played

        # Rotate number of gems held by each player
        arr_size = self.player_gem_indices[1, colours[0]] - self.player_gem_indices[0, colours[0]]
        player_gems = [
            vector[self.player_gem_indices[(i, first_colour)]:self.player_gem_indices[(i, first_colour)] + arr_size] for
            i in range(num_players)]
        for i in range(num_players):
            cur_player_gems = player_gems[(i + index) % num_players]
            cur_player_index = self.player_gem_indices[(i, first_colour)]
            new_vector[cur_player_index:cur_player_index + arr_size] = cur_player_gems

        # Rotate number of cards played by each player
        arr_size = 8 * 5
        player_cards = [vector[self.player_played_colours_indices[(i, first_colour)]:self.player_played_colours_indices[
                                                                                         (i, first_colour)] + arr_size]
                        for i in range(num_players)]
        for i in range(num_players):
            cur_player_num_cards = player_cards[(i + index) % num_players]
            cur_player_index = self.player_played_colours_indices[(i, first_colour)]
            new_vector[cur_player_index:cur_player_index + arr_size] = cur_player_num_cards

        # Rotate current score of each player
        arr_size = 21
        player_scores = [vector[self.player_score_indices[i]:self.player_score_indices[i] + arr_size] for i in
                         range(num_players)]
        for i in range(num_players):
            cur_player_score = player_scores[(i + index) % num_players]
            cur_player_index = self.player_score_indices[i]
            new_vector[cur_player_index:cur_player_index + arr_size] = cur_player_score

        # Rotate current player
        p1_index = self.current_player_indices[0]
        current_players = vector[p1_index:p1_index + self.num_players]
        new_vector[p1_index:p1_index + self.num_players] = np.roll(current_players, -1 * index)

        # Rotate noble remaining costs
        p1_index = self.noble_cost_indices[(0, 0, colours[0])]
        current_costs = vector[
                        p1_index:p1_index + self.num_players * len(colours) * 5 * self.num_nobles]
        new_vector[p1_index:p1_index + len(current_costs)] = np.roll(
            current_costs, len(colours) * 5 * self.num_nobles * index)

        # Rotate cost of cards in hand
        p1_index = self.player_card_cost_indices[(0, 0, colours[0])]
        p2_index = self.player_card_cost_indices[(1, 0, colours[0])]
        length = p2_index - p1_index
        new_vector[p1_index:p1_index + self.num_players * length] = np.roll(
            vector[p1_index:p1_index + self.num_players * length], -1 * length * index)

        # Rotate points of cards in hand
        p1_index = self.player_card_points_indices[(0, 0)]
        p2_index = self.player_card_points_indices[(1, 0)]
        length = p2_index - p1_index
        new_vector[p1_index:p1_index + self.num_players * length] = np.roll(
            vector[p1_index:p1_index + self.num_players * length], -1 * length * index)

        # Rotate remaining cost of cards in market
        p1_index = self.card_remaining_cost_indices[(0, 1, 0, 'white')]
        p2_index = self.card_remaining_cost_indices[(1, 1, 0, 'white')]
        length = p2_index - p1_index
        new_vector[p1_index:p1_index + self.num_players * length] = np.roll(
            vector[p1_index:p1_index + self.num_players * length], -1 * length * index)

        # Rotate remaining cost of cards in hands
        p1_index = self.player_card_remaining_cost_indices[(0, 0, 'white')]
        p2_index = self.player_card_remaining_cost_indices[(1, 0, 'white')]
        length = p2_index - p1_index
        new_vector[p1_index:p1_index + self.num_players * length] = np.roll(
            vector[p1_index:p1_index + self.num_players * length], -1 * length * index)

        # Rotate colours of hand cards
        p1_index = self.player_card_colour_indices[(0, 0)]
        p2_index = self.player_card_colour_indices[(1, 0)]
        length = p2_index - p1_index
        new_vector[p1_index:p1_index + self.num_players * length] = np.roll(
            vector[p1_index:p1_index + self.num_players * length], -1 * length * index)

        # Rotate number of points-less buys
        p1_index = self.no_points_indices[0]
        p2_index = self.no_points_indices[1]
        length = p2_index - p1_index
        new_vector[p1_index:p1_index + self.num_players * length] = np.roll(
            vector[p1_index:p1_index + self.num_players * length], -1 * length * index)

        # Rotate number of pointsful buys
        p1_index = self.points_indices[0]
        p2_index = self.points_indices[1]
        length = p2_index - p1_index
        new_vector[p1_index:p1_index + self.num_players * length] = np.roll(
            vector[p1_index:p1_index + self.num_players * length], -1 * length * index)

        return new_vector

    def init_vector(self):

        num_players = self.num_players
        num_cards = len(all_cards)

        cur_index = 0

        # # store card locations
        # card_locations = [0 for _ in range(num_cards * (2 + num_players + num_players))]
        # self.card_indices = {card: i * (2 + num_players + num_players)
        #                      for i, card in enumerate(all_cards)}

        # cur_index += len(card_locations)

        # store numbers of gems in the supply
        num_colour_gems_in_play = self.num_gems_in_play
        gem_nums_in_supply = [0 for _ in range(5 * (num_colour_gems_in_play + 1))]
        self.supply_gem_indices = {colour: cur_index + i * (num_colour_gems_in_play + 1)
                                   for i, colour in enumerate(colours)}

        cur_index += len(gem_nums_in_supply)

        # ...plus gold
        gold_nums_in_supply = [0 for _ in range(6)]
        self.supply_gem_indices['gold'] = cur_index

        cur_index += len(gold_nums_in_supply)

        # store numbers of gems held by each player
        all_player_gems = []
        player_gem_indices = {}
        for player_index in range(num_players):
            player_gems = [0 for _ in range(5 * (num_colour_gems_in_play + 1))]
            all_player_gems.extend(player_gems)
            player_gem_indices.update({(player_index, colour): cur_index + i * (num_colour_gems_in_play + 1)
                                       for i, colour in enumerate(colours)})
            cur_index += len(player_gems)

            all_player_gems.extend([0 for _ in range(6)])
            player_gem_indices[(player_index, 'gold')] = cur_index
            cur_index += 6

            all_player_gems.extend([0 for _ in range(11)])
            player_gem_indices[(player_index, 'all')] = cur_index
            cur_index += 11

        self.player_gem_indices = player_gem_indices

        # store numbers of coloured cards played by each player
        # only count up to 7 - more than this makes no difference
        all_player_cards = []
        player_played_colours_indices = {}
        for player_index in range(num_players):
            player_cards = [0 for _ in range(5 * 8)]
            all_player_cards.extend(player_cards)

            player_played_colours_indices.update({(player_index, colour): cur_index + i * 8
                                                  for i, colour in enumerate(colours)})
            cur_index += len(player_cards)
        self.player_played_colours_indices = player_played_colours_indices

        # store number of points of each player
        # only count up to 20, higher scores are very unlikely
        player_scores = [0 for _ in range(21 * num_players)]
        self.player_score_indices = {player_index: cur_index + player_index * 21
                                     for player_index in range(num_players)}

        cur_index += len(player_scores)

        # store current player
        current_player = [0 for _ in range(num_players)]
        current_player[0] = 1
        self.current_player_indices = {player_index: cur_index + player_index
                                       for player_index in range(num_players)}

        cur_index += len(current_player)

        # # store current round
        # current_round = [0 for _ in range(51)]
        # current_round[0] = 1
        # self.current_round_index = cur_index

        # cur_index += 51

        # store remaining cost of each available noble
        noble_cost_indices = {}
        noble_costs = [0 for _ in range(self.num_nobles * 5 * 5 * num_players)]
        for player_index in range(num_players):
            for noble_index in range(self.num_nobles):
                for colour_index, colour in enumerate(colours):
                    noble_cost_indices[(player_index, noble_index, colour)] = (
                            cur_index + noble_index * 5 * 5 + colour_index * 5 + player_index * self.num_nobles * 5 * 5)
        self.noble_cost_indices = noble_cost_indices
        cur_index += len(noble_costs)

        # store whether each noble is present
        nobles_present = [0 for _ in range(self.num_nobles)]
        self.nobles_present_index = cur_index
        cur_index += len(nobles_present)

        # store cost of each available card
        card_cost_indices = {}
        t1_max_gems = 5
        for card_index in range(4):  # tier 1
            for colour_index, colour in enumerate(colours):
                card_cost_indices[(1, card_index, colour)] = (
                        cur_index + card_index * 5 * t1_max_gems + colour_index * t1_max_gems)
        cur_index += 4 * 5 * t1_max_gems
        t2_max_gems = 7
        for card_index in range(4):  # tier 2
            for colour_index, colour in enumerate(colours):
                card_cost_indices[(2, card_index, colour)] = (
                        cur_index + card_index * 5 * t2_max_gems + colour_index * t2_max_gems)
        cur_index += 4 * 5 * t2_max_gems
        t3_max_gems = 8
        for card_index in range(4):  # tier 3
            for colour_index, colour in enumerate(colours):
                card_cost_indices[(3, card_index, colour)] = (
                        cur_index + card_index * 5 * t3_max_gems + colour_index * t3_max_gems)
        cur_index += 4 * 5 * t3_max_gems
        self.card_cost_indices = card_cost_indices
        self.tier_max_gems = {1: 5, 2: 7, 3: 8}
        card_costs = [0 for _ in range(4 * 5 * (t1_max_gems + t2_max_gems + t3_max_gems))]

        # store cost of each card in player hands
        player_card_cost_indices = {}
        hand_max_gems = 8
        for player_index in range(num_players):
            for card_index in range(3):  # player hands
                for colour_index, colour in enumerate(colours):
                    player_card_cost_indices[(player_index, card_index, colour)] = (
                            cur_index + card_index * 5 * hand_max_gems + colour_index * t3_max_gems)
            cur_index += 3 * 5 * hand_max_gems
        self.player_card_cost_indices = player_card_cost_indices
        player_card_costs = [0 for _ in range(3 * 5 * hand_max_gems * num_players)]

        # store remaining cost of each available card
        card_remaining_cost_indices = {}
        for player_index in range(num_players):
            for tier_index in range(1, 4):
                tier_max_gems = {1: 5, 2: 7, 3: 8}[tier_index]
                for card_index in range(4):
                    for colour_index, colour in enumerate(colours):
                        card_remaining_cost_indices[
                            (player_index, tier_index, card_index, colour)] = cur_index
                        cur_index += tier_max_gems
        self.card_remaining_cost_indices = card_remaining_cost_indices
        remaining_card_costs = [0 for _ in range(num_players * (5 + 7 + 8) * 4 * 5)]

        # store remaining cost of each card in player hands
        player_card_remaining_cost_indices = {}
        hand_max_gems = 8
        for player_index in range(num_players):
            for card_index in range(3):
                for colour in colours:
                    player_card_remaining_cost_indices[(player_index, card_index, colour)] = cur_index
                    cur_index += hand_max_gems
        self.player_card_remaining_cost_indices = player_card_remaining_cost_indices
        player_remaining_card_costs = [0 for _ in range(num_players * 8 * 3 * 5)]

        # store points value of each available card
        card_points_indices = {}
        self.tier_max_points = {1: 1, 2: 3, 3: 5}
        self.tier_min_points = {1: 0, 2: 1, 3: 3}
        t1_num_diff_points = 2
        t2_num_diff_points = 3
        t3_num_diff_points = 3
        for card_index in range(4):  # tier 1
            card_points_indices[(1, card_index)] = cur_index + card_index * t1_num_diff_points
        cur_index += 4 * t1_num_diff_points
        for card_index in range(4):  # tier 2
            card_points_indices[(2, card_index)] = cur_index + card_index * t2_num_diff_points
        cur_index += 4 * t2_num_diff_points
        for card_index in range(4):  # tier 3
            card_points_indices[(3, card_index)] = cur_index + card_index * t3_num_diff_points
        cur_index += 4 * t3_num_diff_points
        card_points = [0 for _ in range(4 * (t1_num_diff_points + t2_num_diff_points + t3_num_diff_points))]
        self.card_points_indices = card_points_indices

        # store points value of each card in player hands
        hand_max_points = 6
        player_card_points_indices = {}
        for player_index in range(num_players):
            for card_index in range(3):  # player hands
                player_card_points_indices[(player_index, card_index)] = cur_index + card_index * hand_max_points
            cur_index += 3 * hand_max_points
        player_card_points = [0 for _ in range(num_players * 3 * hand_max_points)]
        self.player_card_points_indices = player_card_points_indices

        # store colour of each available card
        card_colour_indices = {}
        for tier_index in range(1, 4):
            for card_index in range(4):
                card_colour_indices[(tier_index, card_index)] = (
                        cur_index +
                        (tier_index - 1) * 4 * len(colour_indices) +
                        card_index * len(colour_indices))
        card_colours = [0 for _ in range(3 * 4 * len(colour_indices))]
        cur_index += len(card_colours)
        self.card_colour_indices = card_colour_indices

        # store colour of each card in player hands
        player_card_colour_indices = {}
        for player_index in range(num_players):
            for card_index in range(3):
                player_card_colour_indices[(player_index, card_index)] = (
                        cur_index +
                        player_index * 3 * len(colour_indices) +
                        card_index * len(colour_indices))
        player_card_colours = [0 for _ in range(num_players * 3 * len(colour_indices))]
        self.player_card_colour_indices = player_card_colour_indices
        cur_index += len(player_card_colours)

        # store number of times a points-less card has been bought
        no_points_buys = [0 for _ in range(16 * num_players)]
        self.no_points_indices = {player_index: cur_index + 16 * player_index for player_index in range(num_players)}
        cur_index += len(no_points_buys)

        # store number of times a pointful card has been bought
        points_buys = [0 for _ in range(10 * num_players)]
        self.points_indices = {player_index: cur_index + 10 * player_index for player_index in range(num_players)}
        cur_index += len(points_buys)

        # missing_state = [0]
        # self.missing_state_index = cur_index
        # cur_index += 1

        self.vector = np.array(  # card_locations +
            gem_nums_in_supply + gold_nums_in_supply +
            all_player_gems + all_player_cards + player_scores +
            # nobles_available +
            current_player +
            noble_costs +
            nobles_present +
            # current_round +
            card_costs + player_card_costs +
            remaining_card_costs + player_remaining_card_costs +
            card_points + player_card_points +
            card_colours + player_card_colours +
            no_points_buys + points_buys
            # missing_state
        )
        # card_progress)

    def verify_state(self):

        # for i, card in enumerate(all_cards):
        #     index = self.card_indices[card]
        #     assert np.sum(self.vector[index:index + 2 + self.num_players + self.num_players]) == 1

        for colour in colours:
            index = self.supply_gem_indices[colour]
            assert np.sum(self.vector[index:index + self.num_gems_in_play + 1] == 1)
        gold_index = self.supply_gem_indices['gold']
        assert np.sum(self.vector[gold_index:gold_index + 5 + 1]) == 1

        for player_index in range(self.num_players):
            for colour in colours:
                index = self.player_gem_indices[(player_index, colour)]
                assert np.sum(self.vector[index:index + self.num_gems_in_play + 1] == 1)
            gold_index = self.player_gem_indices[(player_index, 'gold')]
            assert np.sum(self.vector[gold_index:gold_index + 5 + 1]) == 1

            # score_index = self.player_score_indices[player_index]
            # assert np.sum(self.vector[score_index:score_index + 21]) == 1

        current_player_index = self.current_player_indices[0]
        players = self.vector[current_player_index:current_player_index + self.num_players]
        assert np.sum(players) == 1

        vs = [self.from_perspective_of(i) for i in range(self.num_players)]
        sums = [np.sum(v) for v in vs]
        assert np.all(sums == sums[0])

    def num_supply_gems(self, colour):
        index = self.supply_gem_indices[colour]
        arr = self.vector[index:index + self.num_gems_in_play + 1]
        return np.argmax(arr)
        # return np.sum(arr) - 1

    # def set_missing_state(self, missing_state):
    #     index = self.missing_state_index
    #     self.vector[index] = 1

    def set_current_round(self, round_number):
        return
        index = self.current_round_index
        self.vector[index:index + 51] = 0
        # self.vector[index:index + round_number + 1] = 1
        self.vector[index + round_number] = 1

    def set_card_location(self, card, location):
        return  # not currently included
        card_index = self.card_indices[card]
        for i in range(2 + self.num_players):
            self.vector[card_index + i] = 0
        if location is not None:
            self.vector[card_index + location] = 1

    def set_supply_gems(self, colour, number):
        index = self.supply_gem_indices[colour]
        num_gems_in_play = self.num_gems_in_play if colour != 'gold' else 5
        self.vector[index:index + num_gems_in_play + 1] = 0
        # self.vector[index:index + number + 1] = 1
        self.vector[index + number] = 1

    def set_player_gems(self, player_index, colour, number):
        index = self.player_gem_indices[(player_index, colour)]
        if colour == 'gold':
            num_gems_in_play = 5
        elif colour == 'all':
            num_gems_in_play = 10
        else:
            num_gems_in_play = self.num_gems_in_play
        for i in range(num_gems_in_play + 1):
            self.vector[index + i] = 0
        # self.vector[index:index + number + 1] = 1
        self.vector[index + min(number, num_gems_in_play)] = 1

    def set_player_played_colour(self, player_index, colour, number):
        number = min(7, number)
        index = self.player_played_colours_indices[(player_index, colour)]
        for i in range(8):
            self.vector[index + i] = 0
        # self.vector[index + number] = 1
        self.vector[index:index + number + 1] = 1

    def set_player_score(self, player_index, score):
        score = min(score, 20)  # measured scores are clamped to 20
        index = self.player_score_indices[player_index]
        for i in range(21):
            self.vector[index + i] = 0
        # self.vector[index + score] = 1
        self.vector[index:index + score + 1] = 1

    def set_noble_available(self, noble, available):
        raise ValueError('set_noble_available no longer valid')
        noble_index = self.noble_indices[noble]
        if available:
            self.vector[noble_index] = 1
        else:
            self.vector[noble_index] = 0

    def set_current_player(self, player_index):
        start_index = self.current_player_indices[0]
        for i in range(self.num_players):
            self.vector[start_index + i] = 0
        self.vector[start_index + player_index] = 1

    # def set_can_afford(self, player_index, card, required):
    #     index = self.card_progress_indices[(player_index, card)]
    #     self.vector[index:index + 5] = 0
    #     self.vector[index + min(required, 4)] = 1

    # def set_progress(self, player_index, tier, row_index, required):
    #     index = self.card_progress_indices[(player_index, tier, row_index)]
    #     self.vector[index:index + self.max_progress_possible[tier]] = 0
    #     self.vector[index + required] = 1

    # def set_available_score(self, player_index, tier, row_index, points):
    #     index = self.available_score_indices[(player_index, tier, row_index)]
    #     self.vector[index:index + 6] = 0
    #     self.vector[index + points - 1] = 1

    def set_noble_cost(self, *args):
        raise AttributeError('set_noble_cost is not currently available')

    def set_noble_remaining_cost(self, player_index, noble_index, colour, number):

        assert number in range(5) or number is None
        index = self.noble_cost_indices[(player_index, noble_index, colour)]
        self.vector[index:index + 5] = 0

        if number is not None:
            self.vector[index + number] = 1

    def set_noble_present(self, index, value):
        self.vector[self.nobles_present_index + index] = value

    def set_card_cost(self, tier, index, colour, cost):
        index = self.card_cost_indices[(tier, index, colour)]
        self.vector[index:index + self.tier_max_gems[tier]] = 0.
        self.vector[index + cost] = 1.
        # self.vector[index:index + cost + 1] = 1.

    def set_card_points(self, tier, index, points):
        index = self.card_points_indices[(tier, index)]
        self.vector[index:index + self.tier_max_points[tier] - self.tier_min_points[tier] + 1] = 0.
        self.vector[index + points] = 1.
        # self.vector[index:index + points + 1] = 1.

    def set_player_card_cost(self, player_index, card_index, colour, cost):
        index = self.player_card_cost_indices[(player_index, card_index, colour)]
        self.vector[index:index + 8] = 0.
        if cost is not None:
            self.vector[index + cost] = 1.
            # self.vector[index:index + cost + 1] = 1.

    def set_player_card_points(self, player_index, card_index, points):
        index = self.player_card_points_indices[(player_index, card_index)]
        self.vector[index:index + 6] = 0.
        if points is not None:
            self.vector[index + points] = 1.
            # self.vector[index:index + points + 1] = 1.

    def set_card_remaining_cost(self, player_index, tier_index, card_index, colour, number):
        index = self.card_remaining_cost_indices[(player_index, tier_index, card_index, colour)]
        num_zeros = {1: 5, 2: 7, 3: 8}[tier_index]
        self.vector[index:index + num_zeros] = 0
        if number is not None:
            # self.vector[index + number] = 1
            self.vector[index:index + number + 1] = 1

    def set_player_card_remaining_cost(self, player_index, card_index, colour, number):
        index = self.player_card_remaining_cost_indices[(player_index, card_index, colour)]
        num_zeros = 8
        self.vector[index:index + num_zeros] = 0
        if number is not None:
            # self.vector[index + number] = 1
            self.vector[index:index + number + 1] = 1

    def set_card_colour(self, tier_index, card_index, colour):
        index = self.card_colour_indices[(tier_index, card_index)]
        self.vector[index:index + len(colour_indices)] = 0
        if colour is not None:
            self.vector[index + colour_indices[colour]] = 1

    def set_player_card_colour(self, player_index, card_index, colour):
        index = self.player_card_colour_indices[(player_index, card_index)]
        self.vector[index:index + len(colour_indices)] = 0
        if colour is not None:
            self.vector[index + colour_indices[colour]] = 1

    def set_no_points_buys(self, player_index, number):
        number = min(number, 15)
        index = self.no_points_indices[player_index]
        self.vector[index:index + 16] = 0
        self.vector[index:index + number + 1] = 1

    def set_points_buys(self, player_index, number):
        number = min(number, 9)
        index = self.points_indices[player_index]
        self.vector[index:index + 10] = 0
        self.vector[index:index + number + 1] = 1
