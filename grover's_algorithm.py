# Import necessary modules from Qiskit
import numpy as np
from qiskit_aer import Aer
from qiskit.circuit.library import MCXGate
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Define the oracle for the 4-qubit Grover's algorithm
def oracle(circuit, qubits):
    circuit.h(qubits[-1])
    # Use MCXGate (multi-controlled X gate) as an alternative to mct
    circuit.append(MCXGate(num_ctrl_qubits=len(qubits) - 1), qubits)
    circuit.h(qubits[-1])

# Define the diffuser (inversion about the mean)
def diffuser(circuit, qubits):
    circuit.h(qubits)
    circuit.x(qubits)
    circuit.h(qubits[-1])
    # Use MCXGate (multi-controlled X gate) as an alternative to mct
    circuit.append(MCXGate(num_ctrl_qubits=len(qubits) - 1), qubits)
    circuit.h(qubits[-1])
    circuit.x(qubits)
    circuit.h(qubits)

if __name__ == "__main__":
    # Create a quantum circuit with 4 qubits and 4 classical bits
    n = 4
    grover_circuit = QuantumCircuit(n, n)

    # Apply Hadamard gates to all qubits to create a superposition
    grover_circuit.h(range(n))

    # Apply the Grover operator (oracle followed by diffuser) N^(1/2) times
    num_iterations = int(np.sqrt(2**n))

    for _ in range(num_iterations):
        oracle(grover_circuit, range(n))
        diffuser(grover_circuit, range(n))

    # Measure the qubits
    grover_circuit.measure(range(n), range(n))
    # Execute the circuit on a simulator
    simulator = Aer.get_backend('qasm_simulator')

    # Transpile the circuit
    transpiled_circuit = transpile(grover_circuit, simulator)

    # Run the assembled job with 2048 shots
    result = simulator.run(transpiled_circuit, shots=2048).result()  # Using simulator.run with shots parameter

    # Get and plot the results
    counts = result.get_counts()
    print('RESULT: ', counts, '\n')
    print("Grover's algorithm test completed successfully!")
    # Draw the circuit
    plt.ion()  # Turn on interactive mode
    grover_circuit.draw(output='mpl')
    plt.ioff()  # Turn off interactive mod
    # Plot the results of the counts of the qubits
    plot_histogram(counts)
    plt.show()

