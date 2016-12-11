import sys
from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators
from math import factorial

@Configuration(local=True)
class ErlangCommand(StreamingCommand):

    blocking_factor = Option(require=False, validate=validators.Float(), default=0.0001,doc='''
    **Syntax:** **blocking_factor=***<blocking_factor>*
        **Description:** define blocking factor to calculate number of lines needed''')
    field = Option(require=True, validate=validators.Fieldname(),doc='''
    **Syntax:** **field=***<field>*
        **Description:** define column which contain current usage''')
    result = Option(require=False, validate=validators.Fieldname(),default="trunks",doc='''
    **Syntax:** **result=***<result>*
        **Description:** define column name of result column''')
    method = Option(require=False, validate=validators.Fieldname(),default="erlangbextended",doc='''
    **Syntax:** **method=***<method>*
        **Description:** define erlangb math method''')

    def stream(self, events):
       trunks = 0
       res = None
       for event in events:
         if self.method == "erlangb":
            trunks = self.erlangb(float(event[self.field]), float(self.blocking_factor))
            event[self.result] = trunks
            yield event
         else:
            trunks = self.extended_b_lines(float(event[self.field]), float(self.blocking_factor))
            event[self.result] = trunks
            yield event

    # math function adapted from https://github.com/natemara/python-erlang
    def extended_b_lines(self, usage, blocking):
        line_count = 1
        while self.extended_b(usage, line_count) > blocking:
            line_count += 1
        return line_count

    def extended_b(self, usage, lines, recall=0.5):
        original_usage = usage
        while True:
            PB = self.b(usage, lines)
            magic_number_1 = (1 - PB) * usage + (1 - recall) * PB * usage
            magic_number_2 = 0.9999 * original_usage
            if magic_number_1 >= magic_number_2:
                return PB
            usage = original_usage + recall * PB * usage
        return -1

    def b(self, usage, lines):
        if usage > 0:
            PBR = (1 + usage) / usage
            for index in range(2, lines + 1):
                PBR = index / usage * PBR + 1
                if PBR > 10000:
                    return 0
            return 1 / PBR
        return 0

    # math function adapted from R app
    def elf(self, n, a):
        b = 1
        i = 0
        a = float(a)
        while i <= n:
            b = b*a/(i+b*a)
            i += 1
        return b

    def erlangb(self, usage, blocking):
        trunks = 0
        bounce_rate = 1
        while bounce_rate > blocking:
            trunks += 1
            bounce_rate = self.elf(trunks,usage)
        return trunks

dispatch(ErlangCommand, sys.argv, sys.stdin, sys.stdout, __name__)
