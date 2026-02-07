class OutputStream:
    def __init__(self, srcPath):
        self.srcPath = srcPath

    def write(self, message):
        print(message)
