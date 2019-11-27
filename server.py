

class ProcessRequest:

    objType = []
    filename = ''

    def __init__(self, type):
        self.objType = type
        self.filename = '/Users/rohit/Documents/SBU/Sem1/FCN/Project/test.txt'


    def handleRequest(self):
        return self.filename