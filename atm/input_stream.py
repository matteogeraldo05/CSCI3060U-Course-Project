# reads input from the command line and from file
class InputStream:
    def __init__(self, srcPath):
        self.srcPath = srcPath
        self.file = None

        if srcPath:
            self.file = open(srcPath, "r")

    def readNextLine(self):
        try:
            if self.file:
                line = self.file.readline()
                if line:
                    # remove newline and return
                    line = line.rstrip('\n')
                    # so user can see what's being processed)
                    print(f"~{self.srcPath}> {line}")
                    return line
                else:
                    # end of file reached
                    self.file.close()
                    self.file = None
                    print("\n***End of file input***")
                    return input()
            return input()
        except KeyboardInterrupt:
            return "logout" 