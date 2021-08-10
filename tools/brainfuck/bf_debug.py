#!/usr/bin/env python
import sys

if len(sys.argv) < 2:
    print("Give me filename...")
    exit()

# Parameters
TAPE_LEN = 264 # from original interpreter
TAPE_CONTEXT = 14
CODE_CONTEXT = 72

process_input = (sys.argv[2].encode() if len(sys.argv) > 2 else b"")
process_output = b""

# Colors
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

code = open(sys.argv[1]).read().replace("\n", "").replace(" ", "")

stack = []              # track loop execution
tape = [0]*TAPE_LEN     # process memory
ptr = 0                 # current tape position

rip = 0                 # next instruction to execute
lip = 0                 # previous instruction (illustrate jumps)

breakpoints = []        # stop exec at these rips
breakops = []           # stop exec at these codes
watchpoints = []        # stop exce on these ptrs


def display_status():
    global code
    global stack
    global tape
    global ptr
    global rip
    global lip
    print("")
    print("")
    print("Tape ptr: %i"%(ptr))
    print("Prog rip: %i"%(rip))
    print("Prog lip: %i"%(lip))
    print("")

    # stack
    if len(stack) == 0:
        print(f"{FAIL}No loops{ENDC}")
    else:
        for l in stack:
            print("0x%05x"%(l), end="  ")
        print("")
    print("")

    # tape
    addr = ""
    hexa = ""
    deci = ""
    asci = ""
    for i in range(ptr - TAPE_CONTEXT, ptr + TAPE_CONTEXT + 1):
        oob = i < 0 or i >= TAPE_LEN
        color = (OKGREEN if i == ptr else WARNING if i in watchpoints else OKCYAN if tape[i] != 0 else FAIL if oob else '')
        value = (0 if oob else tape[i])
        char = (chr(value) if value >= 0x20 and value < 0x7f else "U")

        addr += f" {color}{UNDERLINE}0x%02x{ENDC}"%(i)
        hexa += f" {color}0x%02x{ENDC}"%(value)
        deci += f" {color}%4i{ENDC}"%(value)
        asci += f" {color}%4s{ENDC}"%(char)

    print(addr)
    print(hexa)
    print(deci)
    print(asci)
    print("")

    # code
    breaks = ""
    ops = ""
    for i in range(rip - CODE_CONTEXT, rip + CODE_CONTEXT + 1):
        oob = i < 0 or i >= len(code)
        color = (OKGREEN+BOLD+UNDERLINE if i == rip
                else OKBLUE+BOLD if i == lip
                else FAIL+BOLD if oob else '')
        oper = (" " if oob else code[i])
        brek = (" " if oob else "P" if i in breakpoints else "O" if code[i] in breakops else " ")

        breaks += f"{FAIL}{brek}{ENDC}"
        ops += f"{color}{oper}{ENDC}"

    print(breaks)
    print(ops)

def display_tape():
    global code
    global stack
    global tape
    global ptr
    global rip
    global lip
    print("")
    print("")
    for i, x in enumerate(tape):
        color = (OKGREEN if i == ptr else WARNING if i in watchpoints else OKCYAN if x != 0 else '')
        print(f"{color}0x%02x{ENDC}  "%(x), end="")
        if (i+1) % 16 == 0:
            print("")
        elif (i+1) % 8 == 0:
            print("  ", end="")
    print("")

def display_tape_ascii():
    global code
    global stack
    global tape
    global ptr
    global rip
    global lip
    print("")
    print("")
    for i, x in enumerate(tape):
        color = (OKGREEN if i == ptr else '')
        char = (chr(x) if x >= 0x20 and x < 0x7f else '.')
        print(f"{color}{char}{ENDC}", end="")
    print("")

def display_code():
    global code
    global stack
    global tape
    global ptr
    global rip
    global lip
    print("")
    print("")
    for i, x in enumerate(code):
        color = (OKGREEN+BOLD+UNDERLINE if i == rip
                else OKBLUE+BOLD if i == lip
                else FAIL+BOLD if i in breakpoints
                else FAIL+BOLD if code[i] in breakops else '')
        print(f"{color}{x}{ENDC}", end="")
    print("")

def display_input():
    global code
    global stack
    global tape
    global ptr
    global rip
    global lip
    global process_input
    print("")
    print("")
    print(f"Input (to-be-read): {process_input}")

def display_output():
    global code
    global stack
    global tape
    global ptr
    global rip
    global lip
    global process_output
    print("")
    print("")
    print(f"Output (cumulative): {process_output}")

