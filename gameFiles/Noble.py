class Noble(object):
    def __init__(self, points=3, white=0, blue=0, green=0, red=0, black=0):
        self.points = points

        self.white = white
        self.blue = blue
        self.green = green
        self.red = red
        self.black = black

    def num_required(self, colour):
        return getattr(self, colour)

    def __str__(self):
        return '<Noble {}>'.format(','.join(
                ['{}:{}'.format(colour, self.num_required(colour)) for colour in
                 ('white', 'blue', 'green', 'red', 'black') if self.num_required(colour)]))

    def __repr__(self):
        return str(self)
