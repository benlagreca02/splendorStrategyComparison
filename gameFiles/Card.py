class Card(object):
    def __init__(
            self, tier, colour, points, white=0, blue=0,
            green=0, red=0, black=0):
        self.colour = colour
        self.points = points
        self.tier = tier

        self.white = white
        self.blue = blue
        self.green = green
        self.red = red
        self.black = black

    @property
    def requirements(self):
        return (self.white, self.blue, self.green, self.red, self.black)

    def num_required(self, colour):
        return getattr(self, colour)

    @property
    def total_num_required(self):
        return sum(self.requirements)

    @property
    def sort_info(self):
        return (self.points, self.white, self.blue, self.green, self.black)

    def __str__(self):
        return '<Card T={} C={} P={} {}>'.format(
            self.tier, self.colour, self.points, ','.join(
                ['{}:{}'.format(colour, self.num_required(colour)) for colour in
                 ('white', 'blue', 'green', 'red', 'black') if self.num_required(colour)]))

    def __repr__(self):
        return str(self)
