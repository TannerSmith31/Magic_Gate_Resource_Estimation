import pytest
from qiskit import QuantumCircuit
from src.resourceEstimator import ResourceEstimator
from src.magicFactory import MagicFactory
from src.utils import QuantumGate

def test_null_factory():
    """Ensures a ValueError is raised when the factory list is None."""
    mockCircuit = QuantumCircuit(2, 0)

    with pytest.raises(ValueError):
        mockEstimator = ResourceEstimator(None, mockCircuit, 5, 1e-3)

def test_clifford_plus_t():
    """Ensures the decomposition runs without errors for a standard T-gate circuit."""
    mockCircuit = QuantumCircuit(4, 0)
    mockFactory = MagicFactory([QuantumGate.T], {QuantumGate.T:15}, {QuantumGate.T:1}, {QuantumGate.T:0.001}, 5.5, 16.5, 200, 3)
    mockCircuit.rz(0.3, 0)

    estimator = ResourceEstimator([mockFactory], mockCircuit, 5, 1e-3, 1e-8)
    # Pytest automatically fails if an uncaught exception is raised here
    estimator.decomposeToCliffordPlusMagic(1)