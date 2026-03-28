from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from typing import Literal
from pygridsynth.gridsynth import gridsynth_gates, gridsynth_circuit
from utils import QuantumGate
import mpmath
import trasyn

class circuitDecomposer:
    gateSet: list[QuantumGate]        #List of gates that we will decompose the arbitrary circuit into
    decompositionError: float         #tolerable error for each gate when decomposing a circuit
    originalCircuit: QuantumCircuit   #the original non-decomposed circuit comprised of arbitrary gates
    decomposedCircuit: QuantumCircuit #the decomposed circuit comprised of only gates in our gateSet
	
    def __init__(self, gateSet:list[QuantumGate], decompositionError:float, originalCircuit:QuantumCircuit):
        self.gateSet = gateSet
        self.decompositionError = decompositionError
        self.originalCircuit = originalCircuit
        self.decomposedCircuit = QuantumCircuit(self.originalCircuit.num_qubits, self.originalCircuit.num_clbits)
	
def decomposeToGateset(self):
    if 'T' in self.gateSet:
        return self.decomposeToCliffordPlusT()
    #TODO: take the original circuit from this object and decompose it into the gateSet of this object

    #TODO: set the decomposedCircuit to the one we just created and then return the decomposed circuit
    return "TODO: IMPLEMENT decomposeToGateset function"

def decomposeToCliffordPlusT(self):
    mpmath.mp.dps = 128
    epsilon = mpmath.mpf("1e-10")

    for inst in self.originalCircuit.data:
        if inst.name == 'rz':
            theta = float(inst.params[0])
            circuit = gridsynth_circuit(mpmath.mpf(theta), epsilon)
            #print(circuit)

            for gate in circuit:
                string = gate.to_simple_str()
                if string == 'S':
                    self.decomposedCircuit.s(gate.target_qubit)
                if string == 'H':
                    self.decomposedCircuit.h(gate.target_qubit)
                if string == 'T':
                    self.decomposedCircuit.t(gate.target_qubit)
                if string == 'X':
                    # Printing the circuit shows this as an SX gate, but its simple string is X.  Not sure which is correct.
                    self.decomposedCircuit.sx(gate.target_qubit)
                # if string == 'W':
                    # Qiskit does not appear to have W as an option.

                #print(self.decomposedCircuit.draw('text'))

            # Not Sure why this is causing an error.
            # print(trasyn.synthesize(target_unitary=theta, nonclifford_budget=100))
    return self.decomposedCircuit
