class IHandler(object):
   
    def handle(self, packet):
        pass


class Handler(IHandler):

    def handle(self, packet):
        print packet
