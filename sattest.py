#!/usr/bin/env python

import satsolve
import random
import matplotlib.pyplot as plt

def create_formula(num_clauses):
	result = []
	for _ in range(num_clauses):
		conj = set()
		for _ in range(3):
			index = random.randint(0, 50)
			conj.add((str(index), bool(random.randint(0,2))))
		result.append(conj)
	return result

def main():
	ratio = []
	runtime = []
	for x in range(400):
		formula = create_formula(x)
		satsolve.dpll(formula, {})
		count = satsolve.dpll.counter
		
		ratio.append(x / 50)
		runtime.append(count)
		#print('Ratio: ' + str(x / 50) + ', Runtime: ' + str(runtime))
	
	fig, ax = plt.subplots()
	ax.scatter(ratio, runtime)
	plt.show()
	
if __name__ == '__main__':
	main()
