#!/usr/bin/env python3

# Homework Assignment 3 
# Requirements: Given a function, and possible values for the variables
#  calculate the number of permutations, solve for all possible solutions,
#  run the above with multiprocessing
# Owner: Dominic Pontious
# This is for _test5 Attempts Pipe

from processing_permutations_test5 import *
from multiprocessing import cpu_count, Pipe
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
	 Creates a pipe, a list to track the processes processList,
	 a list of the permutations permList, and a set of the permutations permSet
	 starts a listOfPermutations process for each of the chunks, waits for them to finish
	 The child has sent each of their chunks of permutations as a tuple containing 
	 tuples extracts the tuples and adds them to the permSet which is then returned

	Input: 	dividedList [<int>]
			permutationNumberAsList [<int>]
			processCount <int>
	Output: permSet {(<int>)}
	"""


	# Initializes a pipe between child and parent processes
	parent_conn, child_conn = Pipe()


	# Initialize the process list permutations list and permutations set
	processList = []
	permSet = set()

	minPermutationAsList = sorted(permutationNumberAsList)

	# Length of the divided list will be the number of processes
	# Goes through each of the chunks in dividedList and starts a process for the chunk
	for number, valuesList in enumerate(dividedList):

		minNumber = valuesList[0]
		maxNumber = valuesList[1]

		# Defines the process
		process = listOfPermutations(minNumber, maxNumber, child_conn, minPermutationAsList)

		# Adds the new process to the processList
		processList.append(process)

		# Starts the process
		process.start()

		# Pulls each tuple out and adds it to the permSet
		for tupl in parent_conn.recv():
			permSet.add(tupl)

	# Waits for all of the processes to finish
	for process in processList:
		process.join()


	return permSet

def runSolutionsPermutations(dividedList):
	"""
	Given a list which has all possible permutations of some given number, 
	 see dividePermutationList(), establishes a pipe between the parent and
	 child process, a list to track the processes processList, 
	 and a set of the solutions to the equation permSolutionSet
	 waits for the process to finish and then takes the resulting set
	 created by the child processes to return as the solution set of tuples

	Input: 	dividedList [(<int>)]
	Output: permSolutionSet {(<int>)}
	"""
	# Sets a pipe between parent and child processes
	parent_conn, child_conn = Pipe()
	
	# Initialize the working lists and set
	processList = []
	# permSolutionList = []
	permSolutionSet = set()

	# Iterate through to give the processes their appropriate information, index and checkList
	# and start the process
	for number, checkList in enumerate(dividedList):
		
		# Defines the process
		process = solutionsWithPermutations(child_conn, checkList)

		# Adds the new process to the processList
		processList.append(process)

		# Starts the process
		process.start()

		# Pulls each tuple out and adds it to the solution Set
		for tupl in parent_conn.recv():
			permSolutionSet.add(tupl)


	# Wait for the processes to finish
	for process in processList:

		process.join()


	return permSolutionSet



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
	defaultNumberList = [1, 2, 3, 4, 5, 6, 7, 8, 9]


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

	# Prints the number of permutations found
	print("Number of permutations ", str(len(listOfPerms)))


	# End for stop time for how fast program ran
	stop = datetime.datetime.now()
	print(stop - start)


	#####################################################################################################
	# Calculate solutions to the equation
	#####################################################################################################

	# Chunk the permutations by the number of processes
	dividedPermList = dividePermutationList(list(listOfPerms), totalProcess)

	# Calculate all solutions for the equation in runSolutionsPermutations
	solutionOfPerms = runSolutionsPermutations(dividedPermList)

	# Print the number of solutions
	print(str(len(solutionOfPerms)) + " is the number of solutions given the input numbers: " + totalNumberString)





# This is a check to make sure the script is being handled correctly
if (__name__ == "__main__"):
	main()

else:
	print("Did not run main function multiprocessing_permutations")
