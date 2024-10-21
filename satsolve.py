#!/usr/bin/env python
'''
ECE 4524 Project 5
Logan Lynch
2022 - 04 - 27

SAT solver using DPLL
'''
import sys
import fileparser

# Attempts to find an existing unit clause in the formula
def find_unit_clause(formula):
	#formula = [clause for clause in formula if not len(clause) == 1]
	for clause in formula:
		if len(clause) == 1:
			literal = clause.pop()
			clause.add(literal)
			return literal
	return None

def unit_propogate(literal, formula):
	# Remove every clause containing the literal
	formula = [clause for clause in formula if not literal in clause]
	
	# Remove every literal's compliment
	new_formula = []
	for clause in formula:
		clause = {old_literal for old_literal in clause if not (old_literal[0] == literal[0] and old_literal[1] != literal[1])}
		new_formula.append(clause)
	
	return new_formula

# Attempt to find a pure literal
def find_pure_literal(formula):
	for clause in formula:
		for literal in clause:
			pure = True
			for comp_clause in formula:
				for comp_literal in comp_clause:
					#print('Comparing ' + str(comp_literal) + ' and ' + str(literal))
					if (comp_literal[0] == literal[0]) and (comp_literal[1] != literal[1]):
						pure = False
			if pure:
				return literal
	return None

# Remove pure literal from formula
def pure_literal_propogate(literal, formula):
	formula = [clause for clause in formula if not literal in clause]
	return formula

# Return first literal in formula
def choose_first_literal(formula):
	for clause in formula:
		for literal in clause:
			return (literal[0], literal[1])

def dpll(formula, model):
	dpll.counter += 1
	while find_unit_clause(formula) is not None:
		literal = find_unit_clause(formula)
		formula = unit_propogate(literal, formula)
		# Add assignment to dict
		model[literal[0]] = literal[1]
	
	while find_pure_literal(formula) is not None:
		literal = find_pure_literal(formula)
		#print('Found Pure Literal: ' + str(literal))
		formula = pure_literal_propogate(literal, formula)
		# Add assignment to dict
		model[literal[0]] = literal[1]
	
	# Satisfied if all clauses are removed
	if (len(formula) == 0):
		return True, model
	
	# Unsatisfiable if the empty clause is reached
	if any(len(clause) == 0 for clause in formula):
		return False, None
	
	literal = choose_first_literal(formula)
	new_formula = unit_propogate((literal[0], 'True'), formula)
	model[literal[0]] = 'True'
	sat, vals = dpll(new_formula, model)
	if sat:
		return sat, vals
	
	new_formula = unit_propogate((literal[0], 'False'), formula)
	model[literal[0]] = 'False'
	sat, vals = dpll(new_formula, model)
	if sat:
		return sat, vals
	
	return False, None
dpll.counter = 0

def satsolve(filename):
	formula, num_vars = fileparser.parse(filename)
	#print('Formula: ' + str(formula))
	sat, values = dpll(formula, model = {})
	print("Test Case: " + filename)
	if sat:
		print("DPLL: SAT")
		print("Calls: " + str(dpll.counter))
		out_str = ''
		for x in range(int(num_vars)):
			# Default to Zero if value not in dict (Can be true or false)
			num_entry = 0
			entry = values.get(str(int(x) + 1))
			if entry == 'True':
				num_entry = 1
			out_str += str(num_entry)
		print(out_str)
	else:
		print("DPLL: UNSAT")

if __name__ == "__main__":
	satsolve("c17.txt")
	satsolve("hole6.txt")
	satsolve("testcase1.txt")
	satsolve("testcase-aim-50-1_6-yes1-4.txt")
	satsolve("testcase-quinn.txt")
	satsolve("dubois20.txt")
	satsolve("dubois21.txt")
	satsolve("dubois22.txt")
	satsolve("testcase-aim-100-1_6-no-1.txt")
