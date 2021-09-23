import re
from functools import reduce
from collections import defaultdict

FSM_RAW = """
    CLOSED: APP_PASSIVE_OPEN -> LISTEN
    CLOSED: APP_ACTIVE_OPEN  -> SYN_SENT
    LISTEN: RCV_SYN          -> SYN_RCVD
    LISTEN: APP_SEND         -> SYN_SENT
    LISTEN: APP_CLOSE        -> CLOSED
    SYN_RCVD: APP_CLOSE      -> FIN_WAIT_1
    SYN_RCVD: RCV_ACK        -> ESTABLISHED
    SYN_SENT: RCV_SYN        -> SYN_RCVD
    SYN_SENT: RCV_SYN_ACK    -> ESTABLISHED
    SYN_SENT: APP_CLOSE      -> CLOSED
    ESTABLISHED: APP_CLOSE   -> FIN_WAIT_1
    ESTABLISHED: RCV_FIN     -> CLOSE_WAIT
    FIN_WAIT_1: RCV_FIN      -> CLOSING
    FIN_WAIT_1: RCV_FIN_ACK  -> TIME_WAIT
    FIN_WAIT_1: RCV_ACK      -> FIN_WAIT_2
    CLOSING: RCV_ACK         -> TIME_WAIT
    FIN_WAIT_2: RCV_FIN      -> TIME_WAIT
    TIME_WAIT: APP_TIMEOUT   -> CLOSED
    CLOSE_WAIT: APP_CLOSE    -> LAST_ACK
    LAST_ACK: RCV_ACK        -> CLOSED
"""

def get_fsm():
    regex = re.compile(r'(?P<initial_state>\w+): (?P<event>\w+)\s*->\s(?P<new_state>\w+)')
    result = defaultdict(defaultdict)
    for initial_state, event, new_state in regex.findall(FSM_RAW):
        result[initial_state][event] = new_state
    return result

def traverse_TCP_states(events):
    fsm = get_fsm()
    return reduce(lambda state, event: fsm[state][event] if event in fsm[state] else "ERROR", events, "CLOSED")
  
