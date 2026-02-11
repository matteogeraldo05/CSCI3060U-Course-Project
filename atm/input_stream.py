# reads input from the command line
class InputStream:
    def __init__(self, srcPath):
        self.srcPath = srcPath

    def readNextLine(self):
        try:
            return input()
        except KeyboardInterrupt:
            return "exit" 