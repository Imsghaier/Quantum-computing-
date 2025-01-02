import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randint
from math import gcd
from qiskit.visualization import plot_histogram
import pandas as pd
from fractions import Fraction
from qiskit_aer import Aer
from qiskit import QuantumCircuit, transpile

print("Imports Successful")

# Function to apply modular exponentiation
def qpe_amod15(a):
    n_count = 8
    qc = QuantumCircuit(4 + n_count, n_count)
    for q in range(n_count):
        qc.h(q)  # Initialize counting qubits in state |+>
    qc.x(3 + n_count)  # Initialize eigenstate |1>
    print("Initial Circuit after Hadamard Gates:")
    print(qc.draw(output='text'))  # For console output
    qc.draw(output='mpl', style={'fontsize': 12, 'subfont_size': 10, 'dpi': 300})
    plt.show(block=False)  # Non-blocking show
    plt.pause(2)  # Pause for 0.5 seconds to allow you to see the histogram
    plt.clf()



    # For Jupyter notebook
    for q in range(n_count):
        qc.append(controlled_U(a, 2**q), [q] + [i + n_count for i in range(4)])
    qc.append(QFT(n_count).inverse(), range(n_count))  # Apply inverse QFT
    # Draw the quantum circuit
    qc.measure(range(n_count), range(n_count))
    print("Final Circuit after measurement:")
    print(qc.draw(output='text'))  # Console output
    qc.draw(output='mpl', style={'fontsize': 12, 'subfont_size': 10, 'dpi': 300})
    plt.show(block=False)  # Non-blocking show
    plt.pause(15)  # Pause for 0.5 seconds to allow you to see the histogram
    plt.clf()
    #plt.show()
    #plt.clf()


    return qc
# Function to create controlled unitary gate
def controlled_U(a, power):
    U = QuantumCircuit(4)
    for iteration in range(power):
        U.swap(2, 1)
        U.swap(1, 0)
        if a in [7, 13]:
            U.swap(0, 2)
        U.cx(0, 2)
    U = U.to_gate().control()
    return U

# Quantum Fourier Transform (QFT) function
def QFT(n):
    circuit = QuantumCircuit(n)
    for j in range(n):
        for k in range(j):
            circuit.cp(np.pi / float(2**(j-k)), k, j)
        circuit.h(j)
    return circuit

# Run the main function
if __name__ == "__main__":


        # Perform the Quantum Phase Estimation to find the period
        np.random.seed(1)
        a = randint(2, 15)
        while gcd(a, 15) != 1:
            a = randint(2, 15)
        qc = qpe_amod15(a)
        simulator = Aer.get_backend('qasm_simulator')
        transpiled_qc = transpile(qc, simulator)
        results = simulator.run(transpiled_qc).result()
        counts = results.get_counts()
        plot_histogram(counts)
        plt.show(block=False)  # Non-blocking show
        plt.pause(7)  # Pause for 0.5 seconds to allow you to see the histogram
        plt.clf()



        # Extract the period r
        rows = [np.binary_repr(int(k, 2)).zfill(8) for k, v in counts.items() for i in range(v)]
        measurements = [int(row, 2) for row in rows]
        frac = Fraction(measurements[0], 2 ** 8).limit_denominator(15)
        r = frac.denominator

        print(f"Measured value of r: {r}")

        # Check if we found a non-trivial factor
        factor_found = False
        if r % 2 == 0:
            guess = (a ** (r // 2) - 1) % 15
            if guess != 1 and guess != 14:
                factor_found = True
                print(f"Non-trivial factor found: {gcd(guess, 15)}")

        if not factor_found:
            print("No non-trivial factors found. Try again.")

        print("Shor's Algorithm Finished")


