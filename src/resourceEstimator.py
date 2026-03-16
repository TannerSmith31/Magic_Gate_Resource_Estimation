from magicFactory import MagicFactory
from typing import List
from qiskit import QuantumCircuit


class ResourceEstimator:
    magicFactories: List[MagicFactory]   #list of magic factories on the chip to run the algo
    quantumCircuit: QuantumCircuit       #The circuit to be run

    def __init__(self, magicFactories: List[MagicFactory], quantumCircuit: QuantumCircuit):
        self.magicFactories = magicFactories
        self.quantumCircuit = quantumCircuit

    #TODO: function to decompose circuit into clifford + whatever magic state is made by the factories

    #TODO: function to go through and analyze the total resource cost of running the circuit with the given factories (may be multiple functions)
