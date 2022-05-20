import scapy.all as scapy
import socket
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.Qt import *

HOME_IP = '10.0.0.100'
HOME_MAC = 'ac-7d-eb-a7-7d-3e'
HOME_HOST_NAME = socket.gethostbyaddr(HOME_IP)[0]
MASK = [255, 255, 255, 0]


def get_network_ip():
    client_ip = [int(octet) for octet in HOME_IP.split('.')]
    network_ip = ''
    for i in range(len(client_ip)):
        network_ip += str(client_ip[i] & MASK[i]) + '.'
    return network_ip[:-1]


class ScannerWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Local net scanner')
        self.setFixedSize(1000, 700)
        self.setObjectName('MainWindow')

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(170, 100, 700, 35)

        self.log = QtWidgets.QTextEdit(self)
        self.log.setGeometry(170, 180, 700, 290)
        self.log.setReadOnly(True)
        self.cursor = QTextCursor(self.log.document())
        self.log.setTextCursor(self.cursor)

        self.scan_button = QtWidgets.QPushButton(self)
        self.scan_button.setGeometry(190, 470, 660, 50)
        self.scan_button.setText('Start scanning')
        self.scan_button.clicked.connect(self.scan)

        self.network_ip = get_network_ip()

        self.clear_log()

    def scan(self):
        self.progress_bar.setValue(0)
        self.show_log("IP Address" + "\t" * 2 + "MAC Address" + "\t" * 3 + "Host name\n")
        self.show_log('Home:\n')
        self.show_log(HOME_IP + "\t" * 2 + HOME_MAC + "\t" * 2 + HOME_HOST_NAME + "\n\n")

        arp_request = scapy.ARP(pdst=self.network_ip + '/24')
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answer_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False, retry=1)[0]
        total_hosts = len(answer_list)
        self.show_log("Local network:\n")
        for i, host in enumerate(answer_list):
            self.progress_bar.setValue(round((i + 1) / total_hosts * 100))
            ip = host[1].psrc
            if ip == HOME_IP:
                continue
            mac_address = host[1].hwsrc
            try:
                host_name = socket.gethostbyaddr(ip)[0]
            except Exception:
                host_name = '-'
            self.show_log(ip + "\t" * 2 + mac_address + "\t" * 2 + host_name)
        self.log.moveCursor(QtGui.QTextCursor.End)  # делаем автоматическую прокрутку для просмотра последних логов

    def clear_log(self):
        with open('scanner_log.txt', 'w') as f:
            f.write('')
            f.close()

    def show_log(self, msg):
        with open('scanner_log.txt', 'a') as f:
            f.write(msg)
            f.close()
        with open('scanner_log.txt', 'r') as f:
            data = f.read()
            self.log.setText(data)
            f.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    scanner_window = ScannerWindow()
    scanner_window.show()
    sys.exit(app.exec_())
