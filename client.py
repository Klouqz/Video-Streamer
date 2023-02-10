import socket
import cv2
import pickle
import struct
import sys
import win32com.shell.shell as shell

def is_admin():
    try:
        return shell.IsUserAnAdmin()
    except:
        return False

if is_admin():
    pass
else:
    shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=' '.join(sys.argv))


class VideoStreamClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = self.client_socket.connect((self.host, self.port))
        self.data = b""
        self.payload_size = struct.calcsize("Q")

    def receive(self):
        while True:
            while len(self.data) < self.payload_size:
                self.packet = self.client_socket.recv(4 * 1024)  # 4K
                if not self.packet: break
                self.data += self.packet
            self.packed_msg_size = self.data[:self.payload_size]
            self.data = self.data[self.payload_size:]
            self.msg_size = struct.unpack("Q", self.packed_msg_size)[0]

            while len(self.data) < self.msg_size:
                self.data += self.client_socket.recv(4 * 1024)
            self.frame_data = self.data[:self.msg_size]
            self.data = self.data[self.msg_size:]
            self.frame = pickle.loads(self.frame_data)
            cv2.imshow("Client", self.frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        self.client_socket.close()

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 9999
    c = VideoStreamClient(host, port)
    c.receive()
