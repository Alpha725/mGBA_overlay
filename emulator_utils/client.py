import struct
import socket

class mGBAclient:
    def __init__(self, host='127.0.0.1', port=8888):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def read_memory(self, address, length=1):
        header = struct.pack('>B H B', 1, address, length)
        self.sock.sendall(header)
        return self.sock.recv(length)

    def write_memory(self, address, value):
        header = struct.pack('>B H B', 2, address, value)
        self.sock.sendall(header)
        return self.sock.recv(1)

    def read_rom(self, bank, address, length=1):
        header = struct.pack('>B B H H', 4, bank, address, length)
        self.sock.sendall(header)
        return self.sock.recv(length)

    def close(self):
        if self.sock:
            try:
                self.sock.sendall(b'\x03')
                self.sock.recv(1)
            except:
                pass
            finally:
                self.sock.close()
                print("Server state reset and socket closed.")
