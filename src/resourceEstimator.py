from magicFactory import MagicFactory
from typing import List
from qiskit import QuantumCircuit
from circuitDecomposer import CircuitDecomposer
from utils import QuantumGate


class ResourceEstimator:
    magicFactories: List[MagicFactory]   #list of magic factories on the chip to run the algo
    quantumCircuit: QuantumCircuit       #The circuit to be run
    codeDistance: int                    #The code distance of error correction on the circuit
    p_phys: float

    def __init__(self, magicFactories: List[MagicFactory], quantumCircuit: QuantumCircuit, codeDistance:int, p_phys:float):
        self.magicFactories = magicFactories
        self.quantumCircuit = quantumCircuit
        self.codeDistance = codeDistance
        self.p_phys = p_phys

    #TODO: function to decompose circuit into clifford + whatever magic state is made by the factories
    def decomposeToCliffordPlusMagic(self, errorRate:float):
        # Raise an error if magicFactories or quantumCircuit is null.
        if self.magicFactories == None:
            raise ValueError("ResourceEstimator.magicFactories should not be null.")
        if self.quantumCircuit == None:
            raise ValueError("ResourceEstimator.quantumCircuit should not be null.")
        
        #TODO: Look at the list of magic factories and decompose the circuit into the available gates.
        gates = []
        for factory in self.magicFactories:
            gates.append(factory.gate)
        for gate in QuantumGate:
            if gate.isClifford():
                gates.append(gate)

        decomposer = CircuitDecomposer(gates, errorRate, self.quantumCircuit)
        decomposedCircuit = decomposer.decomposeToGateset()
        return decomposedCircuit
    
    """
        calculates the total number of physical qubits needed to run the algorithm (factories + algorithm)
    """
    def calcFootprint(self):
        #Calculate the total area of factories
        magicFactoryFootprint = 0 #initialize a counter for the qubits required for all factories
        for mFactory in self.magicFactories:
            magicFactoryFootprint += mFactory.qubitFootprint
        
        #Calculate the physical qubits required for the algorithm based on code distance
        logicalQubits = self.quantumCircuit.num_qubits()            #each qubit in the algorithm is a logical qubit
        physQubitsPerLogicalQubit = 2 * self.codeDistance**2 - 1    #surface codes are a [2d^2-1, 1, d] code so it takes 2d^2-1 physical qubits to implement 1 logical qubit
        circuitFootprint = logicalQubits * physQubitsPerLogicalQubit

        #TODO: account for routing / lattice surgery? or ignore routing

        return magicFactoryFootprint + circuitFootprint
    

    def calcRuntime(self):
        #TODO: need a way to calculate how long the circuit will take to run
        #This will have to do with how many magic factories are running and how many cycles we need to wait for enough states
        return

    def runCircuit(self):
        #TODO: since our circuit is a qiskit circuit, we just have to run it. main reason is to get fidelity
        # update gate fidelities based on logical error rate AND magic factory output rate (for non-clifford gates)
        return

    """
        Do a resource analysis of the given circuit using the magic factories provided
        Determine cycles to run (runtime), space on chip (magic factory + errorcorrection + algo), 
    """
    def analyzeCircuit(self):
        #Decompose circuit based on magic factories

        #Calculate footprint

        #run circuit and determine fidelity
        return
