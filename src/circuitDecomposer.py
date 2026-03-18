from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from typing import Literal

Gates = Literal['X', 'Y', 'Z', 'CX', 'CZ', 'H', 'T', 'CCZ', 'sqrtT', 'R_z', 'T/2']
CliffordGates = Literal['X', 'Y', 'Z', 'CX', 'CZ', 'H']
NonCliffordGates = Literal['T', 'CCZ', 'sqrtT', 'R_z', 'T/2']

class circuitDecomposer:
    gateSet: list[Gates]              #List of gates that we will decompose the arbitrary circuit into
    decompositionError: float         #tolerable error for each gate when decomposing a circuit
    originalCircuit: QuantumCircuit   #the original non-decomposed circuit comprised of arbitrary gates
    decomposedCircuit: QuantumCircuit #the decomposed circuit comprised of only gates in our gateSet

    def __init__(self, gateSet, decompositionError, originalCircuit):
        self.gateSet = gateSet
        self.decompositionError = decompositionError
        self.originalCircuit = originalCircuit
    
    def decomposeToGateset(self):
        #TODO: take the original circuit from this object and decompose it into the gateSet of this object

        #TODO: set the decomposedCircuit to the one we just created and then return the decomposed circuit
        return "TODO: IMPLEMENT decomposeToGateset function"