def jump_past_loop():
    global code
    global stack
    global tape
    global ptr
    global rip
    global lip
    i = 1
    for pos in range(rip, len(code)):
        if code[pos] == '[':
            i += 1
        elif code[pos] == ']':
            i -= 1
        if i == 0:
            rip = pos + 1
            break
    if i != 0:
        raise Exception("'[' has no paring ']'")

def run_code():
    global code
    global stack
    global tape
    global ptr
    global rip
    global lip
    global process_input
    global process_output
    while True:
        if step_forward() == True:
            break
        if rip in breakpoints:
            break
        if rip < len(code) and (code[rip] in breakops):
            break
        if ptr in watchpoints:
            break

def step_forward():
    global code
    global stack
    global tape
    global ptr
    global rip
    global lip
    global process_input
    global process_output
    if rip >= len(code):
        print("Execution finished.")
        return True

    op = code[rip]
    lip = rip
    rip += 1

    if op == '<':
        if ptr == 0:
            raise Exception("Tape ptr out of bounds! (underflow)")
        ptr -= 1
    elif op == '>':
        if ptr == TAPE_LEN-1:
            raise Exception("Tap ptr out of bounds! (overflow)")
        ptr += 1
    elif op == '+':
        if tape[ptr] == 255:
            tape[ptr] = 0
        else:
            tape[ptr] += 1
    elif op == '-':
        if tape[ptr] == 0:
            tape[ptr] = 255
        else:
            tape[ptr] -= 1
    elif op == '.':
        process_output += tape[ptr].to_bytes(1, 'big')
        display_output()
    elif op == ',':
        if len(process_input) == 0:
            raise Exception("Out of input!")
        display_input()
        tape[ptr] = process_input[0]
        process_input = process_input[1:]
    elif op == '[':
        if tape[ptr] == 0:
            jump_past_loop()
        else:
            stack.append(rip) # rip currently on first op after [
    elif op == ']':
        if tape[ptr] == 0:
            stack.pop()
        else:
            rip = stack[-1]
    else:
        raise Exception("Illegal instruction!")

def manage_breakpoints():
    global breakpoints
    while True:
        print("Current breakpoints:")
        for i, x in enumerate(breakpoints):
            print(f"    {i}: {x}")
        print("")

        ip = input("[a]dd/[d]el/[f]inish <arg>: ")
        cmd = ip.split()[0]

        if cmd == 'f':
            break
        if cmd == 'a':
            breakpoints.append(int(ip.split()[1]))
        elif cmd == 'd':
            del breakpoints[int(ip.split()[1])]

def manage_breakops():
    global breakops
    while True:
        print("Current breakops:")
        for i, x in enumerate(breakops):
            print(f"    {i}: {x}")
        print("")

        ip = input("[a]dd/[d]el/[f]inish <arg>: ")
        cmd = ip.split()[0]

        if cmd == 'f':
            break
        if cmd == 'a':
            breakops.append(ip.split()[1])
        elif cmd == 'd':
            del breakops[int(ip.split()[1])]

def manage_watchpoints():
    global watchpoints
    while True:
        print("Current watchpoints:")
        for i, x in enumerate(watchpoints):
            print(f"    {i}: {x}")
        print("")

        ip = input("[a]dd/[d]el/[f]inish <arg>: ")
        cmd = ip.split()[0]

        if cmd == 'f':
            break
        if cmd == 'a':
            watchpoints.append(int(ip.split()[1]))
        elif cmd == 'd':
            del watchpoints[int(ip.split()[1])]

def write_tape():
    global tape
    addr = int(input("Address: "))
    val = int(input("Value: "))
    tape[addr] = val


enter_is_step = False
print("Hints:  j: step forward   t: show tape   a: show tape (ascii)   c: show code   i: show input   o: show output")
print("        r: run   p: manage breakpoints   l: manage breakops   w: manage watchpoints   q: quit   s: show status")
print("        m: edit tape memory")
display_status()
while True:
    c = input("> ")

    if c == 'j' or (c == '' and enter_is_step):
        enter_is_step = True
        step_forward()
        display_status()
    else:
        enter_is_step = False
        if c == 's':
            display_status()
        elif c == 't':
            display_tape()
        elif c == 'a':
            display_tape_ascii()
        elif c == 'c':
            display_code()
        elif c == 'i':
            display_input()
        elif c == 'o':
            display_output()
        elif c == 'q':
            break
        elif c == 'r':
            run_code()
            display_status()
        elif c == 'p':
            manage_breakpoints()
            display_status()
        elif c == 'l':
            manage_breakops()
            display_status()
        elif c == 'w':
            manage_watchpoints()
            display_status()
        elif c == 'm':
            write_tape()
