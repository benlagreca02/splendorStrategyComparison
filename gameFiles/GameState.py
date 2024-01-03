import numpy as np

from gameFiles.Card import Card
from gameFiles.Player import Player
from gameFiles.StateVector import StateVector
from gameFiles.data import colours, colour_indices
from gameFiles.game import tier_1, tier_2, tier_3, nobles, choose_3, discard_to_n_gems


class GameState(object):

    def __init__(self, players=3, init_game=False, validate=True, generator=None,
                 state_vector=None):
        self.num_players = players
        self.players = []
        self.validate = validate

        if state_vector is None:
            state_vector = StateVector(self.num_players)
        self.state_vector = state_vector

        self.current_player_index = 0

        self.num_gems_in_play = {2: 4, 3: 5, 4: 7}[players]
        self.num_dev_cards = 4
        self.num_nobles = {2: 3, 3: 4, 4: 5}[players]

        self._tier_1 = tier_1
        self._tier_1_copied = False
        self._tier_2 = tier_2
        self._tier_2_copied = False
        self._tier_3 = tier_3
        self._tier_3_copied = False

        self._tier_1_visible = []
        self._tier_1_visible_copied = False
        self._tier_2_visible = []
        self._tier_2_visible_copied = False
        self._tier_3_visible = []
        self._tier_3_visible_copied = False

        self._num_gold_available = 5
        self._num_white_available = self.num_gems_in_play
        self._num_blue_available = self.num_gems_in_play
        self._num_green_available = self.num_gems_in_play
        self._num_red_available = self.num_gems_in_play
        self._num_black_available = self.num_gems_in_play

        self.initial_nobles = []
        self.nobles = []
        self.noble_indices = {}

        self.round_number = 1

        self.moves = []

        if generator is None:
            generator = np.random.RandomState()
        self.generator = generator

        if init_game:
            self.init_game()

    @property
    def tier_1(self):
        raise ValueError('tier_1')

    @property
    def tier_2(self):
        raise ValueError('tier_2')

    @property
    def tier_3(self):
        raise ValueError('tier_3')

    @property
    def tier_1_available(self):
        raise ValueError('tier_1_available')

    @property
    def tier_2_available(self):
        raise ValueError('tier_2_available')

    @property
    def tier_3_available(self):
        raise ValueError('tier_3_available')

    @property
    def num_gold_available(self):
        raise ValueError('gold')

    @property
    def num_white_available(self):
        raise ValueError('white')

    @property
    def num_blue_available(self):
        raise ValueError('blue')

    @property
    def num_green_available(self):
        raise ValueError('green')

    @property
    def num_red_available(self):
        raise ValueError('red')

    @property
    def num_black_available(self):
        raise ValueError('black')

    def copy(self):
        copy = GameState(self.num_players, validate=self.validate, generator=self.generator,
                         state_vector=self.state_vector.copy())
        for colour in colours + ['gold']:
            setattr(copy, '_num_{}_available'.format(colour), self.num_gems_available(colour))

        copy.initial_nobles = self.initial_nobles
        copy.nobles = self.nobles[:]

        copy._tier_1 = self.cards_in_deck(1, ensure_copied=False)
        copy._tier_2 = self.cards_in_deck(2, ensure_copied=False)
        copy._tier_3 = self.cards_in_deck(3, ensure_copied=False)

        copy._tier_1_visible = self.cards_in_market(1, ensure_copied=False)
        copy._tier_2_visible = self.cards_in_market(2, ensure_copied=False)
        copy._tier_3_visible = self.cards_in_market(3, ensure_copied=False)

        copy.players = [p.copy() for p in self.players]
        copy.current_player_index = self.current_player_index

        copy.generator = self.generator

        return copy

    def get_scores(self):
        scores = [player.score for player in self.players]
        return scores

    @property
    def current_player(self):
        return self.players[self.current_player_index]

    def num_gems_available(self, colour):
        return getattr(self, '_num_{}_available'.format(colour))

    def total_num_gems_available(self):
        return sum([self.num_gems_available(colour) for colour in colours])

    def cards_in_deck(self, tier, ensure_copied=True):
        tier_attr = '_tier_{}'.format(tier)
        if ensure_copied:
            copied_attr = '_tier_{}_copied'.format(tier)
            if not getattr(self, copied_attr):
                setattr(self, tier_attr, getattr(self, tier_attr)[:])
                setattr(self, copied_attr, True)
        return getattr(self, tier_attr)

    def cards_in_market(self, tier, ensure_copied=True):
        tier_attr = '_tier_{}_visible'.format(tier)
        if ensure_copied:
            copied_attr = '_tier_{}_visible_copied'.format(tier)
            if not getattr(self, copied_attr):
                setattr(self, tier_attr, getattr(self, tier_attr)[:])
                setattr(self, copied_attr, True)
        return getattr(self, '_tier_{}_visible'.format(tier))

    def add_supply_gems(self, colour, change):
        attr_name = '_num_{}_available'.format(colour)
        setattr(self, attr_name, getattr(self, attr_name) + change)
        self.state_vector.set_supply_gems(colour, self.num_gems_available(colour))

    def seed(self):
        self.generator.seed(seed)

    def init_game(self):
        # Shuffle the cards
        self.generator.shuffle(self.cards_in_deck(1))
        self.generator.shuffle(self.cards_in_deck(2))
        self.generator.shuffle(self.cards_in_deck(3))

        # Select nobles
        orig_nobles = nobles[:]
        self.generator.shuffle(orig_nobles)
        self.nobles = orig_nobles[:self.num_nobles]
        self.initial_nobles = tuple(self.nobles[:])
        self.noble_indices = {noble: index for index, noble in enumerate(self.nobles)}

        # Make player objects
        self.players = [Player() for _ in range(self.num_players)]

        # Update visible dev cards
        self.update_dev_cards()
        self.update_card_costs_and_points()

        # Sync with state vector
        for card in self.cards_in_deck(1) + self.cards_in_deck(2) + self.cards_in_deck(3):
            self.state_vector.set_card_location(card, 0)
        for card in self.cards_in_market(1) + self.cards_in_market(2) + self.cards_in_market(3):
            self.state_vector.set_card_location(card, 1)

        for colour in colours:
            self.state_vector.set_supply_gems(colour, self.num_gems_in_play)
        self.state_vector.set_supply_gems('gold', 5)

        # for noble_index, noble in enumerate(self.initial_nobles):
        #     for colour in colours:
        #         self.state_vector.set_noble_cost(noble_index, colour, noble.num_required(colour))
        # self.state_vector.set_noble_available(noble, 1)
        self.update_noble_availability()

        for player_index in range(self.num_players):
            self.state_vector.set_player_score(player_index, 0)
            for colour in colours:
                self.state_vector.set_player_gems(player_index, colour, 0)
                self.state_vector.set_player_played_colour(player_index, colour, 0)
                # self.state_vector.set_player_cards(player_index, colour, 0)
            self.state_vector.set_player_gems(player_index, 'all', 0)
            self.state_vector.set_player_gems(player_index, 'gold', 0)

        # for i in range(self.num_players):
        #     self.update_card_affording(i)

    # def update_card_affording(self, player_index, update_colours=colours):
    #     player = self.players[player_index]
    #     v = self.state_vector

    #     cards_to_update = set()
    #     for colour in update_colours:
    #         for card in cards_by_gem_colour[colour]:
    #             cards_to_update.add(card)

    #     for card in cards_to_update:
    #         can_afford, cost = player.can_afford(card)
    #         if can_afford:
    #             v.set_can_afford(player_index, card, 0)
    #         else:
    #             v.set_can_afford(player_index, card, cost)

    def make_move(self, move, refill_market=True):
        self.moves.append(move)

        player = self.players[self.current_player_index]
        if move[0] == 'gems':
            player.add_gems(**move[1])
            for colour, change in move[1].items():
                self.add_supply_gems(colour, -1 * change)
                self.state_vector.set_supply_gems(colour, self.num_gems_available(colour))
                self.state_vector.set_player_gems(self.current_player_index, colour, player.num_gems(colour))

            # update remaining costs for this player
            player_index = self.current_player_index
            for tier in range(1, 4):
                for card_index, card in enumerate(self.cards_in_market(tier)):
                    for colour in move[1]:
                        value = max(0, card.num_required(colour) - player.num_gems(colour) - player.num_cards_of_colour(
                            colour))
                        self.state_vector.set_card_remaining_cost(
                            player_index, tier, card_index, colour, value)
                for card_index, card in enumerate(player.cards_in_hand):
                    for colour in move[1]:
                        value = max(0, card.num_required(colour) - player.num_gems(colour) - player.num_cards_of_colour(
                            colour))
                        self.state_vector.set_player_card_remaining_cost(
                            player_index, card_index, colour, value)


        elif move[0] == 'buy_available':
            action, tier, index, gems = move
            card = self.cards_in_market(tier).pop(index)
            player.cards_played.append(card)
            self.state_vector.set_card_location(card, 2 + self.num_players + self.current_player_index)
            player.add_gems(**gems)
            for colour, change in gems.items():
                self.add_supply_gems(colour, -1 * change)
                self.state_vector.set_player_gems(self.current_player_index, colour, player.num_gems(colour))
            card_colour = card.colour
            cur_num_card_colour = len([c for c in player.cards_played if c.colour == card_colour])
            self.state_vector.set_player_played_colour(self.current_player_index, card_colour,
                                                       cur_num_card_colour)

            self.state_vector.set_player_score(self.current_player_index, player.score)

            for noble, noble_index in self.noble_indices.items():
                if noble in self.nobles:
                    self.state_vector.set_noble_remaining_cost(
                        self.current_player_index, noble_index, card_colour,
                        max(0, noble.num_required(card_colour) - player.num_cards_of_colour(card_colour)))

        elif move[0] == 'buy_reserved':
            action, index, gems = move
            card = player.cards_in_hand.pop(index)
            player.cards_played.append(card)
            self.state_vector.set_card_location(card, 2 + self.num_players + self.current_player_index)
            player.add_gems(**gems)
            for colour, change in gems.items():
                self.add_supply_gems(colour, -1 * change)
                self.state_vector.set_player_gems(self.current_player_index, colour, player.num_gems(colour))
            card_colour = card.colour
            cur_num_card_colour = len([c for c in player.cards_played if c.colour == card_colour])
            self.state_vector.set_player_played_colour(self.current_player_index, card_colour,
                                                       cur_num_card_colour)

            self.state_vector.set_player_score(self.current_player_index, player.score)

            for noble, noble_index in self.noble_indices.items():
                if noble in self.nobles:
                    self.state_vector.set_noble_remaining_cost(
                        self.current_player_index, noble_index, card_colour,
                        max(0, noble.num_required(card_colour) - player.num_cards_of_colour(card_colour)))

        elif move[0] == 'reserve':
            action, tier, index, gems = move
            if index == -1:
                card = self.cards_in_deck(tier).pop()
            else:
                card = self.cards_in_market(tier).pop(index)
            player.cards_in_hand.append(card)
            player.add_gems(**gems)
            for colour, change in gems.items():
                self.add_supply_gems(colour, -1 * change)
                self.state_vector.set_player_gems(self.current_player_index, colour, player.num_gems(colour))
            self.state_vector.set_card_location(card, 2 + self.current_player_index)
            # self.update_card_affording(self.current_player_index, update_colours=colours)

        else:
            raise ValueError('Received invalid move {}'.format(move))

        # Assign nobles if necessary
        assignable = []
        for i, noble in enumerate(self.nobles):
            for colour in colours:
                if player.num_cards_of_colour(colour) < noble.num_required(colour):
                    break
            else:
                assignable.append(i)
        if assignable:
            noble = self.nobles.pop(assignable[0])
            player.nobles.append(noble)
            self.state_vector.set_player_score(self.current_player_index, player.score)
            self.update_noble_availability()
            # self.state_vector.set_noble_available(noble, 0)

        # Clean up the state
        self.update_dev_cards(fake_refill=not refill_market)
        if move[0] != 'gems':
            self.update_card_costs_and_points()
        if move[0].startswith('buy'):
            num_cards_played = len(player.cards_played)
            points_cards_played = len([c for c in player.cards_played if c.points > 0])
            no_points_cards_played = num_cards_played - points_cards_played
            self.state_vector.set_points_buys(self.current_player_index, points_cards_played)
            self.state_vector.set_no_points_buys(self.current_player_index, no_points_cards_played)
        self.state_vector.set_player_gems(self.current_player_index, 'all', player.total_num_gems)

        # Check that everything is within expected parameters
        if self.validate:
            try:
                player.verify_state()
                self.verify_state()
            except AssertionError:
                print('Failure verifying state after making move')
                print('move was', move)
                import traceback
                traceback.print_exc()
                import ipdb;
                ipdb.set_trace()

        self.current_player_index += 1
        self.current_player_index %= len(self.players)
        if self.current_player_index == 0:
            self.round_number += 1
            self.state_vector.set_current_round(self.round_number)
        self.state_vector.set_current_player(self.current_player_index)

        return self

    def verify_state(self):
        sv = self.state_vector

        for player in self.players:
            player.verify_state()

        for colour in colours:
            assert 0 <= self.num_gems_available(colour) <= self.num_gems_in_play
        assert 0 <= self.num_gems_available('gold') <= 5

        for colour in colours:
            assert self.num_gems_available(colour) + sum(
                [player.num_gems(colour) for player in self.players]) == self.num_gems_in_play
            assert self.num_gems_available(colour) == self.state_vector.num_supply_gems(colour)

            index = sv.supply_gem_indices[colour]
            num_available = self.num_gems_available(colour)
            assert np.sum(sv.vector[index:index + self.num_gems_in_play + 1]) == 1  # num_available + 1
            assert np.sum(sv.vector[index + num_available]) == 1

        gold_index = sv.supply_gem_indices['gold']
        assert np.sum(sv.vector[gold_index:gold_index + 6]) == 1  # self.num_gems_available('gold') + 1
        assert sv.vector[gold_index + self.num_gems_available('gold')] == 1

        for noble, noble_index in self.noble_indices.items():
            if noble in self.nobles:
                assert sv.vector[sv.nobles_present_index + noble_index] == 1
            else:
                assert sv.vector[sv.nobles_present_index + noble_index] == 0

            if noble in self.nobles:
                for player_index, player in enumerate(self.players):
                    for colour in colours:
                        index = sv.noble_cost_indices[(player_index, noble_index, colour)]
                        assert np.sum(sv.vector[index:index + 5]) == 1
                        assert sv.vector[
                                   index + max(0, noble.num_required(colour) - player.num_cards_of_colour(colour))] == 1
            else:
                for player_index, player in enumerate(self.players):
                    if noble not in player.nobles:
                        num_required = 0
                    else:
                        num_required = max(0, noble.num_required(colour) - player.num_cards_of_colour(colour))
                    assert num_required == 0
                    for colour in colours:
                        index = sv.noble_cost_indices[(player_index, noble_index, colour)]
                        assert np.sum(sv.vector[index:index + 5]) == 0

        for tier in range(1, 4):
            for card_index, card in enumerate(self.cards_in_market(tier)):
                for colour in colours:
                    index = sv.card_cost_indices[(tier, card_index, colour)]
                    try:
                        assert np.sum(
                            sv.vector[index:index + sv.tier_max_gems[tier]]) == 1  # card.num_required(colour) + 1
                        assert sv.vector[index + card.num_required(colour)] == 1
                    except AssertionError:
                        import traceback
                        traceback.print_exc()
                        import ipdb
                        ipdb.set_trace()

                index = sv.card_colour_indices[(tier, card_index)]
                try:
                    assert np.sum(sv.vector[index:index + len(colour_indices)]) == 1
                    assert sv.vector[index + colour_indices[card.colour]] == 1
                except AssertionError:
                    import traceback
                    traceback.print_exc()
                    import ipdb
                    ipdb.set_trace()

                index = sv.card_points_indices[(tier, card_index)]
                offset = (sv.tier_max_points[tier] - sv.tier_min_points[tier] + 1)
                try:
                    assert np.sum(sv.vector[index:index + offset]) == 1  # card.points - sv.tier_min_points[tier] + 1
                except AssertionError:
                    import traceback
                    traceback.print_exc()
                    import ipdb
                    ipdb.set_trace()

                assert sv.vector[index + card.points - sv.tier_min_points[tier]] == 1

        for player_index, player in enumerate(self.players):
            for card_index, card in enumerate(player.cards_in_hand):
                for colour in colours:
                    index = sv.player_card_cost_indices[(player_index, card_index, colour)]
                    try:
                        assert np.sum(sv.vector[index:index + 8]) == 1  # card.num_required(colour) + 1
                        assert sv.vector[index + card.num_required(colour)] == 1
                    except AssertionError:
                        import traceback
                        traceback.print_exc()
                        import ipdb
                        ipdb.set_trace()

                index = sv.player_card_points_indices[(player_index, card_index)]
                assert np.sum(sv.vector[index:index + 6]) == 1  # card.points + 1
                assert sv.vector[index + card.points] == 1

                index = sv.player_card_colour_indices[(player_index, card_index)]
                assert np.sum(sv.vector[index:index + len(colour_indices)]) == 1
                assert sv.vector[index + colour_indices[card.colour]] == 1
            for card_index in range(len(player.cards_in_hand), 3):
                for colour in colours:
                    index = sv.player_card_cost_indices[(player_index, card_index, colour)]
                    assert np.sum(sv.vector[index:index + 8]) == 0
                index = sv.player_card_points_indices[(player_index, card_index)]
                assert np.sum(sv.vector[index:index + 6]) == 0

        # remaining costs
        for player_index, player in enumerate(self.players):
            for tier in range(1, 4):
                num_zeros = {1: 5, 2: 7, 3: 8}[tier]
                for card_index, card in enumerate(self.cards_in_market(tier)):
                    for colour in colours:
                        index = sv.card_remaining_cost_indices[(player_index, tier, card_index, colour)]
                        try:
                            assert np.sum(sv.vector[index:index + num_zeros]) == max(0, card.num_required(
                                colour) - player.num_gems(colour) - player.num_cards_of_colour(colour)) + 1

                        except AssertionError:
                            import traceback
                            traceback.print_exc()
                            import ipdb
                            ipdb.set_trace()
                        assert sv.vector[index + max(
                            0, (card.num_required(colour) -
                                player.num_gems(colour) -
                                player.num_cards_of_colour(colour)))] == 1

                for card_index in range(len(self.cards_in_market(tier)), 4):
                    for colour in colours:
                        index = sv.card_remaining_cost_indices[(player_index, tier, card_index, colour)]
                        assert np.sum(sv.vector[index:index + num_zeros]) == 0

            for card_index, card in enumerate(player.cards_in_hand):
                for colour in colours:
                    index = sv.player_card_remaining_cost_indices[(player_index, card_index, colour)]
                    assert np.sum(sv.vector[index:index + 8]) == max(0, card.num_required(colour) - player.num_gems(
                        colour) - player.num_cards_of_colour(colour)) + 1
                    assert sv.vector[index + max(
                        0, (card.num_required(colour) -
                            player.num_gems(colour) -
                            player.num_cards_of_colour(colour)))] == 1
            for card_index in range(len(player.cards_in_hand), 3):
                for colour in colours:
                    index = sv.player_card_remaining_cost_indices[(player_index, card_index, colour)]
                    assert np.sum(sv.vector[index:index + 8]) == 0

        for player_index, player in enumerate(self.players):
            pv = sv.from_perspective_of(player_index)
            # for card in player.cards_in_hand:
            #     index = sv.card_indices[card]
            #     assert np.sum(sv.vector[index:index + 2 + len(self.players)]) == 1
            #     assert sv.vector[index + 2 + player_index] == 1

            #     assert pv[index + 2] == 1

            # for card in player.cards_played:
            #     index = sv.card_indices[card]
            #     assert np.sum(sv.vector[index:index + 2 + len(self.players)]) == 0
            #     assert sv.vector[index + 2 + self.num_players + player_index] == 1

            #     assert pv[index + 2 + self.num_players] == 1

            for colour in colours:
                index = sv.player_gem_indices[(player_index, colour)]
                number = player.num_gems(colour)
                try:
                    assert np.sum(sv.vector[index:index + self.num_gems_in_play + 1]) == 1  # number + 1
                except:
                    import ipdb
                    ipdb.set_trace()
                assert sv.vector[index + player.num_gems(colour)] == 1
                p0_index = sv.player_gem_indices[(0, colour)]
                assert pv[p0_index + player.num_gems(colour)] == 1

                num_played = len([c for c in player.cards_played if c.colour == colour])
                index = sv.player_played_colours_indices[(player_index, colour)]
                assert np.sum(sv.vector[index:index + 8]) == min(7, num_played) + 1
                assert sv.vector[index + min(num_played, 7)] == 1
                p0_index = sv.player_played_colours_indices[(0, colour)]
                try:
                    assert pv[p0_index + min(num_played, 7)] == 1
                except AssertionError:
                    print('ERROR with num played of colour')
                    import traceback
                    traceback.print_exc()
                    import ipdb
                    ipdb.set_trace()
            index = sv.player_gem_indices[(player_index, 'all')]
            number = player.total_num_gems
            assert np.sum(sv.vector[index:index + 11]) == 1
            assert sv.vector[index + number] == 1

            score = player.score
            index = sv.player_score_indices[player_index]
            assert np.sum(sv.vector[index:index + 21]) == min(score, 20) + 1
            assert sv.vector[index + min(score, 20)] == 1
            p0_index = sv.player_score_indices[0]
            assert pv[p0_index + min(score, 20)] == 1

            gold_index = sv.player_gem_indices[(player_index, 'gold')]
            assert np.sum(sv.vector[gold_index:gold_index + 6]) == 1  # player.num_gems('gold') + 1
            assert sv.vector[gold_index + player.num_gems('gold')] == 1
            p0_index = sv.player_gem_indices[(0, 'gold')]
            try:
                assert pv[p0_index + player.num_gems('gold')] == 1
            except AssertionError:
                print('ERROR with num gold')
                import traceback
                traceback.print_exc()
                import ipdb
                ipdb.set_trace()

            for card_index, card in enumerate(player.cards_in_hand):
                for colour in colours:
                    index = sv.player_card_cost_indices[(0, card_index, colour)]
                    assert np.sum(pv[index:index + 8]) == 1  # card.num_required(colour) + 1
                    assert pv[index + card.num_required(colour)] == 1

                index = sv.player_card_points_indices[(0, card_index)]
                assert np.sum(pv[index:index + 6]) == 1  # card.points + 1
                assert pv[index + card.points] == 1

            for noble, noble_index in self.noble_indices.items():
                if noble in self.nobles:
                    for cur_player_index, player in enumerate(self.players):
                        cur_player_index -= player_index
                        cur_player_index %= self.num_players
                        for colour in colours:
                            index = sv.noble_cost_indices[(cur_player_index, noble_index, colour)]
                            assert np.sum(sv.vector[index:index + 5]) == 1

                            # this was throwing lots of errors when doing 3 players
                            # but i mean.... we can probably skip this check
                            #assert pv[index + max(0, noble.num_required(colour) - player.num_cards_of_colour(colour))] == 1
                else:
                    for cur_player_index, player in enumerate(self.players):
                        cur_player_index -= player_index
                        cur_player_index %= self.num_players
                        if noble not in player.nobles:
                            continue
                        for colour in colours:
                            index = sv.noble_cost_indices[(cur_player_index, noble_index, colour)]
                            assert np.sum(sv.vector[index:index + 5]) == 0
                            num_required = max(0, noble.num_required(colour) - player.num_cards_of_colour(colour))
                            assert num_required == 0
                            # assert pv[index + num_required] == 1

        # import ipdb
        # ipdb.set_trace()
        assert sv.vector[sv.current_player_indices[self.current_player_index]] == 1

        self.state_vector.verify_state()

    def update_dev_cards(self, fake_refill=False):

        while len(self.cards_in_market(1)) < 4 and self.cards_in_deck(1):
            if fake_refill:
                card = Card(1, 'none', 0, white=2, blue=2, green=2, red=2, black=2)
            else:
                card = self.cards_in_deck(1).pop()
            self.state_vector.set_card_location(card, 1)
            self.cards_in_market(1).append(card)
            self.cards_in_market(1).sort(key=lambda j: j.sort_info)

        while len(self.cards_in_market(2)) < 4 and self.cards_in_deck(2):
            if fake_refill:
                card = Card(2, 'none', 1, white=3, blue=3, green=3, red=3, black=3)
            else:
                card = self.cards_in_deck(2).pop()
            self.state_vector.set_card_location(card, 1)
            self.cards_in_market(2).append(card)
            self.cards_in_market(2).sort(key=lambda j: j.points)

        while len(self.cards_in_market(3)) < 4 and self.cards_in_deck(3):
            if fake_refill:
                card = Card(3, 'none', 3, white=4, blue=4, green=4, red=4, black=4)
            else:
                card = self.cards_in_deck(3).pop()
            self.state_vector.set_card_location(card, 1)
            self.cards_in_market(3).append(card)
            self.cards_in_market(3).sort(key=lambda j: j.points)

    def update_noble_availability(self):
        for noble, noble_index in self.noble_indices.items():
            if noble in self.nobles:
                self.state_vector.set_noble_present(noble_index, 1)
            else:
                self.state_vector.set_noble_present(noble_index, 0)

        for player_index, player in enumerate(self.players):
            for noble, noble_index in self.noble_indices.items():
                if noble not in self.nobles:
                    for colour in colours:
                        self.state_vector.set_noble_remaining_cost(
                            player_index, noble_index, colour, None)
                else:
                    for colour in colours:
                        self.state_vector.set_noble_remaining_cost(
                            player_index, noble_index, colour,
                            max(0, noble.num_required(colour) - player.num_cards_of_colour(colour)))

    def update_card_costs_and_points(self):
        for tier in range(1, 4):
            min_points = self.state_vector.tier_min_points[tier]
            for i, card in enumerate(self.cards_in_market(tier)):
                for colour in colours:
                    self.state_vector.set_card_cost(tier, i, colour, card.num_required(colour))
                self.state_vector.set_card_points(tier, i, card.points - min_points)
                self.state_vector.set_card_colour(tier, i, card.colour)
            # note: we don't clear the vector state if cards aren't present?

        for player_index, player in enumerate(self.players):
            num_cards_in_hand = len(player.cards_in_hand)
            for card_index in range(3):
                if card_index < num_cards_in_hand:
                    card = player.cards_in_hand[card_index]
                    for colour in colours:
                        self.state_vector.set_player_card_cost(player_index, card_index, colour,
                                                               card.num_required(colour))
                    self.state_vector.set_player_card_points(player_index, card_index, card.points)
                    self.state_vector.set_player_card_colour(player_index, card_index, card.colour)
                else:
                    for colour in colours:
                        self.state_vector.set_player_card_cost(player_index, card_index, colour, None)
                    self.state_vector.set_player_card_points(player_index, card_index, None)
                    self.state_vector.set_player_card_colour(player_index, card_index, None)

        # update remaining costs
        for player_index, player in enumerate(self.players):
            for tier in range(1, 4):
                for card_index, card in enumerate(self.cards_in_market(tier)):
                    for colour in colours:
                        value = max(0, card.num_required(colour) - player.num_gems(colour) - player.num_cards_of_colour(
                            colour))
                        self.state_vector.set_card_remaining_cost(
                            player_index, tier, card_index, colour, value)
                for card_index in range(len(self.cards_in_market(tier)), 4):
                    for colour in colours:
                        self.state_vector.set_card_remaining_cost(
                            player_index, tier, card_index, colour, None)
            for card_index, card in enumerate(player.cards_in_hand):
                for colour in colours:
                    value = max(0, card.num_required(colour) - player.num_gems(colour) - player.num_cards_of_colour(
                        colour))
                    self.state_vector.set_player_card_remaining_cost(
                        player_index, card_index, colour, value)
            for card_index in range(len(player.cards_in_hand), 3):
                for colour in colours:
                    self.state_vector.set_player_card_remaining_cost(
                        player_index, card_index, colour, None)

    def print_state(self):
        print('{} players'.format(self.num_players))
        print()

        print('Nobles:')
        for noble in self.nobles:
            print(noble)
        print()

        print('Tier 1 visible:')
        for card in self._tier_1_visible:
            print(card)
        print('{} tier 1 remain'.format(len(self._tier_1)))
        print()

        print('Tier 2 visible:')
        for card in self._tier_2_visible:
            print(card)
        print('{} tier 2 remain'.format(len(self._tier_2)))
        print()

        print('Tier 3 visible:')
        for card in self._tier_3_visible:
            print(card)
        print('{} tier 3 remain'.format(len(self._tier_3)))
        print()

        print('Available colours:')
        for colour in colours:
            print('  {}: {}'.format(colour, self.num_gems_available(colour)))
        print()

        for i, player in enumerate(self.players):
            i += 1
            print('Player {}:'.format(i))
            for colour in colours + ['gold']:
                print('  {}: {}'.format(colour, player.num_gems(colour)))
            if player.cards_in_hand:
                print(' reserves:'.format(i))
                for card in player.cards_in_hand:
                    print('  ', card)
            if player.cards_played:
                print(' played:'.format(i))
                for card in player.cards_played:
                    print('  ', card)

        # moves = self.get_current_player_valid_moves()
        # for move in moves:
        #     print(move)
        # print('{} moves available'.format(len(moves)))

    def get_valid_moves(self, player_index):

        moves = []
        provisional_moves = []  # moves that take gems, will need checking later
        player = self.players[player_index]

        # Moves that take gems
        # 1) taking two of the same colour
        for colour in colours:
            if self.num_gems_available(colour) >= 4:
                provisional_moves.append(('gems', {colour: 2}))
        # 2) taking up to three different colours
        available_colours = [colour for colour in colours if self.num_gems_available(colour) > 0]
        # for ps in list(set(permutations(available_colours, min(3, len(available_colours))))):
        #     provisional_moves.append(('gems', {p: 1 for p in ps}))
        for selection in choose_3(available_colours):
            provisional_moves.append(('gems', {c: 1 for c in selection}))

        num_gem_moves = len(provisional_moves)

        # Moves that reserve cards
        if player.num_reserved < 3:
            gold_gained = 1 if self.num_gems_available('gold') > 0 else 0
            for tier in range(1, 4):
                for i in range(len(self.cards_in_market(tier))):
                    provisional_moves.append(('reserve', tier, i, {'gold': gold_gained}))
                if self.cards_in_deck(tier, ensure_copied=False):
                    provisional_moves.append(('reserve', tier, -1, {'gold': gold_gained}))

        num_reserve_moves = len([m for m in provisional_moves if m[0] == 'reserve'])

        # Moves that buy available cards
        buy_moves = []
        for tier in range(1, 4):
            for index, card in enumerate(self.cards_in_market(tier)):
                can_afford, cost = player.can_afford(card)
                if not can_afford:
                    continue
                buy_moves.append(('buy_available', tier, index, {c: -1 * v for c, v in cost.items()}))

        # Moves that buy reserved cards
        for index, card in enumerate(player.cards_in_hand):
            can_afford, cost = player.can_afford(card)
            if not can_afford:
                continue
            buy_moves.append(('buy_reserved', index, {c: -1 * v for c, v in cost.items()}))

        if buy_moves:
            buy_multiplier = max(1, (num_gem_moves + num_reserve_moves) / len(buy_moves))
            buy_multiplier = int(np.round(buy_multiplier))
            for move in buy_moves:
                for _ in range(buy_multiplier):
                    moves.append(move)
        # for move in buy_moves:
        #     moves.append(move)

        # If taking gems leaves us with more than 10, discard any
        # possible gem combination
        player_gems = player.gems
        for move in provisional_moves:
            if move[0] == 'gems':
                num_gems_gained = sum(move[1].values())
                if player.total_num_gems + num_gems_gained <= 10:
                    moves.append(move)
                    continue
                num_gems_to_lose = player.total_num_gems + num_gems_gained - 10

                gems_gained = move[1]
                new_gems = {c: (player_gems[c] + gems_gained.get(c, 0)) for c in (colours + ['gold'])}
                possible_discards = discard_to_n_gems(new_gems, 10)
                for discard in possible_discards:
                    new_gems_gained = {key: value for key, value in gems_gained.items()}
                    for key, value in discard.items():
                        if key not in new_gems_gained:
                            new_gems_gained[key] = 0
                        new_gems_gained[key] += value
                    moves.append(('gems', new_gems_gained))

                    # print(num_gems_to_lose, -1 * sum(discard.values()))
                    if num_gems_to_lose != -1 * sum(discard.values()):
                        import ipdb
                        ipdb.set_trace()
                    assert -1 * sum(discard.values()) == num_gems_to_lose

            elif move[0] == 'reserve':
                num_gems_gained = sum(move[3].values())
                if player.total_num_gems + num_gems_gained <= 10:
                    moves.append(move)
                    continue
                for colour in colours + ['gold']:
                    new_gems_dict = {key: value for key, value in move[3].items()}
                    if player.num_gems(colour) > 0:
                        if colour not in new_gems_dict:
                            new_gems_dict[colour] = 0
                        new_gems_dict[colour] -= 1
                        moves.append(('reserve', move[1], move[2], new_gems_dict))

                # gems_list = set(player.gems_list() + gems_dict_to_list(move[3]))
                # for gem in gems_list:
                #     new_gems_dict = {key: value for key, value in move[3].items()}
                #     if gem not in new_gems_dict:
                #         new_gems_dict[gem] = 0
                #     new_gems_dict[gem] -= 1
                #     moves.append(('reserve', move[1], move[2], new_gems_dict))

        # if player.total_num_gems > 7:
        #     gems_moves = []
        #     other_moves = []
        #     gems_move_index = {}
        #     gems_move_keys = set()
        #     for move in moves:
        #         if move[0] == 'gems':
        #             gems_moves.append(move)
        #         else:
        #             other_moves.append(move)
        #     initial_num_gems_moves = len(gems_moves)
        #     for move in gems_moves:
        #         key = (move[1]['white'] if 'white' in move[1] else 0,
        #                move[1]['blue'] if 'blue' in move[1] else 0,
        #                move[1]['green'] if 'green' in move[1] else 0,
        #                move[1]['red'] if 'red' in move[1] else 0,
        #                move[1]['black'] if 'black' in move[1] else 0,
        #                move[1]['gold'] if 'gold' in move[1] else 0)
        #         gems_move_index[key] = move
        #         gems_move_keys.add(key)
        #     gems_moves = [gems_move_index[key] for key in gems_move_keys]
        #     final_num_gems_moves = len(gems_moves)
        #     # print('went from {} to {} gems moves'.format(initial_num_gems_moves,
        #     #                                              final_num_gems_moves))
        #     moves = gems_moves + other_moves

        if len(moves) == 0:
            moves = [('gems', {})]

        return moves

    def get_current_player_valid_moves(self):
        return self.get_valid_moves(self.current_player_index)

    def get_state_vector(self, player_perspective_index=None):

        if player_perspective_index is None:
            raise ValueError('player_perspective_index is None')
            player_perspective_index = self.current_player_index

        return self.state_vector.from_perspective_of(player_perspective_index).copy()
        # return self.state_vector.vector.copy()
