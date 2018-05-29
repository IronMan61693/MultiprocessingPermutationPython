#!/usr/bin/env python3

# Homework Assignment 3 
# Requirements: Given a function, and possible values for the variables
#  calculate the number of permutations, solve for all possible solutions,
#  run the above with multiprocessing
# Owner: Dominic Pontious

# Uses permutation calculator
from itertools import permutations

from numberOfPermutations import numberOfPermutations, listAllPermutations

# Use for command line interface
import argparse

import re

def parseEquationNums(equationAsString):
	operators = set('+-*/=')
	ops_caught = []
	nums_caught = []
	buff_dude = []

	# Begin analyzing the string one character at a time
	for c in equationAsString:
		# We have come across an operator
		# This means everything in the buffer is either a variable or number
		# We therefore want to join it together and put it in nums_caught
		if c in operators:
			nums_caught.append(''.join(buff_dude))
			# Resets the buffer
			buff_dude = []
			# Adds the operator to it's list in order
			ops_caught.append(c)

		# There is not yet an operator so add the character to the buffer
		else: 
			buff_dude.append(c)

	# We have gotten to the end
	nums_caught.append(''.join(buff_dude))

	# Returns the numbers/variables and the operators as two lists, which are in order, 
	# and if we alternate starting with nums caught we should be able to recreate the equation 
	return nums_caught

def parseEquationOps(equationAsString):
	operators = set('+-*/=')
	ops_caught = []
	nums_caught = []
	buff_dude = []

	# Begin analyzing the string one character at a time
	for c in equationAsString:
		# We have come across an operator
		# This means everything in the buffer is either a variable or number
		# We therefore want to join it together and put it in nums_caught
		if c in operators:
			nums_caught.append(''.join(buff_dude))
			# Resets the buffer
			buff_dude = []
			# Adds the operator to it's list in order
			ops_caught.append(c)

		# There is not yet an operator so add the character to the buffer
		else: 
			buff_dude.append(c)

	# We have gotten to the end
	nums_caught.append(''.join(buff_dude))


	# Returns the numbers/variables and the operators as two lists, which are in order, 
	# and if we alternate starting with nums caught we should be able to recreate the equation 
	return ops_caught


def main():
	# perma = permutations([1,2,3,4,5,6,7,8,9])
	# 1 + 2 * 3 = 7
	# 1 + 3 * 2 = 7
	# return those two permutations

	# Hard coding in numbers to get the concept to work


	# listPerm = list(perma)
	solutions = []
	# print("Please input the equation you would like solved in the form: x+x*13+10 = 23 \n\
	# 	   Use x for every variable you would like solved please \n")

	# equationString = str(input('Also please do not use 13x seperate it as 13 * x \n'))
	# numList = parseEquationNums(equationString)
	# opsList = parseEquationOps(equationString)


	# for a in numList:
	# 	print("Check num")
	# 	print(str(a))

	# for b in opsList:
	# 	print("Check op")
	# 	print(b)

	# numberOfVariables = numList.count('x')
	# print("There are: " + str(numberOfVariables) + " variables")

	

	possibleValues = input('Please input the possible values with spaces and as integers: ')
	possibleValuesList = [int(x) for x in possibleValues.split()]

	# Note both list and this works
	for element in listAllPermutations(possibleValuesList):
		# count = 0
		# for n,i in enumerate(numList):
		# 	if i == 'x':
		# 		numList[n] = element[count]
		# 		count = count + 1 

		if ((element[0] + 13 * element[1] / element[2] + element[3] + 12 * element[4] - element[5] - 11 + element[6] * element[7]\
		 	/ element[8] - 10 == 66) and (element not in solutions)):
			
			 solutions.append(element)


		# print(str(element))

	for answer in solutions:
		print("An answer is " + str(answer))

	print("The total number of answers is: " + str(len(solutions)))




# This is a check to make sure the script is being handled correctly
if (__name__ == "__main__"):
	main()

else:
	print("Did not run main function usingPermCalculator")