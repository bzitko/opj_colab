# coding=utf-8
import itertools

HMM_TXT = """
S

S A 0.5
S B 0.5
A A 0.8
A B 0.2
B A 0.6
B B 0.4

A x 0.7
A y 0.2
A z 0.1
B x 0.3
B y 0.5
B z 0.2
"""

HMM_TXT2 = """
S

S N 0.4 
S V 0.2
S A 0.4
A A 0.4
A V 0.1
A N 0.5
N A 0.1
N V 0.6
N N 0.3
V A 0.4
V N 0.4
V V 0.2

N dobar 0.05
N dan 0.9
N je 0.05
A dobar 0.9
A dan 0.05
A je 0.05
V dobar 0.05
V dan 0.05
V je 0.9
"""

class Hmm(object):

    def parse(txt):
        start, transitions_txt, emissions_txt = txt.strip().split('\n\n')
        
        transitions = {}
        for line in transitions_txt.split('\n'):
            state, next_state, prob = line.strip().split()
            transitions[(state, next_state)] = float(prob)

        emissions = {}
        for line in emissions_txt.split('\n'):
            state, sym, prob = line.strip().split()
            emissions[(state, sym)] = float(prob)
        return Hmm(start, transitions, emissions)

    def __init__(self, start, transitions, emissions):
        self.start, self.transitions, self.emissions = start, transitions, emissions

    @property
    def states(self):
        return {state for state, _ in self.emissions}

    @property
    def symbols(self):
        return list(set(sym for _, sym in self.emissions))

    def transition(self, state, next_state):
        return self.transitions.get((state, next_state), 0)

    def emission(self, state, sym):
        return self.emissions.get((state, sym), 0)


    def calc_probability_of_seq(self, seq):
        sym_seq = seq.strip().split()
        n = len(sym_seq)
        
        prob_seq = 0
        probabilities = {}
        for state_seq in itertools.product(self.states, repeat = n):
            state = self.start
            prob_seq_state = 1
            for next_state, sym in zip(state_seq, sym_seq):
                prob_seq_state *= self.transitions.get((state, next_state), 0) * self.emissions.get((next_state, sym), 0)
                state = next_state
            probabilities[state_seq] = prob_seq_state
            prob_seq += prob_seq_state
                
        print(probabilities, prob_seq)


    def viterbi(self, seq):
        sym_seq = seq.strip().split()
        mx = [{}]
        path = {}

        t = 0
        for state in self.states:
            mx[0][state] = self.transition(self.start, state) * self.emission(state, sym_seq[0])
            path[state] = [state]


        for t, sym in enumerate(sym_seq[1:], 1):
            mx.append({})
            newpath = {}
            
            for next_state in self.states:
                mx[t][next_state], state = max((
                    mx[t-1][state] * 
                    self.transition(state, next_state) *
                    self.emission(next_state, sym) 
                    ,state) for state in self.states)
                newpath[next_state] = path[state] + [next_state]

            path = newpath
                
        n = len(sym_seq) - 1
        prob, state = max((mx[n][state], state) for state in self.states)
        print(prob, path[state])



hmm1 = Hmm.parse(HMM_TXT)
seq = 'y z'
print(seq)
hmm1.calc_probability_of_seq(seq)
hmm1.viterbi(seq)

print()
print()

hmm2 = Hmm.parse(HMM_TXT2)
seq ='dan je dobar'
print(seq)
hmm2.calc_probability_of_seq(seq)
hmm2.viterbi(seq)