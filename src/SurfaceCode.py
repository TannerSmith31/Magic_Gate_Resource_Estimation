import stim


circuit = stim.Circuit("""
    H 0
    CNOT 0 1
    M 0 1                   
""")

sampler = circuit.compile_sampler()

samples = sampler.sample(shots=10)

print("Results of 10 shots (Qubit 0, Qubit 1):")
print(samples)
