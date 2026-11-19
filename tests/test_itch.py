import io
import struct

import itch_book as I


def hdr(t, loc, ts):
    return bytes([t]) + struct.pack(">HH", loc, 0) + ts.to_bytes(6, "big")


def msg(b):
    return struct.pack(">H", len(b)) + b


def test_book_rebuild_and_sampling_before_update():
    S = b"QQQ".ljust(8)
    R = msg(hdr(82, 1, 0) + S + b"Q N 100NC     N" + b"\x00" * 10)

    def A(ref, side, sh, price, ts):
        return msg(hdr(65, 1, ts) + struct.pack(">Q", ref) + side + struct.pack(">I", sh) + S + struct.pack(">I", price))
    sec = lambda s: s * 10 ** 9
    data = (R + A(1, b"B", 100, 2000000, sec(34201)) + A(2, b"S", 300, 2000100, sec(34201)) + A(3, b"B", 100, 1999900, sec(34201))
            + msg(hdr(69, 1, sec(34202)) + struct.pack(">QIQ", 2, 100, 5)) + msg(hdr(68, 1, sec(34203)) + struct.pack(">Q", 1)))
    rows = I.process(io.BytesIO(data), syms=[S], quiet=True)[S]
    assert [r[0] for r in rows] == [34201, 34202, 34203]
    assert rows[0][4] == 300 and rows[1][4] == 200        # the execution shows up only in the following second
    assert abs(rows[2][1] - 200.0) < 1e-9                 # best bid deleted, next level 199.99
