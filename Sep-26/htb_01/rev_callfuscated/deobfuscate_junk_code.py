# -*- coding: utf-8 -*-
"""
Deobfuscate call->jmp obfuscation.
Pattern:  ... ; call sub_X        ->  ... ; jmp sub_X
          sub_X: pop r8 ; ...     ->  sub_X: nop ; nop ; ...
"""
import ida_bytes, ida_funcs, ida_auto, ida_ua, ida_segment, ida_kernwin
import idautils, idc

DRY_RUN = False         # True = chi in bao cao, khong patch gi
SEG_NAME = ".text"

# Cac bien the "pop reg" hay gap o dau block. Them neu binary dung reg khac.
POP_STUBS = {
    b"\x41\x58": "pop r8",
    b"\x41\x59": "pop r9",
    b"\x41\x5A": "pop r10",
    b"\x41\x5B": "pop r11",
    b"\x58":     "pop rax",
    b"\x59":     "pop rcx",
    b"\x5A":     "pop rdx",
}

def seg_range(name):
    s = ida_segment.get_segm_by_name(name)
    if not s:
        raise RuntimeError("Khong tim thay segment %s" % name)
    return s.start_ea, s.end_ea

def match_pop(ea):
    """Tra ve (do_dai, ten) neu ea bat dau bang mot pop stub, else None."""
    for pat, name in POP_STUBS.items():
        if ida_bytes.get_bytes(ea, len(pat)) == pat:
            return len(pat), name
    return None

def is_call_rel32(ea):
    """True neu ea la lenh call rel32 (E8, dai dung 5 byte)."""
    if ida_bytes.get_byte(ea) != 0xE8:
        return False
    tmp = ida_ua.insn_t()
    return ida_ua.decode_insn(tmp, ea) == 5

# ---------- PASS 1: thu thap ----------
start, end = seg_range(SEG_NAME)
calls = []          # (call_ea, target_ea)
target_refs = {}    # target_ea -> [call_ea, ...]

ea = start
while ea < end:
    insn = ida_ua.insn_t()
    length = ida_ua.decode_insn(insn, ea)
    if length == 0:
        ea += 1
        continue

    if is_call_rel32(ea) and insn.Op1.type == ida_ua.o_near:
        tgt = insn.Op1.addr
        if start <= tgt < end and match_pop(tgt):
            calls.append((ea, tgt))
            target_refs.setdefault(tgt, []).append(ea)

    ea += length

# ---------- PASS 2: kiem chung ----------
# Chi patch target ma MOI xref den no deu la call rel32 trong danh sach tren.
# Loai bo canh flow-ref "gia" ma IDA tu tao cho moi call (gia dinh se return
# roi roi xuong lenh ke) - vi obfuscation nay call khong bao gio return.
obf_call_eas = set(ea for ea, _ in calls)

safe_targets = set()
unsafe = []

for tgt, refs in target_refs.items():
    real_xrefs = set()
    for src in idautils.CodeRefsTo(tgt, 1):   # 1 = ke ca fallthrough
        if src in obf_call_eas and src + 5 == tgt:
            continue    # canh fallthrough gia tu chinh call obfuscated nay
        real_xrefs.add(src)

    if real_xrefs == set(refs):
        safe_targets.add(tgt)
    else:
        unsafe.append((tgt, real_xrefs - set(refs)))

print("[*] call rel32 -> pop-stub tim thay : %d" % len(calls))
print("[*] target an toan                  : %d" % len(safe_targets))
print("[*] target BO QUA (xref la)         : %d" % len(unsafe))
for tgt, extra in unsafe[:20]:
    print("    - %X  bi tham chieu tu %s" % (tgt, ", ".join("%X" % x for x in extra)))

if DRY_RUN:
    print("[!] DRY_RUN = True, chua ghi gi ca. Doi thanh False de patch.")
    raise SystemExit

# ---------- PASS 3: patch ----------
patched_calls = 0
for call_ea, tgt in calls:
    if tgt in safe_targets:
        ida_bytes.patch_byte(call_ea, 0xE9)      # E8 -> E9
        patched_calls += 1

patched_pops = 0
for tgt in safe_targets:
    n, _ = match_pop(tgt)
    ida_bytes.patch_bytes(tgt, b"\x90" * n)      # nop don, giu nguyen do dai
    patched_pops += 1

print("[+] Da patch %d call, %d pop stub." % (patched_calls, patched_pops))

# ---------- PASS 4: bat IDA phan tich lai ----------
ida_bytes.del_items(start, ida_bytes.DELIT_EXPAND, end - start)
ida_auto.plan_and_wait(start, end)
ida_auto.auto_wait()
print("[+] Reanalyze xong.")