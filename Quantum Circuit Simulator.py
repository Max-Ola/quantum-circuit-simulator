import numpy as np

# Quantum gate definitions
I = np.array([[1, 0], [0, 1]])
X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.array([[1, 0], [0, -1]])
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
S = np.array([[1, 0], [0, 1j]])
CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])

# Helper functions for state manipulation
def tensor_product(matrix1, matrix2):
    return np.kron(matrix1, matrix2)

def apply_gate(state, gate, target_qubits):
    gate_size = int(np.log2(gate.shape[0]))
    num_qubits = int(np.log2(state.shape[0]))
    for target_qubit in target_qubits:
        tensor_gates = [I] * num_qubits
        tensor_gates[target_qubit] = gate
        tensor_gate = tensor_gates[0]
        for tensor in tensor_gates[1:]:
            tensor_gate = tensor_product(tensor_gate, tensor)
        state = np.dot(tensor_gate, state)
    return state

# Quantum Circuit class
class QuantumCircuit:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.num_states = 2 ** num_qubits
        self.state = np.zeros(self.num_states, dtype=np.complex128)
        self.state[0] = 1  # Initialize to |0>

    def apply_gate(self, gate, target_qubits):
        self.state = apply_gate(self.state, gate, target_qubits)

    def measure(self, target_qubit):
        probabilities = np.abs(self.state) ** 2
        result = np.random.choice(range(self.num_states), p=probabilities)
        self.state = np.zeros(self.num_states, dtype=np.complex128)
        self.state[result] = 1
        return bin(result)[2:].zfill(self.num_qubits)

    def simulate(self):
        return self.state

# Example usage
num_qubits = 2
qc = QuantumCircuit(num_qubits)

# Apply gates
qc.apply_gate(H, [0])
qc.apply_gate(CNOT, [0, 1])
qc.apply_gate(X, [1])

# Perform measurement
measurement_result = qc.measure(1)
print("Measurement result:", measurement_result)

# Simulate the circuit
final_state = qc.simulate()
print("Final state:", final_state)

