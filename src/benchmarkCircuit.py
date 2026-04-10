from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
import numpy as np

class BenchmarkCircuit:
    circuit:QuantumCircuit      #The benchmark circuit
    idealCounts:dict[str,int]   #The ideal counts for this benchmark circuit when run with no noise for 'shots' shots
    shots:int                   #The number of shots to run this benchmark

    def __init__(self, circuit:QuantumCircuit, idealCounts:dict[str,int], shots:int):
        
        totalIdealShots = sum(idealCounts.values())
        if totalIdealShots != shots:
            raise ValueError(f'the sum of the idealCounts shots [{totalIdealShots}] total number of shots [{shots}] when creating a BenchmarkCircuit')
        
        self.circuit = circuit
        self.idealCounts = idealCounts
        self.shots = shots

    """
        Creates a benchmark circuit of a single Rz rotation of theta degrees (Rz(theta)) and determines the ideal counts
        The way it is able to still measure in the 0,1 basis is that I apply a hadimar before and after the Rz rotation
        Circuit:
                q0 --H--Rz(theta)--H---M
    """
    @classmethod
    def singleRzBenchmark(cls, theta:float, shots:int=1000):
        
        qc = QuantumCircuit(1,1)
        qc.h()
        qc.rz(theta,0)
        qc.h()

        # calculate the ideal counts. Note, Rz(theta) corresponds to Ry(theta)
        # this means theta=0 or 2pi --> |0>, theta=pi --> |1>, theta = -3pi/2 or pi/2 --> |->, theta = -pi/2 or 3pi/2 --> |+>
        ideal1Prob = 1-np.cos(theta)
        ideal1Cnts = np.ceil(shots*ideal1Prob)
        ideal0Cnts = shots - ideal1Cnts
        
        idealCounts = {'1':ideal0Cnts, '0':ideal0Cnts}

        return cls(
            circuit = qc,
            idealCounts = idealCounts,
            shots = shots
        )
    
    """
        Creates a benchmark circuit that runs QFT of size numQbits followed by QFT^-1 which should output the same bitstring as the input
        Params:
            numQbits: the number of qubits in the QFT circuit
            inputStr: the initial string passed to QFT (i.e. '011' -> 3)
            shots: the number of shots to run (used to calculate the ideal counts)
    """
    @classmethod
    def QFTandInvBenchmark(cls, numQbits:int, inputStr:str, shots:int=1000):

        if len(inputStr) != numQbits:
            raise ValueError(f'QFTandInvBenchmark: inputStr param [{inputStr}] needs to be the same length as numQbits [{numQbits}]')

        qc = QuantumCircuit(numQbits,numQbits)
        
        #set up the input to be the inputStr by applying X gates to qbits that need to be 1
        for i, bit in enumerate(reversed(inputStr)):
            if bit == '1':
                qc.x(i)

        #create a qft circuit as a gate and apply it followed by its inverse
        qft_gate = QFT(num_qubits=numQbits, do_swaps=True).to_gate()  #do_swaps=True so the order of the qbits stays the same
        qc.append(qft_gate,range(numQbits))  
        qc.append(qft_gate.inverse(), range(numQbits))

        #measure all the qbits
        qc.measure(range(numQbits), range(numQbits))

        idealCounts = {inputStr:shots} #since we applied QFT then QFT^-1 the output string should be the same as the input

        return cls(
            circuit = qc,
            idealCounts = idealCounts,
            shots = shots
        )
    
    """
        #TODO: add benchmark for QAOA if I have time
    """
