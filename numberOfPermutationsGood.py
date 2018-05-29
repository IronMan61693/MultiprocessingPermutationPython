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
	numberPermutations = (math.factorial(len(numbers)) // duplicateNumbers)


	return numberPermutations



def listAllPermutations(numbers):
	"""
	Given a list of integers, return a list of a list containing int permutations
	Input: numbers [<int>]
	Output: listPermutations [ (<int>) ]
	"""

	# Multi-process the brute force method

	minNumberList = sorted(numbers)
	maxNumberList = sorted(numbers,reverse = True)
	maxNumber = int("".join(str(x) for x in maxNumberList))
	minNumber = int("".join(str(x) for x in minNumberList))

	currentNumber = minNumber
	finalList = set()
	finalList.add(tuple(minNumberList))


	whileCount = 0
	maxCount = 1e9
	while (currentNumber <= maxNumber and whileCount < maxCount):
		whileCount += 1
		if (whileCount % 30000 == 0):
			print("+ 30000 while count listAllPermutations")
		# turns into a string and iterates over each digit and then puts each digit into a list
		digitsOfCurrentNum = [int(d) for d in str(currentNumber)]

		# Now I want to check if the list contains the appropriate digits exactly
		if (sorted(digitsOfCurrentNum) == minNumberList):
				finalList.add(tuple(digitsOfCurrentNum))

		currentNumber = currentNumber + 1

	if (whileCount >= maxCount):
		print("You done goofed in while loop listAllPermutations")
		exit(-1)
	return finalList





# Test to make sure my functions work atm
def main():
	numberList = [1, 2, 4, 4]
	numberList1 = [1, 2, 3]
	numberList2 = [1, 2]
	numberList3 = [1, 1, 1, 2]
	permutations = numberOfPermutations(numberList)
	print("And there are: " + str(permutations))

	permutations1 = numberOfPermutations(numberList1)
	print("And there are: " + str(permutations1))

	# listAllPermutations(numberList1)
	# allPermutations = listAllPermutations(numberList)
	# for perm in allPermutations:
	# 	print(str(perm))

	allPermutations1 = listAllPermutations(numberList1)
	for perm in allPermutations1:
		print(str(perm))

	# allPermutations2 = listAllPermutations(numberList2)
	# for perm in allPermutations2:
	# 	print(str(perm))

	allPermutations3 = listAllPermutations(numberList3)
	for perm in allPermutations3:
		print(str(perm))




# This is a check to make sure the script is being handled correctly
if (__name__ == "__main__"):
	main()

else:
	print("Did not run main function numberOfPermutations")
