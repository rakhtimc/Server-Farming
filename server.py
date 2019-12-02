

class ProcessRequest:

    objType = []
    filename = ''

    def __init__(self, type):
        self.objType = type
        self.filename = r"C:\Users\Rakhtim Chatterjee\Desktop\adss.txt"


    def handleRequest(self):
        return self.filename