import numpy as np
import random
import math
from tqdm import tqdm

def sigmoid(x):

	round(x, 10)
	return 1.0 / (1.0 + math.exp(-x))

def sigmoid_der(x):
	return x*(1.0-x)


class Network:

	def __init__(self, n_inputs, n_hidden, n_outputs):

		self.layers = []
		self.create_network(n_inputs, n_hidden, n_outputs)

	def create_network(self, n_inputs, n_hidden, n_outputs):

		hidden_neurons = []

		for neuron in range(n_hidden):
			weights = [random.random() for _ in range(n_inputs)]
			biases = [random.random()]

			hidden_neurons.append(Neuron(weights, biases))

		self.layers.append(Layer(hidden_neurons))


		output_neurons = []

		for neuron in range(n_outputs):

			weights = [random.random() for _ in range(n_hidden)]
			biases = [random.random()]

			output_neurons.append(Neuron(weights, biases))

		self.layers.append(Layer(output_neurons))

	def forward_propagate(self, row):

		next_inputs = row
		for layer in (self.layers):

			hidden_neurons = []
			for neuron in layer.neurons:
				
				neuron.activate(next_inputs)
				
				# print(f"{next_inputs}")
				# print(neuron.weights)
				# print(neuron.bias)
				# print(neuron.output)
				# print("niggor\n")
				hidden_neurons.append(neuron.output)

			next_inputs = hidden_neurons

		output = next_inputs
		return output

	# ALWAYS DO FORWARD PROPAGATE FIRST, ELSE ITLL MESS UP THE FUNCS
	def backward_propagate(self, labels):

		for i in reversed(range(len(self.layers))):

			layer = self.layers[i]
			error = []

			if i != len(self.layers) -1:

				for j in range(len(layer.neurons)):

					error_el = 0.0

					for neuron in self.layers[i+1].neurons:

						error_el += (neuron.weights[j] * neuron.delta)

					error.append(error_el)

			else:

				for j in range(len(layer.neurons)):

					neuron = layer.neurons[j]
					error.append(labels[j] - neuron.output)

			for j in range(len(layer.neurons)):

				neuron = layer.neurons[j]
				neuron.delta = error[j] * sigmoid_der(neuron.output)

	def update_weights(self, feature_set, lr):

		for i in range(len(self.layers)):
			inputs = feature_set
			if i != 0:
				inputs = [neuron.output for neuron in self.layers[i-1].neurons]

			for neuron in self.layers[i].neurons:
				for j in range(len(inputs)):

					#print(neuron.weights[j])
					neuron.weights[j] += lr * neuron.delta * inputs[j]


				neuron.bias += lr * neuron.delta

	def train_network(self, feature_set, labels, n_epochs, lr):

		for epoch in (range(n_epochs)):
			sum_error = 0
			for idx,row in enumerate(feature_set):
				outputs = self.forward_propagate(row)
				expected = labels[idx]

				sum_error += sum([(expected[i] - outputs[i])**2 for i in range(len(expected))])
				self.backward_propagate(expected)
				self.update_weights(row, lr)

			print(f"The error is: {sum_error}")

	def predict(self, test_data, test_labels):

		accuracy = 0.0
		data_size = len(test_data)

		for idx in range(data_size):

			outputs = self.forward_propagate(test_data[idx])			
			expected = test_labels[idx]


			same_outputs = 0
			for x in range(len(outputs)):

				print(len(expected))
				print(x)

				print(f"predicted: {outputs[x]} && expected: {expected[x]}")
				if round(outputs[x]) == expected[x]:
		
					same_outputs += 1

			if same_outputs == len(outputs):
				accuracy += 1/data_size * 100

		return accuracy


	def get_labels(self, plr, item):

		moveX = 0
		moveY = 0

		if plr.posx > item.posx + item.size :

			moveX = [0, 0] # move left 

		elif plr.posx< item.posx:

			moveX = [0, 1] # move right

		else:
			moveX = [1,0] # dont move at all

		if plr.posy > item.posy + item.size :

			moveY = [0, 0] # move left 
			

		elif plr.posy < item.posy:

			moveY = [0, 1] # move right 

		else:
			
			moveY = [1,0] # dont move at all

		return moveX + moveY

	def right_wrong(self, d_before, d_after):

		if d_before > d_after:
			return 1
		else:
			return 0





class Neuron:

	def __init__(self, weights, bias):

		self.weights = weights
		self.bias = bias[0]

		self.output = 0.0
		self.delta = 0.0

	def activate(self, inputs):

		activation = self.bias
		for x in range(len(self.weights)):
			activation += self.weights[x] * inputs[x]

		
		'''
		if type(activation) == np.ndarray: 
			activation = round(activation.item()/ len(self.weights), 100)
		else:
			activation = round(activation/ len(self.weights), 100)
		'''

		self.output = sigmoid(activation)

class Layer:

	def __init__(self, neurons):

		self.neurons = neurons



if __name__ == "__main__":

	feature_set = [[2.7810836,2.550537003],
							[1.465489372,2.362125076],
							[3.396561688,4.400293529],
							[1.38807019,1.850220317],
							[3.06407232,3.005305973],
							[7.627531214,2.759262235],
							[5.332441248,2.088626775],
							[6.922596716,1.77106367],
							[8.675418651,-0.242068655],
							[7.673756466,3.508563011]] # 5 person with 3 qualities: (smoking, obesity, excercise)
	#feature_set = np.array([[0,2,0],[0,0,2],[2,0,0],[1,12,0],[4,40,1]]) 
	labels = [[0, 1],[0, 0],[0, 0],[0, 1] ,[0, 0], [1, 0],[1, 1],[1,0],[1, 1],[1, 1]] # return of isDeabetic for each person

	nn = Network(2, 4, 2)
	before_train = (nn.layers[0].neurons[0].weights)[:]
	
	nn.train_network(feature_set, labels, 1000, 0.5)

	output = nn.forward_propagate([0,1,1])
	

	after_train = (nn.layers[0].neurons[0].weights)

	print(before_train)
	print(after_train)
	print(nn.predict(feature_set, labels))