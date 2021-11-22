# window name
WINDOW_NAME = 'POP3Client'

# encode type
encoding = 'utf-8'

# icon path
ICON_PATH = './icon.ico'

# Email address
MAILADDR = ''

# Password of email address
MAILPASS = ''

# POP3 server
POP3SERVER = ''

# Port of POP3 server
POP3PORT = ''

# retr number
RETRNUM = ''

# list number
LISTNUM = ''

# line terminator   (\r\n or \n) 
# (we always output CRLF, but accept any of CRLF, LFCR, LF)
CR = b'\r'
LF = b'\n'
CRLF = CR+LF

# maximal line length when calling readline(). This is to prevent
# reading arbitrary length lines. RFC 1939 limits POP3 line length to
# 512 characters, including CRLF. We have selected 2048 just to be on
# the safe side.
MAXLINE = 2048

