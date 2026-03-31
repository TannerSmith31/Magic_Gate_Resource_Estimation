from magicFactory import MagicFactory
from qiskit import QuantumCircuit
from qiskit_aer.noise import NoiseModel, pauli_error
from circuitDecomposer import CircuitDecomposer
from qiskit.converters import circuit_to_dag
from utils import QuantumGate
from qiskit_aer import AerSimulator

#TODO: go through and change the decompPrecision variable to be a mp floating point rather than just a float.
class ResourceEstimator:
    magicFactories: list[MagicFactory]   # List of magic factories on the chip to run the algo
    quantumCircuit: QuantumCircuit       # The circuit to be run
    decomposedCircuit: QuantumCircuit    # The circuit to be run decomposed into clifford + magic gates that can be produced by the factories
    basisGateset: list[QuantumGate]      # basis gateset for this estimator (clifford + the magic gates that can be produced by the factories)
    magicGateset: list[QuantumGate]        # set of magic gates being distilled
    codeDistance: int                    # The code distance of error correction on the circuit
    p_phys: float

    def __init__(self, magicFactories: list[MagicFactory], quantumCircuit: QuantumCircuit, codeDistance:int, p_phys:float, decompPrecision:float):
        self.magicFactories = magicFactories
        self.quantumCircuit = quantumCircuit
        self.codeDistance = codeDistance
        self.p_phys = p_phys

        # Look at the list of magic factories and decompose the circuit into the available gates.
        magicGateset = {factory.gate for factory in self.magicFactories} #create a set of gates from the magic factory
        basisGateset = list(magicGateset) #convert the magic gateset to a list and assign those gates into the basis gateset, then iterate through the nonclifford gates and add them
        for gate in QuantumGate:
            if gate.isClifford():
                basisGateset.append(gate)
        
        self.basisGateset = list(basisGateset)
        self.magicGateset = magicGateset
        self.decomposedCircuit = self.decomposeToCliffordPlusMagic(self, decompPrecision) #decompose the circuit and set it in the estimator

    """
        Function to decompose circuit into Clifford + whatever magic state is made by the factories
            precision: How close we want each gate to be to the target unitary (TODO: determine if this should be per gate, or full circuit decomp precision [i.e. we want the full circuit, when treated as a unitary, to be within the precision of the original])
    """
    def decomposeToCliffordPlusMagic(self, precision:float):
        # Raise an error if magicFactories or quantumCircuit is null.
        if self.magicFactories == None:
            raise ValueError("ResourceEstimator.magicFactories should not be null.")
        if self.quantumCircuit == None:
            raise ValueError("ResourceEstimator.quantumCircuit should not be null.")

        # create a decomposer for our gateset and decompose the circuit
        decomposer = CircuitDecomposer(self.basisGateset, precision, self.quantumCircuit)
        decomposedCircuit = decomposer.decomposeToGateset()
        return decomposedCircuit
    
    """
        calculates the total number of physical qubits needed to run the algorithm (factories + algorithm)
    """
    def calcFootprint(self):
        # Calculate the total area of factories
        magicFactoryFootprint = 0 #initialize a counter for the qubits required for all factories
        for mFactory in self.magicFactories:
            magicFactoryFootprint += mFactory.qubitFootprint
        
        #Calculate the physical qubits required for the algorithm based on code distance
        logicalQubits = self.quantumCircuit.num_qubits()            #each qubit in the algorithm is a logical qubit
        logicalQubitFootprint = 2 * self.codeDistance**2 - 1    #surface codes are a [2d^2-1, 1, d] code so it takes 2d^2-1 physical qubits to implement 1 logical qubit
        circuitFootprint = logicalQubits * logicalQubitFootprint

        #TODO: account for routing / lattice surgery? or ignore routing? maybe give a flat 10% for routing or something?

        return magicFactoryFootprint + circuitFootprint
    
    """
        Function to calculate how long the algorithm will take to run. It considers the number of cycles needed to produces the required
        number of magic states and how many magic states can be produced per timestep
            decomposeQC: boolean telling whether to call the decompose function on the circuit within this object or nthe decomposed circuit
    """
    def calcRuntime(self, decomposeQC:bool = True):
        qc = None
        if decomposeQC:
            qc = self.decomposedCircuit
        else:
            qc = self.quantumCircuit
        
        circuitDAG = circuit_to_dag(qc) #get the circuit as a DAG
        magicDepths = {} #dictionary {QuantumGate:int} to store the magic gate and its depth in the circuit
        # for magicGate in self.magicGateset:
            # if magicGate == QuantumGate.T:
            #     magicDepths[magicGate] = circuitDAG.depth(filter_function=lambda x:x.name in ['t', 'tdg'])
            # if magicGate == QuantumGate.CCZ:
            #     magicDepths[magicGate] = circuitDAG.depth(filter_function=lambda x:x.name in ['ccz']) #TODO: figure out how qiskit does ccz gates


        #figure out what the longest path of gates is 
        #TODO: need a way to calculate how long the circuit will take to run
        #This will have to do with how many magic factories are running and how many cycles we need to wait for enough states
        #get the magic state depth. Figure out what magic factories are producing what states
        return

    """
        Function to run the circuit (decomposed or original depending on 'decomposeQC' variable) and determine runtime statistics of the algorithm (fidelity, etc.)
            shots: the number of shots to run
            decomposeQC: boolean to tell whether to run the decomposed circuit or the original circuit. Defaults to True (using the decomposed circuit)
            idealClifford: boolean to tell whether noise should be added to the circuit itself, or just to the magic gates
    """
    def runCircuit(self, shots:int=1000, decomposeQC:bool=True, idealCliffords:bool=True):
        ###GENERATING NOISE MODEL###
        p_th = 0.01  #based on surface codes from 'Surface codes towards practical quantum computing'
        
        ## Compute logical error rate
        if self.codeDistance == 0:
            p_L = self.p_phys  #no error correction
        else:
            exponent = (self.codeDistance + 1) / 2
            p_L = 0.03 * (self.p_phys / p_th)**exponent #LER eq based on 'Surface codes towards practical quantum computing'

        ##Build noise model
        noiseModel = NoiseModel()

        ## Add noise to cliffords if chosen
        if not idealCliffords:
            ## ONE QUBIT ERROR
            # Symmetric logical Pauli channel
            logical_error = pauli_error([
                ('X', p_L / 3),
                ('Y', p_L / 3),
                ('Z', p_L / 3),
                ('I', 1 - p_L)
            ])

            ## Apply to all logical single- and two-qubit gates
            all_gates = ['x', 'y', 'z', 'h', 'sx', 'id']
            noiseModel.add_all_qubit_quantum_error(logical_error, all_gates)
            
            ## 2 QUBIT ERROR
            # All 15 non-identity two-qubit Paulis
            paulis_2q = []
            single = ["I", "X", "Y", "Z"]

            for p1 in single:
                for p2 in single:
                    op = p1 + p2
                    if op != "II":
                        paulis_2q.append(op)

            prob_per_term = p_L / len(paulis_2q)

            two_qubit_channel = [(op, prob_per_term) for op in paulis_2q]
            two_qubit_channel.append(("II", 1 - p_L))
            two_qubit_error = pauli_error(two_qubit_channel)
            two_qubit_gates = ["cx", "cz", "swap"]

            noiseModel.add_all_qubit_quantum_error(two_qubit_error, two_qubit_gates)        
        
        ## TODO: add error to magic gates based on fidelity of factories
        #FOR EACH FACTORY
            #ADD ERROR TO THOSE MAGIC GATES BASED ON THE MAGIC GATE OUTPUT ERROR RATE

        backend = AerSimulator(noise_model = noiseModel)

        if decomposeQC:
            pass #TODO: run circuit on self.decomposedQC
        else:
            pass #TODO: run circuit on self.quantumCircuit

        ## return counts

        return

    """
        Do a resource analysis of the given circuit using the magic factories provided
        Determine cycles to run (runtime), space on chip (magic factory + errorcorrection + algo), 
    """
    def analyzeCircuit(self):
        #Decompose circuit based on magic factories  (ALREADY DONE WHEN RESOURCE ESTIMATOR IS CREATED. MAYBE CHANGE THIS TO BE DONE AFTER AND DECOMPOSED CIRCUIT IS PASSED IN?)

        #Calculate footprint

        #run circuit to get COUNTS

        # use COUNTS into a function that takes in counts and the circuit/algo run and determines fidelity (so somehow gets the ideal counts and compares)
        return
