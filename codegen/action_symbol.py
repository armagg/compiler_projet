from codegen import syntax


class ActionSymbol:
    def __init__(self, name):
        self.name = name[1:]

    def match(self, *args):
        # print("Acting on", self.name)
        return getattr(self, f'gen_{self.name}')(*args)

    def gen_declvar(self, tokens, errors, ss, pb, symbol_table):
        ss.push(tokens.lookahead)

    def gen_skipvar(self, tokens, errors, ss, pb, symbol_table):
        ss.pop(1)

    def gen_savevar(self, tokens, errors, ss, pb, symbol_table):
        symbol_table.insert_var(ss[0][1])
        ss.pop(1)

    def gen_savearr(self, tokens, errors, ss, pb, symbol_table):
        symbol_table.insert_arr(ss[0][1], int(tokens.lookahead[1]))
        ss.pop(1)

    def gen_popexp(self, tokens, errors, ss, pb, symbol_table):
        ss.pop(1)

    def gen_startif(self, tokens, errors, ss, pb, symbol_table):
        ss.push(pb.advance())

    def gen_startelse(self, tokens, errors, ss, pb, symbol_table):
        jump_pos = pb.advance()
        pb[ss[0]] = syntax.jpf(ss[1], pb.next_line)
        ss.pop(2)
        ss.push(jump_pos)

    def gen_endelse(self, tokens, errors, ss, pb, symbol_table):
        pb[ss[0]] = syntax.jp(pb.next_line)
        ss.pop(1)

    def gen_startwhile(self, tokens, errors, ss, pb, symbol_table):
        ss.push(pb.next_line)

    def gen_midwhile(self, tokens, errors, ss, pb, symbol_table):
        ss.push(pb.advance())

    def gen_endwhile(self, tokens, errors, ss, pb, symbol_table):
        pb.append(syntax.jp(ss[2]))
        pb[ss[0]] = syntax.jpf(ss[1], pb.next_line)
        ss.pop(3)

    def gen_assignvar(self, tokens, errors, ss, pb, symbol_table):
        pb.append(syntax.assign(ss[0], ss[1]))
        ss.pop(1)

    def gen_arrindex(self, tokens, errors, ss, pb, symbol_table):
        var = symbol_table.get_temp()
        pb.append(syntax.multiply('#4', ss[0], var))
        pb.append(syntax.add(f'#{ss[1]}', var, var))
        ss.pop(2)
        ss.push(f'@{var}')

    def gen_applyrelop(self, tokens, errors, ss, pb, symbol_table):
        var = symbol_table.get_temp()
        op1, op2 = ss[2], ss[0]
        assert ss[1] in range(2)
        if ss[1] == 0:
            pb.append(syntax.equal(op1, op2, var))
        else:
            pb.append(syntax.lessthan(op1, op2, var))
        ss.pop(3)
        ss.push(var)

    def gen_pushrelop(self, tokens, errors, ss, pb, symbol_table):
        if tokens.lookahead[1] == '==':
            ss.push(0)
        elif tokens.lookahead[1] == '<':
            ss.push(1)
        else:
            print('Relop detection error')

    def gen_applyaddop(self, tokens, errors, ss, pb, symbol_table):
        var = symbol_table.get_temp()
        op1, op2 = ss[2], ss[0]
        assert ss[1] in range(2)
        if ss[1] == 0:
            pb.append(syntax.add(op1, op2, var))
        else:
            pb.append(syntax.subtract(op1, op2, var))
        ss.pop(3)
        ss.push(var)

    def gen_pushaddop(self, tokens, errors, ss, pb, symbol_table):
        if tokens.lookahead[1] == '+':
            ss.push(0)
        elif tokens.lookahead[1] == '-':
            ss.push(1)
        else:
            print('Addop detection error')

    def gen_multiply(self, tokens, errors, ss, pb, symbol_table):
        var = symbol_table.get_temp()
        op1, op2 = ss[1], ss[0]
        pb.append(syntax.multiply(op1, op2, var))
        ss.pop(2)
        ss.push(var)

    def gen_signpos(self, tokens, errors, ss, pb, symbol_table):
        pass

    def gen_signneg(self, tokens, errors, ss, pb, symbol_table):
        var = symbol_table.get_temp()
        pb.append(syntax.subtract('#0', ss[0], var))
        ss.pop(1)
        ss.push(var)

    def gen_pushid(self, tokens, errors, ss, pb, symbol_table):
        var = symbol_table.get_address(tokens.lookahead[1])
        ss.push(var)

    def gen_pushnum(self, tokens, errors, ss, pb, symbol_table):
        var = symbol_table.get_temp()
        num = int(tokens.lookahead[1])
        pb.append(syntax.assign(f'#{num}', var))
        ss.push(var)

    def gen_print(self, tokens, errors, ss, pb, symbol_table):
        pb.append(syntax.output(ss[0]))
        ss.pop(1)
