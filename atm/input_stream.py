'''
The InputStream class manages all user input for the ATM Banking system.

This class is responsible for reading commands either from standard input
(interactive command line) or from a provided file source. It allows the
system to operate in both interactive mode and automated file-driven mode.

It maintains the current input source state, handles end-of-file transitions,
echoes file-based commands for visibility, and safely captures interruptions
to ensure controlled session termination.
'''

class InputStream:
    def __init__(self, srcPath):
        self.srcPath = srcPath
        self.file = None

        if srcPath:
            self.file = open(srcPath, "r")
            
    '''
    Retrieves the next line of input for processing.

    If a file source is active, reads the next command from
    the file and echoes it to the console. When the end of
    the file is reached, switches to interactive input mode.
    '''

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