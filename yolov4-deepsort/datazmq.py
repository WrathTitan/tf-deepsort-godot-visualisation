import zmq
import numpy as np

class JSONSender():
    """Opens a zmq socket and sends data

    Opens a zmq (REQ or PUB) socket on the data sending computer, 
    that will be sending data to the hub computer. Provides methods to
    send data.

    Two kinds of ZMQ message patterns are possible:
    REQ/REP: data is sent and the sender waits for a reply ("blocking").
    PUB/SUB: data is sent and no reply is sent or expected ("non-blocking").

    There are advantabes and disadvantages for each message pattern.
    See the documentation for a full description of REQ/REP and PUB/SUB.
    The default is REQ/REP for the JSONSender class and the JSONHub class.

    Arguments:
      connect_to: the tcp address:port of the hub computer.
      REQ_REP: (optional) if True (the default), a REQ socket will be created
                          if False, a PUB socket will be created
    """

    def __init__(self, connect_to='tcp://127.0.0.1:5555', REQ_REP = True):
        """Initializes zmq socket for sending data to the hub.

        Expects an appropriate ZMQ socket at the connect_to tcp:port address:
        If REQ_REP is True (the default), then a REQ socket is created. It
        must connect to a matching REP socket on the JSONHub().

        If REQ_REP = False, then a PUB socket is created. It must connect to
        a matching SUB socket on the JSONHub().
        """

        if REQ_REP == True:
             # REQ/REP mode, this is a blocking scenario
             self.init_reqrep(connect_to)
        else:
             #PUB/SUB mode, non-blocking scenario
             self.init_pubsub(connect_to)

    def init_reqrep(self, address):
        """ Creates and inits a socket in REQ/REP mode
        """
        socketType = zmq.REQ
        self.zmq_context = zmq.Context()
        self.zmq_socket = self.zmq_context.socket(socketType)
        self.zmq_socket.connect(address)

        self.send_data = self.send_data_reqrep

    def send_data_reqrep(self, msg, data):
        self.zmq_socket.send_json(data)
        hub_reply = self.zmq_socket.recv()  # receive the reply message
        return hub_reply

    def init_pubsub(self, address):
        """Creates and inits a socket in PUB/SUB mode
        """
        socketType = zmq.PUB
        self.zmq_context = zmq.Context()
        self.zmq_socket = self.zmq_context.socket(socketType)
        self.zmq_socket.bind(address)

        self.send_data = self.send_data_pubsub

    def send_data_pubsub(self, msg, data):
        self.zmq_socket.send_json(data)
        pass

    def close(self):
        """Closes the ZMQ socket and the ZMQ context.
        """
        self.zmq_socket.close()
        self.zmq_context.term()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Enables use of JSONSender in with statement.
        """

        self.close()


class JSONHub():
    """Opens a zmq socket and receives data

    Opens a zmq (REP or SUB) socket on the hub computer, 
    that will be receiving data. Provides methods to receive data.

    Two kinds of ZMQ message patterns are possible:
    REQ/REP: data is sent and the sender waits for a reply ("blocking").
    PUB/SUB: data is sent and no reply is sent or expected ("non-blocking").

    There are advantabes and disadvantages for each message pattern.
    See the documentation for a full description of REQ/REP and PUB/SUB.
    The default is REQ/REP for the JSONSender class and the JSONHub class.

    Arguments:
      open_port: (optional) the socket to open for receiving REQ requests or
                 socket to connect to for SUB requests.
      REQ_REP: (optional) if True (the default), a REP socket will be created
                          if False, a SUB socket will be created
    """

    def __init__(self, open_port='tcp://*:5555', REQ_REP = True):
        """Initializes zmq socket to receive data.

        Expects an appropriate ZMQ socket at the senders tcp:port address:
        If REQ_REP is True (the default), then a REP socket is created. It
        must connect to a matching REQ socket on the JSONSender().

        If REQ_REP = False, then a SUB socket is created. It must connect to
        a matching PUB socket on the JSONSender().

        """
        self.REQ_REP = REQ_REP
        if REQ_REP ==True:
            #Init REP socket for blocking mode
            self.init_reqrep(open_port)
        else:
            #Connect to PUB socket for non-blocking mode
            self.init_pubsub(open_port)

    def init_reqrep(self, address):
        """ Initializes Hub in REQ/REP mode
        """
        socketType = zmq.REQ
        self.zmq_context = zmq.Context()
        self.zmq_socket = self.zmq_context.socket(socketType)
        self.zmq_socket.connect(address)

    def init_pubsub(self, address):
       """ Initialize Hub in PUB/SUB mode
       """
       socketType = zmq.SUB
       self.zmq_context = zmq.Context()
       self.zmq_socket = self.zmq_context.socket(socketType)
       self.zmq_socket.setsockopt(zmq.SUBSCRIBE, b'')
       self.zmq_socket.connect(address)

    def connect(self, open_port):
        """In PUB/SUB mode, the hub can connect to multiple senders at the same
        time.
        Use this method to connect (and subscribe) to additional senders.

        Arguments:
             open_port: the PUB socket to connect to.
        """

        if self.REQ_REP == False:
            #This makes sense only in PUB/SUB mode
            self.zmq_socket.setsockopt(zmq.SUBSCRIBE, b'')
            self.zmq_socket.connect(open_port)
            self.zmq_socket.subscribe(b'')
        return

    def recv_json(self):
        """Receives data.
        Returns:
          msg: text msg.
          data: json data
        """
        data = self.zmq_socket.recv_json()
        return data


    def send_reply(self, reply_message=b'OK'):
        """Sends the zmq REP reply message.

        Arguments:
          reply_message: reply message text, often just string 'OK'
        """
        self.zmq_socket.send(reply_message)

    def close(self):
        """Closes the ZMQ socket and the ZMQ context.
        """
        self.zmq_socket.close()
        self.zmq_context.term()

    def __enter__(self):
        """Enables use of JSONHub in with statement.

        Returns:
          self.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Enables use of JSONHub in with statement.
        """
        self.close()