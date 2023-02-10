import socket
import cv2
import pickle
import struct

class VideoStreamServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Listenin At:", (self.host, self.port))

    def start(self):
        self.client_socket, self.addr = self.server_socket.accept()
        print('Connection From:', self.addr)
        if self.client_socket:
            self.video = cv2.VideoCapture(0)
            while self.video.isOpened():
                self.ret, self.frame = self.video.read()
                self.a = pickle.dumps(self.frame)
                self.message = struct.pack("Q", len(self.a)) + self.a
                self.client_socket.sendall(self.message)
                cv2.imshow('Server', self.frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    self.client_socket.close()


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 9999
    s = VideoStreamServer(host, port)
    s.start()
