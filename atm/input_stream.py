class InputStream:
    def __init__(self, srcPath):
        self.srcPath = srcPath

    def readNextLine(self):
        return input()
