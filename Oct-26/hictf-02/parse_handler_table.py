import idautils
import idc
path = r"D:\CTF\practical\Oct-26\hictf-02\output\handler_table"

START = 0x404588
END   = 0x404690   # địa chỉ retn
base = 0x40A240
table = {}
for ea in idautils.Heads(START, END):
    if idc.print_insn_mnem(ea) != "mov":
        continue
    if idc.get_operand_type(ea, 0) != idc.o_mem:
        continue
    addr    = idc.get_operand_value(ea, 0)
    handler = idc.get_name(idc.get_operand_value(ea, 1))
    table[addr] = handler
print("{")
for addr, name in table.items():
    print(f'{hex(addr)}: "{name}",')
print("}")

