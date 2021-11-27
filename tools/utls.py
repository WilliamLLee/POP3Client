import socket as sk

from config.config  import CRLF, CR, MAXLINE


def get_ip_address(hostname=None):
    '''
    Get the IP address of the hostname.
    hostname: the hostname of the target.
    '''
    assert(hostname is not None)
    try:
        ip_address = sk.gethostbyname(hostname)
    except sk.gaierror:
        ip_address = 'Unknown'
    return ip_address


class error_proto(Exception):
    pass

class POP3:
    '''
        this class supports the minimal command sets of pop3 protocol.
        Arguments can be strings or integers (where appropriate)
        (e.g.: retr(1) and retr('1')) both work equally well.

        Minimal Command Set:
            USER name       user(name)
            PASS string     pass_(string)
            STAT            state()
            LIST [msg]      list(msg = None)
            RETR msg        retr(msg)
            QUIT            quit()

        Raises one exception: 'error_proto'

        Instantiate with 
            POP3(hostname, port=110)
    '''

    def __init__(self, hostname, port=110, is_debug=False, encoding = 'utf-8', timeout=50):
        self.__hostname = hostname
        self.__port = port
        self.__socket = self._create_socket(timeout)
        self.__file = self.__socket.makefile('rb')
        self.__debugging = is_debug
        self.__state = 'DISCONNECTED'
        self.__debugging = is_debug
        self.__encoding = encoding
        self.welcome = self._getresp()  # welcome message

    def _create_socket(self, timeout):
        return sk.create_connection((self.__hostname, self.__port), timeout)

    def _putline(self, line):
        if self.__debugging: print('>>>', repr(line))
        self.__socket.sendall(line + CRLF)

    def _putcmd(self, line):
        if self.__debugging: print('>>>', repr(line))
        line  = bytes(line, self.__encoding)
        self._putline(line)

    def _get_line(self):
        line = self.__file.readline(MAXLINE + 1)
        if len(line) > MAXLINE:
            raise ValueError('line too long')

        if self.__debugging: print('<<<', repr(line))

        if not line: raise EOFError


        octets = len(line)  # bytes in line
        # Strip trailing CRLF
        if line[-2:] == CRLF:
            return line[:-2].decode(self.__encoding), octets
        if line[:1] == CR:
            return line[1:-1].decode(self.__encoding), octets
        return line[:-1].decode(self.__encoding), octets

    def _getresp(self):
        # Read the response code, the result code, and the rest.
        # We are looking for a line that starts with '+OK'
        resp, o = self._get_line()
        if self.__debugging: print('<<<', repr(resp))
        if not resp.startswith('+OK'):
            raise error_proto(resp)
        return resp

    def _getlongresp(self):
        resp = self._getresp()
        list = []; octets = 0
        line, o = self._get_line()
        while line != '.':
            if line.startswith('..'):
                o = o-1
                line = line[1:]
            octets = octets + o
            list.append(line)
            line, o = self._get_line()
        return resp, list, octets  # the octets means the number of bytes in the message

    def _shortcmd(self, line):
        self._putcmd(line)
        return self._getresp()

    def _longcmd(self, line):
        self._putcmd(line)
        return self._getlongresp()

    # get welcome message
    def getwelcome(self):
        return self.welcome

    def set_debug(self, is_debug):
        self.__debugging = is_debug

    def user(self, user):
        return self._shortcmd('USER %s' % user)

    def pass_(self, pswd):
        return self._shortcmd('PASS %s' % pswd)

    def stat(self):
        return self._shortcmd('STAT')
    def retr(self, msg):
        return self._longcmd('RETR %s' % msg)

    def list(self, msg = None):
        if msg is None:
            return self._longcmd('LIST')
        return self._shortcmd('LIST %s' % msg)
    
    def quit(self):
        resp = self._shortcmd('QUIT')
        if self.__socket:
            self.__socket.close()
            del self.__socket
        return resp
        


    
if __name__ == '__main__':
    '''
        test code
    '''
    pass

