from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from typing import Literal
from pygridsynth.gridsynth import gridsynth_gates, gridsynth_circuit
from utils import QuantumGate
import mpmath
import numpy as np

from utils import dagger

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
		# Use numpy matrices.
		#if 'T' in self.gateSet:
			#return self.decomposeToCliffordPlusT()
		#TODO: take the original circuit from this object and decompose it into the gateSet of this object

		#TODO: set the decomposedCircuit to the one we just created and then return the decomposed circuit
		return "TODO: IMPLEMENT decomposeToGateset function"
	
	def basicApproximationHelper(self, numGates, currSet):
		if numGates == 0:
			return currSet
		else:
			newSet = currSet
			for combination in currSet:
				for gate in self.gateSet:
					newSet.add(combination + gate)
			return "TODO: Implement basicApproximationHelper function."
	
	def basicApproximation(self, U):
		options = self.basicApproximationHelper(6, set(self.gateSet)) # TODO: Find a good numGates.
		return "TODO: Implement basicApproximation function."
	
	def gcDecompose(self, input):
		return "TODO: Implement gcDecompose function."

	# function Solovay-Kitaev(Gate U , depth n)
	def solovayKitaev(self, U , n):
		# if (n == 0)
		if n == 0:
			# Return Basic Approximation to U
			return self.basicApproximation(U)
		# else
		else:
			# Set Un−1 = Solovay-Kitaev(U, n − 1)
			UNMinusOne = self.solovayKitaev(U, n - 1)
			# Set V , W = GC-Decompose(U U^†_{n − 1})
			V, W = self.gcDecompose(np.dot(U, dagger(UNMinusOne)))
			# Set Vn−1 = Solovay-Kitaev(V ,n − 1)
			VNMinusOne = self.solovayKitaev(V, n - 1)
			# Set Wn−1 = Solovay-Kitaev(W ,n − 1)
			WNMinusOne = self.solovayKitaev(W, n - 1)
			# Return Un = Vn−1Wn−1V †  n−1W †  n−1Un−1;
			return np.dot(np.dot(np.dot(np.dot(VNMinusOne, WNMinusOne), dagger(VNMinusOne)), dagger(WNMinusOne)), UNMinusOne)
	
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

		# Might use SK instead for consistency of comparison.
		return self.decomposedCircuit
