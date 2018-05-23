#!/usr/bin/env python3

# Homework Assignment 3 
# Requirements: Given a function, and possible values for the variables
#  calculate the number of permutations, solve for all possible solutions,
#  run the above with multiprocessing
# Owner: Dominic Pontious

# Uses permutation calculator
from itertools import permutations
from numberOfPermutations import numberOfPermutations


def main():
	perma = permutations([1,2,3,4,5,6,7,8,9])
	# 1 + 2 * 3 = 7
	# 1 + 3 * 2 = 7
	# return those two permutations

	# Hard coding in numbers to get the concept to work


	listPerm = list(perma)
	solutions = []
	for element in listPerm:
		totalPermutations = numberOfPermutations(listPerm)
		while (totalPermutations != 0):
			if ((element[0] + 13 * element[1] / element[2] + element[3] + 12 * element[4] - element[5] - 11 + element[6] * element[7]\
				 / element[8] - 10 == 66) and (element not in solutions)):
				solutions.append(element)

			totalPermutations = totalPermutations -1


		# print(str(element))

	for answer in solutions:
		print("An answer is " + str(answer))




# This is a check to make sure the script is being handled correctly
if (__name__ == "__main__"):
	main()

else:
	print("Did not run main function")