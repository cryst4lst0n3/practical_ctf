import ida_bytes
path = r"D:\CTF\practical\Oct-26\hictf-02\output\dump.hex"
def dump_bytes(base,size) :
    bytecode = [0] * size
    for i in range(size):
        offset = base + i
        bytecode[i] = ida_bytes.get_byte(offset)
    return bytecode
start = 0x405e00
byte_code = dump_bytes(start,0x497)
with open(path,"w") as f:
    f.write("bytecode=[\n")
    for i in range(0,len(byte_code),16):
        chunk = byte_code[i:i+16]
        f.write("    " + ", ".join("0x{:02x}".format(b) for b in chunk) + ",\n")
    f.write("]\n")

