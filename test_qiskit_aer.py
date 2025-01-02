# Import Qiskit Aer
from qiskit_aer import Aer

# Check if Aer is accessible
print("Qiskit Aer is accessible!")

# Create a simple quantum circuit
from qiskit import QuantumCircuit, transpile

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Simulate the circuit
simulator = Aer.get_backend('qasm_simulator')
compiled_circuit = transpile(qc, simulator)
result = simulator.run(compiled_circuit).result()
counts = result.get_counts()

print("Simulation result:", counts)
