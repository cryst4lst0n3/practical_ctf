BASE = 0x400000
import struct 

def target_of_call(buf, off):
    rel = struct.unpack_from("<i", buf, off + 1)[0]
    return BASE + off + 5 + rel


buf = bytearray(open('crackme', "rb").read())

for off in range(len(buf) - 5):
	if buf[off] != 0xE8:
		continue

	target = target_of_call(buf, off)
	target_off = target - BASE

	if 0 <= target_off < len(buf) - 1 and buf[target_off : target_off + 2] == b"\x41\x58":
		buf[off] = 0xE9
		buf[target_off : target_off + 2] = b"\x90\x90"

open('patched_crackme', "wb").write(buf)
print("done")