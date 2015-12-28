class IHandler(object):
   
    def __init__(self, config):
        pass

    def handle(self, packet):
        pass


class Handler(IHandler):

    def handle(self, packet):
        print packet
