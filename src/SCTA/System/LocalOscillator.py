import logging

logger = logging.getLogger(__name__)

class LocalOscillator(object):

    def __init__(self, id='LO', freq=0):
        """Constructor.

        ~~~~~ Possibilities ~~~~~
        id:  string
        freq:        positive (float) [MHz]

        """
        self.id = id         # identifier string
        self.freq = freq     # LO freq