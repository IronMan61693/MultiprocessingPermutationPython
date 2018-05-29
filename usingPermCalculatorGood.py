#!/usr/bin/env python3

# Homework Assignment 3 
# Requirements: Given a function, and possible values for the variables
#  calculate the number of permutations, solve for all possible solutions,
#  run the above with multiprocessing
# Owner: Dominic Pontious

from numberOfPermutationsGood import numberOfPermutations, listAllPermutations




def main():

	solutions = []
	

	possibleValues = input('Please input the possible values with spaces and as integers: ')
	possibleValuesList = [int(x) for x in possibleValues.split()]

	# Note both list and this works
	possibleSet = set(listAllPermutations(possibleValuesList))
	for element in possibleSet:
		# (element[0] + 13 * element[1] / element[2] + element[3] + 12 * element[4] - element[5] - 11 + element[6] * element[7]\
		 #	/ element[8] - 10 == 66)
		if (element[0] + 2 * element[1] / element[2] + element[3] + 12 * element[4] == 43 and (element not in solutions)):
			
			 solutions.append(element)


	for answer in solutions:
		print("An answer is " + str(answer))

	print("The total number of answers is: " + str(len(solutions)) + " out of the following permutations: " + str(numberOfPermutations(possibleValuesList)))




# This is a check to make sure the script is being handled correctly
if (__name__ == "__main__"):
	main()

else:
	print("Did not run main function usingPermCalculator")