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

	'''
	Attempt 1
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

	'''

	'''
	Attempt 2
	# This gives me how many numbers are input, including duplicates
	howManyNumbers = len(numbers)

	# range(number) goes through every integer from 0 to the number
	# so by creating an n by n sized array{mathematic array not cs} we are
	# able to look at every combination
	# take the numbers are 1 and 2, the howManyNumbers = 2
	# then we would check over 2**2 = 2^2 = 4, or imagine a 
	# 2 by 2 square which each side contains a value 1 or 2
	# now as we join these combinations we get every combination with duplicates
	finalList = [numbers]
	for n in range(howManyNumbers**howManyNumbers):
		individualList = []
		# This is going through each dimension and creating a list of the elements along the dimension
		for d in range(howManyNumbers):
			individualList.append(numbers[n // howManyNumbers**(howManyNumbers-d-1) % howManyNumbers])

		# This adds the new list to our final list as long as it is not already present
		if individualList not in finalList:
			finalList.append(individualList)

		# yield "".join(str(numbers[n // howManyNumbers**(howManyNumbers-d-1) % howManyNumbers]) for d in range(howManyNumbers))
	return finalList
	'''


	
	''' 
	Attempt 3, this works but is slow

	# If numbers is empty then there are no permutations
	if len(numbers) == 0:
		pass

	# If there is only one element in numbers then, only one permuatation is possible
	# This is the base case
	elif len(numbers) == 1:
		return [numbers]

	# The list which will store the lists and be returned
	finalList = [] 


	# Iterate the input(numbers) and calculate the permutation
	# This is where the magic happens

	for num in range(len(numbers)):
		
		# This will extract the number from the numbers list at spot num
		internalNum = numbers[num]

		# Pull out the extracted number from the total list and set equal to remainingList  
		remainingList = numbers[:num] + numbers[num+1:]

		# smallList = [internalNum]

		for perm in listAllPermutations(remainingList):
			# smallList = smallList + listAllPermutations(remainingList)
			# smallList.append(listAllPermutations(remainingList))
			if([internalNum] + perm not in finalList):
				finalList.append([internalNum] + perm)

	return finalList
	'''

	# Multi-process the brute force method

	minNumberList = sorted(numbers)
	maxNumberList = sorted(numbers,reverse = True)
	# print (str(maxNumberList) + str(minNumberList))
	# maxNumber = 0
	maxNumber = int("".join(str(x) for x in maxNumberList))
	# print("Max num: " + str(maxNumber))
	minNumber = int("".join(str(x) for x in minNumberList))
	# print("Min num: " + str(minNumber))
	# minNumber =0
	# index = 0
	# while (index < len(numbers)):
	# 	maxNumber = maxNumber + (maxNumberList[index] * (10**index))
	# 	minNumber = minNumber + (minNumberList[index] * (10**index))
	# 	index = index + 1

	# print("Max number " + str(maxNumber) + " Min number " + str(minNumber))

	currentNumber = minNumber
	finalList = set()
	finalList.add(tuple(minNumberList))


	whileCount = 0
	maxCount = 1e9
	while (currentNumber <= maxNumber and whileCount < maxCount):
		whileCount += 1
		if (whileCount % 1000 == 0):
			print("+ 1000 while count listAllPermutations")
		# turns into a string and iterates over each digit and then puts each digit into a list
		digitsOfCurrentNum = [int(d) for d in str(currentNumber)]

		# Now I want to check if the list contains the appropriate digits exactly
		if (sorted(digitsOfCurrentNum) == minNumberList):
			if tuple(digitsOfCurrentNum) not in finalList:
				finalList.add(tuple(digitsOfCurrentNum))

		currentNumber = currentNumber + 1

	if (whileCount >= maxCount):
		print("You done goofed in while loop listAllPermutations")
		exit(-1)
	return finalList





# Test to make sure my functions work atm
def main():
	numberList = [1, 2, 4, 4, 5]
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
