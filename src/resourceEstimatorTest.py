import mpmath

from resourceEstimator import ResourceEstimator
from qiskit import QuantumCircuit
from magicFactory import MagicFactory

# Test the null value errors for decomposeToCliffordPlusMagic().
def testNullCircuit():
	try:
		factory = MagicFactory("", 0, 0, 0, 0, 0)
		estimator = ResourceEstimator([factory], None)
		estimator.decomposeToCliffordPlusMagic(1)
	except ValueError:
		pass
	else:
		raise Exception("testNullCircuit() failed.")

def testNullFactory():
	try:
		circuit = QuantumCircuit(2, 0)
		estimator = ResourceEstimator(None, circuit)
		estimator.decomposeToCliffordPlusMagic(1)
	except ValueError:
		pass
	else:
		raise Exception("testNullFactory() failed.")
	
def testCliffordPlusT():
	circuit = QuantumCircuit(4, 0)
	factory = MagicFactory("T", 0, 0, 0, 0, 0)

	circuit.rz(0.3, 0)

	estimator = ResourceEstimator([factory], circuit)
	estimator.decomposeToCliffordPlusMagic(1)

testNullCircuit()
testNullFactory()
testCliffordPlusT()