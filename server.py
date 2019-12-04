

class ProcessRequest:

    objType = []
    filename = ''

    def __init__(self, type):
        self.objType = type
        self.filename = r'C:\Users\S1M1\Desktop\Newfolder\trailer.mp4'


    def handleRequest(self):
        return self.filename
