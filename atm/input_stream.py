'''
The InputStream class manages all user input for the ATM Banking system.

This class is responsible for reading commands either from standard input
(interactive command line).

It safely captures interruptions to ensure controlled session termination.
'''

class InputStream:
    def __init__(self):
        pass
            
    '''
    Retrieves the next line of input for processing.

    If a file source is active, reads the next command from
    the file and echoes it to the console. When the end of
    the file is reached, switches to interactive input mode.
    '''

    def readNextLine(self):
        try:
            return input()
        except KeyboardInterrupt:
            return "logout" 