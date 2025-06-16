import sys
import time
import re

class Ev:
    def ev(self, s):
        self.vars = {}
        self.funcs = {}
        lines = [x for x in s.split("\n") if x.strip() != ""]
        pc = 0
        while pc < len(lines):
            line = lines[pc].strip()

            

            # Function definition
            if line.startswith("FUNC"):
                name = line.split()[1]
                pc += 1
                func_body = []
                while not lines[pc].strip().startswith("/"):
                    func_body.append(lines[pc])
                    pc += 1
                self.funcs[name] = func_body
                pc += 1
                continue

            # Function call
            elif line.startswith("call"):
                fname = line.split()[1]
                if fname in self.funcs:
                    for fline in self.funcs[fname]:
                        fline = fline.strip()
                        if not fline or fline in ['\\', '/']:
                            continue
                        if '=' in fline:
                            name, _, expr = fline.split(maxsplit=2)
                            self.vars[name] = self.ev_expr(expr)
                        else:
                            self.ev_expr(fline)
                else:
                    print(f"[FunctionError] '{fname}' not found")
                pc += 1
                continue

            # COMP conditional block
            elif line.startswith("COMP"):
                parts = line.split()
                if len(parts) < 4:
                    print(f"[SyntaxError] Invalid COMP format")
                    pc += 1
                    continue
                _, lhs, rhs, op = parts[:4]
                condition = f"{lhs} {rhs} {op}"
                block = []
                pc += 1
                while pc < len(lines) and not lines[pc].strip().startswith("/"):
                    block.append(lines[pc])
                    pc += 1
                if self.ev_expr(condition) == 1:
                    for bline in block:
                        bline = bline.strip()
                        if not bline or bline in ['\\', '/']:
                            continue
                        if '=' in bline:
                            name, _, expr = bline.split(maxsplit=2)
                            self.vars[name] = self.ev_expr(expr)
                        else:
                            self.ev_expr(bline)
                pc += 1
                continue

            # While loop start
            if line.startswith("while"):
                condition = line.split(maxsplit=1)[1]
                loop_start = pc + 1
                loop_body = []
                depth = 1
                pc += 1
                while pc < len(lines) and depth > 0:
                    loop_line = lines[pc].strip()
                    if loop_line.startswith("while"):
                        depth += 1
                    elif loop_line == "end":
                        depth -= 1
                        if depth == 0:
                            break
                    loop_body.append(loop_line)
                    pc += 1
                while self.ev_expr(condition) == 1:
                    for loop_line in loop_body:
                        if '=' in loop_line:
                            name, _, expr = loop_line.split(maxsplit=2)
                            self.vars[name] = self.ev_expr(expr)
                        else:
                            self.ev_expr(loop_line)
                pc += 1
                continue

            elif line == "end":
                pc += 1
                continue

            elif line.startswith("INP"):
                varname = line.split()[1]
                self.vars[varname] = input(f"{varname}: ")
                pc += 1
                continue

            elif '=' in line:
                name, _, expr = line.split(maxsplit=2)
                self.vars[name] = self.ev_expr(expr)
            else:
                self.ev_expr(line)

            pc += 1

    def ev_expr(self, s):
        string_literals = re.findall(r'".*?"', s)
        for i, literal in enumerate(string_literals):
            s = s.replace(literal, f'__str{i}__')

        toks = s.split()
        for i, tok in enumerate(toks):
            if tok.startswith('__str') and tok.endswith('__'):
                index = int(re.findall(r'\d+', tok)[0])
                toks[i] = string_literals[index]

        stack = []
        for i, tok in enumerate(toks):
            #DON'T REACTIVATE THESE LINES
            #if tok in ['?']:
            #continue
            if tok.startswith('"') and tok.endswith('"'):
                stack.append(tok[1:-1])
            elif tok.isdigit():
                stack.append(int(tok))
            elif tok in self.vars:
                stack.append(self.vars[tok])
            elif tok in ['+', '-', '*', '/', '^', '%', '==', '!=', '>=', '<=']:
                if len(stack) < 2:
                    print(f"[RuntimeError] Not enough values on stack for '{tok}'")
                    return 0
                rhs = stack.pop()
                lhs = stack.pop()
                try:
                    lhs = int(lhs) if isinstance(lhs, str) and lhs.isdigit() else lhs
                    rhs = int(rhs) if isinstance(rhs, str) and rhs.isdigit() else rhs
                    if tok == '+': stack.append(lhs + rhs)
                    elif tok == '-': stack.append(lhs - rhs)
                    elif tok == '*': stack.append(lhs * rhs)
                    elif tok == '^': stack.append(lhs ** rhs)
                    elif tok == '/':
                        if rhs == 0:
                            print("[MathError] Division by zero")
                            stack.append(0)
                        else:
                            stack.append(lhs // rhs)
                    elif tok == '%': stack.append(lhs % rhs)
                    elif tok == '==': stack.append(1 if lhs == rhs else 0)
                    elif tok == '!=': stack.append(1 if lhs != rhs else 0)
                    elif tok == '>=': stack.append(1 if lhs >= rhs else 0)
                    elif tok == '<=': stack.append(1 if lhs <= rhs else 0)
                except Exception as e:
                    print(f"[TypeError] Operation '{tok}' failed: {e}")
                    return 0

            elif tok == 'TONUM':
                if i + 1 < len(toks):
                    varname = toks[i + 1]
                    if varname in self.vars:
                        try:
                            self.vars[varname] = int(self.vars[varname])
                        except:
                            self.vars[varname] = 0
            elif tok == 'TOSTR':
                if i + 1 < len(toks):
                    varname = toks[i + 1]
                    if varname in self.vars:
                        self.vars[varname] = str(self.vars[varname])
            elif tok == 'TOUTP':
                if stack:
                    val = stack.pop()
                    print(val)
                else:
                    idx = toks.index('TOUTP')
                    if idx + 1 < len(toks):
                        varname = toks[idx + 1]
                        if varname in self.vars:
                            print(str(self.vars[varname]))
                        else:
                            print(f"[undefined variable: {varname}]")
                    else:
                        print("[TOUTP missing value]")

            elif tok == 'SLEEP':
                if stack:
                    val = stack.pop()
                    time.sleep(val / 1000)
                else:
                    sys.exit("No value selected for the Yell SLEEP")
                
            
            elif tok == 'EXEND':
                if stack:
                    val = stack.pop()
                    sys.exit(str(val))
                else:
                    sys.exit(" ")
                
        return stack[0] if stack else 0

Ev().ev(open(sys.argv[1]).read())