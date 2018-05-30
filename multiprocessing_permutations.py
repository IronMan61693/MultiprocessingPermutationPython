#!/usr/bin/env python3

# Homework Assignment 3 
# Requirements: Given a function, and possible values for the variables
#  calculate the number of permutations, solve for all possible solutions,
#  run the above with multiprocessing
# Owner: Dominic Pontious

from processing_permutations_test3 import *
from multiprocessing import cpu_count, Array
import itertools
import argparse
import datetime
import math

def possiblePermutations(permutationNumberAsList):
	"""
	Given a number as a list calculate the total possible permutations
	Input:	permutationNumberAsList [<int>]
	Output: possiblePermutations <int>
	"""
	# Create a dictionary from the list with the key as the integer and the value as the times that number appears in the list
	numberDict = {}

	for number in permutationNumberAsList:

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
		if (numberDict[duplicate] > 1):
			factorialNumber = math.factorial(numberDict[duplicate])
			duplicateNumbers = duplicateNumbers * factorialNumber

	# Gives me the total number of possible permutations
	numberPermutations = (math.factorial(len(permutationNumberAsList)) // duplicateNumbers)


	return numberPermutations



def runListPermutations(dividedList, permutationNumberAsList, processCount):
	"""
	Given a list which has as its 0 elements the minimum number for each chunk
	 and the 1 elements the maximum number for each chunk, see divideNumberListPermutations()
	 and the number which is being permuted as a list
	 Creates a shared array permListArray, a list to track the processes processList,
	 a list of the permutations permList, and a set of the permutations permSet
	 starts a listOfPermutations process for each of the chunks, waits for them to finish
	 The array has the permutations as integers in each index spot, so takes each of these 
	 integers and converts them to a tuple checks it has not been added and then adds them

	Input: 	dividedList [<int>]
			permutationNumberAsList [<int>]
			processCount <int>
	Output: permList [<int>]
	"""

	# The maximum length of the array would be every permutation
	# added 15 as a catch for each process if for some reason it went farther
	sizeOfArray = possiblePermutations(permutationNumberAsList) + (100*processCount)

	# Starts our Array at the first spot
	index = 0

	# Initializes the array for 2 bit int and with size of sizeOfArray
	permListArray = Array('I', sizeOfArray)


	# Initialize the process list permutations list and permutations set
	processList = []
	permList = []
	permSet = set()
	step = ((possiblePermutations(permutationNumberAsList) + (100*processCount)) // processCount)

	minPermutationAsList = sorted(permutationNumberAsList)

	# Length of the divided list will be the number of processes
	# Goes through each of the chunks in dividedList and starts a process for the chunk
	for number, valuesList in enumerate(dividedList):

		minNumber = valuesList[0]
		maxNumber = valuesList[1]


		process = listOfPermutations(index, minNumber, maxNumber, permListArray, minPermutationAsList)

		processList.append(process)
		process.start()

		#print("Process ", number, " started")

		index += step

	# Waits for all of the processes to finish
	for process in processList:
		process.join()

	# Takes the results from the Array and makes them into a list of tuples
	for permutation in permListArray:

		if permutation != 0:

			permTuple = tuple(int(d) for d in str(permutation))

			if permTuple not in permSet:

				permSet.add(permTuple)
				permList.append(permTuple)

	return permList

def runSolutionsPermutations(dividedList):
	"""
	Given a list which has all possible permutations of some given number, 
	 see dividePermutationList(), creates an array which is shared between the 
	 processes, a list to track the processes processList, 
	 a list of the solutions to the equation permSolutionList, and 
	 a set of the solutions permSolutionSet
	 starts a process saving to the correct part in the array, given by index,
	 and a list that it is checking if it has solutions checkList,
	 waits for the process to finish and then takes the resulting array and 
	 turns the solutions into tuples in a list called permSolutionList

	Input: 	dividedList [(<int>)]
	Output: permSolutionList [<int>]
	"""
	# Creates the array of the size of all of the permutations laid out sequentially
	permSolutionArray = Array('I', len(list(itertools.chain(*dividedList))), lock = False)
	
	# Initialize the working lists and set
	processList = []
	permSolutionList = []
	permSolutionSet = set()

	index = 0

	# Iterate through to give the processes their appropriate information, index and checkList
	# and start the process
	for number, checkList in enumerate(dividedList):
		
		process = solutionsWithPermutations(index, permSolutionArray, checkList)

		processList.append(process)
		process.start()

		print("Process in solutions ", number, " started")

		index += len(checkList)

	# Wait for the processes to finish
	for process in processList:

		process.join()

	# Takes the results from the Array and makes them into a list of tuples
	for permSolution in permSolutionArray:

		if permSolution != 0:

			permSolTuple = tuple(int(d) for d in str(permSolution))

			if permSolTuple not in permSolutionSet:

				permSolutionSet.add(permSolTuple)
				permSolutionList.append(permSolTuple)

	return permSolutionList



def main():
	"""
	Uses datetime to check how quickly the code is being run for optimization.
	 Sets the default values
	 Calls the divideNumberListPermutations function
	 Calls runListPermutations function
	 prints all of the permutations
	 Calls dividePermutationList
	 Calls runSolutionsPermutations
	 prints the solutions
	"""
	description = "This script finds all solutions with permutations to an equation given a list of numbers"
	# Start for start time for program speed check
	start = datetime.datetime.now()

	# Create a command line argument parser
	parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)

	# Default max number of process to use
	defaultProcessCount = cpu_count()

	# Default numbers and numberLists
	defaultNumberList = [1, 2, 3, 4, 5]


	######################################################################################################
	# Command line interactions
	######################################################################################################

	# Add arguments to the parser
	parser.add_argument("-n", "--numbers", help="path to input numbers to check for solutions", default=defaultNumberList)
	parser.add_argument("-p", "--process", help="path to input process count", default=defaultProcessCount)

	# Parse the command line arguments
	args = parser.parse_args()

	# Read in the desired number of processes
	totalProcess = int(args.process)

	# Turn the input into a single int
	totalNumberString = ("".join(str(x) for x in args.numbers))

	# Turns the current integer number into a list of single numbers
	totalNumberList = [int(d) for d in str(totalNumberString)]


	######################################################################################################
	# Calculate all permutations
	######################################################################################################

	# Chunk the numbers for permuting by the number of processes
	dividedNumbers = divideNumberListPermutations(totalNumberList, totalProcess)

	# Calculate all permutations using multiple processes
	listOfPerms = runListPermutations(dividedNumbers, totalNumberList, totalProcess)


	print(str(len(listOfPerms)))


	# End for stop time for how fast program ran
	stop = datetime.datetime.now()
	print(stop - start)


	#####################################################################################################
	# Calculate solutions to the equation
	#####################################################################################################

	# Chunk the permutations by the number of processes
	dividedPermList = dividePermutationList(listOfPerms, totalProcess)

	# Calculate all solutions for the equation in runSolutionsPermutations
	solutionOfPerms = runSolutionsPermutations(dividedPermList)

	# Print the number of solutions
	print(str(len(solutionOfPerms)) + " is the number of solutions given the input numbers: " + totalNumberString)





# This is a check to make sure the script is being handled correctly
if (__name__ == "__main__"):
	main()

else:
	print("Did not run main function multiprocessing_permutations")
