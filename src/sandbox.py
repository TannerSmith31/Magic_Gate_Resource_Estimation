from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from logicalQubit import LogicalQubit #This is the logical qubit I created (likely wont be used)


###### QISKIT SIMPLE CIRCUIT EXAMPLE #####
# 1. Create a circuit with 2 qubits
qc = QuantumCircuit(2,2)

# 2. Add a Hadamard gate on qubit 0
qc.h(0)

# 0-----[H]-----
# 1-------------

# 3. Add a CNOT gate (Control: 0, Target: 1)
qc.cx(0, 1)

# 0---[H]---C----
# 1---------X----

# 4. Measure both qubits
qc.measure([0, 1], [0, 1])

print(qc.draw(output='text'))

# 5. Simulate the circuit
simulator = AerSimulator()
job = simulator.run(qc, shots=1024)
result = job.result()

# 6. Get the results
counts = result.get_counts()
print(f"Measurement results: {counts}")






############## STIM STUFF #######
Lqubit = LogicalQubit(x_offset = 1, y_offset=0, d_x=3, d_z=3)
Lqubit.printLattice()

# class SCCircut():

# circuit = stim.Circuit("""
#     H 0
#     CNOT 0 1
#     M 0 1                   
# """)

# sampler = circuit.compile_sampler()

# samples = sampler.sample(shots=10)

# print("Results of 10 shots (Qubit 0, Qubit 1):")
# print(samples)

# circuit = stim.Circuit.generated(
#     "surface_code:rotated_memory_z",
#     distance=3,
#     rounds=10,
#     after_clifford_depolarization=0.001 # Adding 0.1% noise
# )

# print(circuit)