#!/usr/bin/env python3

# Homework Assignment 3 
# Requirements: Given a function, and possible values for the variables
#  calculate the number of permutations, solve for all possible solutions,
#  run the above with multiprocessing
# Owner: Dominic Pontious

# Makes use of factorial
import math

def numberOfPermutations(numbers):
	"""
	Goes through a list of integers and returns the number of possible permutations
	Input: numbers [<int>]
	Output: numberPermutations <int>
	"""

	# Create a dictionary from the list with the key as the integer and the value as the times that number appears in the list
	numberDict = {}
	for number in numbers:

		# Checks if the number is a key already, if it is add one to the value
		if number in numberDict.keys():
			numberDict[number] = numberDict[number] + 1

		else:
			numberDict[number] = 1


	duplicateNumbers = 1
	# Calculates total number of permutation duplications
	# This is giving me the denominator for the permutation formula
	# values!/(duplicate a)!(duplicate b)! and so on
	for duplicate in numberDict:

		factorialNumber = math.factorial(numberDict[duplicate])
		duplicateNumbers = duplicateNumbers * factorialNumber

	# Gives me the total number of possible permutations
	numberPermutations = (math.factorial(len(numbers)) / duplicateNumbers)


	return numberPermutations

def listAllPermutations(numbers):
	"""
	Given a list of integers, return a list of a list containing int permutations
	Input: numbers [<int>]
	Output: listPermutations [ [<int>] ]
	"""

	# Create a dictionary from the list with the key as the integer and the value as the times that number appears in the list
	numberDict = {}
	for number in numbers:

		# Checks if the number is a key already, if it is add one to the value
		if number in numberDict.keys():
			numberDict[number] = numberDict[number] + 1

		else:
			numberDict[number] = 1

	# Goes through every permutation
	permutationsLeft = numberOfPermutations(numbers)

	# Uses index as the key
	index = 1
	permList = {1 : []}
	while(permutationsLeft != 0):


		#Creates a dictionary containing every permutation where the key is just a count 0 through permutationsLeft-1
		for num in numbers:
			permDict[index] = permDict[index].append(num)
		

		print("There are: " + str(permutationsLeft) + " permutations left")
		for key in permDict:
			print ("Key of permDict: " + str(key) + " and value " + str(permDict[key]))

		permutationsLeft = permutationsLeft -1
		index = index +1



# Test to make sure my functions work atm
def main():
	numberList = [1, 2, 4, 4, 5]
	numberList1 = [1, 1, 1, 1, 1, 2]
	permutations = numberOfPermutations(numberList)
	print("And there are: " + str(permutations))

	permutations1 = numberOfPermutations(numberList1)
	print("And there are: " + str(permutations1))
	listAllPermutations(numberList1)




# This is a check to make sure the script is being handled correctly
if (__name__ == "__main__"):
	main()

else:
	print("Did not run main function")
