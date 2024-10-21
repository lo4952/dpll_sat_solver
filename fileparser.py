#!/usr/bin/env python
'''
ECE 4524 Project 5
Logan Lynch
2022 - 04 - 27

A parser to read clauses from cnf files 
'''
import sys

def parse(filename):
	clauses = []
	for line in open(filename):
		c = set()
		if line.startswith('c'):
			continue
		if line.startswith('p'):
			num_vars = line.split()[2]
			continue
		for x in line[:-2].split():
			if x.startswith('-'):
				literal = (x[1:], 'False')
				c.add(literal)
			elif x != '0':
				literal = (x, 'True')
				c.add(literal)
		clauses.append(c)
	return clauses, num_vars
