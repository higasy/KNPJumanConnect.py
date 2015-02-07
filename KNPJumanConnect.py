#!/usr/bin/python3

import socket
import sys


def _encode(data: str, encoding='utf-8'):
    return data.encode(encoding)


def _decode(data: bytes, encoding='utf-8'):
    return data.decode(encoding)


class KNPJumanConnect():

    def __init__(self):
        self.juman_s = None
        self.knp_s = None

    def juman_socket(self, name, port, option=""):
        while(not self.juman_s):
            try:
                self.juman_s = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                self.juman_s.connect((name, port))
            except:
                sys.stderr.write("Jumanとの接続に失敗しました\n")
                return False

        sys.stderr.write("Jumanと接続しました\n")
        input_a = ["RUN ", option, "\n"]
        input_mode = _encode("".join(input_a))
        self.juman_s.sendall(input_mode)
        sys.stderr.write(_decode(self.juman_s.recv(1024)))
        if option == "":
            sys.stderr.write("JUMAN running on BASIC MODE.....\n")
        else:
            sys.stderr.write("JUMAN running on " + option + " MODE.....\n")
        return True

    def post_juman(self, context):
        juman_result = ""
        self.juman_s.sendall(_encode(context + "\n"))
        juman_result = _decode(self.juman_s.recv(4096))
        return juman_result

    def juman_close(self):
        self.juman_s.close()

    def knp_socket(self, name, port, option=""):
        while(not self.knp_s):
            try:
                self.knp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.knp_s.connect((name, port))
            except:
                sys.stderr.write("KNPとの接続に失敗しました\n")
                return False
        sys.stderr.write("KNPと接続しました\n")
        input_a = ["RUN ", option, "\n"]
        input_mode = _encode("".join(input_a))
        self.knp_s.sendall(input_mode)
        sys.stderr.write(_decode(self.knp_s.recv(1024)))
        sys.stderr.write(_decode(self.knp_s.recv(1024)))
        if option == "":
            sys.stderr.write("KNP running on BASIC MODE.....\n")
        else:
            sys.stderr.write("KNP running on " + option + " MODE.....\n")
        return True

    def post_knp(self, context):
        knp_result = ""
        knp_result_list = []
        self.knp_s.sendall(_encode(self.post_juman(context)))
        while 1:
            f = self.knp_s.recv(1024)
            knp_result_list.append(f)
            if f.find(_encode("EOS\n")) != -1:
                break
        knp_result = _decode(b"".join(knp_result_list))
        return knp_result

    def knp_close(self):
        self.knp_s.close()
