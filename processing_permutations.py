#!/usr/bin/env python3

# Homework Assignment 3 
# Requirements: Given a function, and possible values for the variables
#  calculate the number of permutations, solve for all possible solutions,
#  run the above with multiprocessing
# Owner: Dominic Pontious

# Makes use of process and value
from multiprocessing import Process, Value

def divideNumberListPermutations(numberList, processCount):
	"""
	Given a minimum number, maximum number and the number of processes, divide the
	 input up into even (as even as possible) chunks.

	Input:  numberMin <int>
			numberMax <int>
			process count <int>
	Output: list of sub-lists [sub-list [<int>]]
	"""
	numberMinList = sorted(numberList)
	numberMaxList = sorted(numberList, reverse = True)

	numberMin = int("".join(str(x) for x in numberMinList))
	numberMax = int("".join(str(x) for x in numberMaxList))

	# Calculate the index step size. Make sure the step is at least 1.
	inputRange = numberMax - numberMin
	step = max(1, inputRange // processCount)

	# If there are too many processes, reduce the number of processes to the number of input values
	processCount = min(processCount, inputRange)

	# A list of the minimum and maximum number to find permutations for from the input numbers
	outputList = []

	# Go through each process number
	for number in range(processCount):
		# This holds the respective minimum(first index) and maximum(last index) numbers for each chunk
		listMinMax = []

		# Calculate the "first" index for this process
		fIndex = number * step + numberMin
		
		# Calculate the last index. If it's the last process, set the last index to the length of the input list.
		if (number < processCount - 1):
			lIndex = (number + 1) * step + numberMin

		else:
			lIndex = numberMax

		# This maxes the 0 element the minimum number checked by the process and
		# the 1 element the max number
		listMinMax.append(fIndex)
		listMinMax.append(lIndex)

		# Append the chunk to the output list
		outputList.append(listMinMax)

	return outputList

def dividePermutationList(permutationList, processCount):
	"""
	Given a list of permutations as tuples and a number of processes, divide the 
	 permutation list into even (as even as possible) chunks of sub-lists in one list

	Input: 	permutationList [(<int>)] <- list of tuples of integers
			processCount <int>
	Output: list of sub-lists [sub-list [<int>]]
	"""
	# Calculate the index step size. Make sure the step is at least 1.
	step = max(1, len(permutationList) // processCount)

	# If there are too many processes, reduce the number of processes to the number of input values
	processCount = min(processCount, len(permutationList))

	# A list containing lists of chunked permutation tuples
	outputList = []

	# For each process segments the chunks of the permutations list
	for number in range(processCount):

		# This is the starting index for the respective process
		fIndex = number * step

		# If it is not the last process set the last index to start of the next process point
		if (number < processCount -1):
			lIndex = (number + 1) * step

		# If it is the last process set the last index to the end of the list
		else:
			lIndex = len(permutationList)

		# Append the sub-list to the list
		outputList.append(permutationList[fIndex:lIndex])

	return outputList


class listOfPermutations(Process):
	"""
	Variables:
		minNumber <int>
		maxNumber <int>
		permListArray [<int>] <- shared Array between processes
		count <int>
		index <int>
		count.value <int>
		permutationNumberAsList [<int>]
		permSet {(<int>)} <-set not dict
	Methods:
		__init__(self,index,minNumber,maxNumber,permListArray,permutationNumberAsList) Initializes the process
		run(self) Adds the original tuple to the permSet, increments by one for every number in the range, from
		 minimum to maximum, compares the digits of the current number with the permutation number, 
		 if they are the same adds them to the set
		 Adds each of the tuples in the set to the permListArray, which is shared between the processes, sequentially
	"""

	def __init__(self, index, minNumber, maxNumber, permListArray, permutationNumberAsList):
		"""
		Initializes the process, calls the Process class __init__ and then sets each of the variables equal to their
		 respective inputs

		Input: 	index <int>
				minNumber <int>
				maxNumber <int>
				permListArray [<int>] <- shared Array between processes
				permutationNumberAsList [<int>]
		Output: None
		"""
		Process.__init__(self)

		self.minNumber = minNumber

		self.maxNumber = maxNumber

		self.index = index

		self.count = index

		self.permListArray = permListArray

		self.permutationNumberAsList = permutationNumberAsList

		self.permSet = set()

	def run(self):
		"""
		Adds the original tuple to the permSet, increments by one for every number in the range, from
		 minimum to maximum, compares the digits of the current number with the permutation number, 
		 if they are the same adds them to the set
		 Adds each of the tuples in the set to the permListArray, which is shared between the processes, sequentially
		Input: None
		Output: None
		"""
		# This is the starting number
		currentNumber = self.minNumber

		# Adds the base permutation as a tuple to the set
		self.permSet.add(tuple(self.permutationNumberAsList))

		# A check to ensure I do not enter an infinite while loop
		whileCount = 0
		maxCount = 1e9

		# Loop through every number from the minimum to the maximum
		while (currentNumber <= self.maxNumber and whileCount < maxCount):
			# A sanity check that the code did not freeze for large permutation checks
			whileCount += 1
			if (whileCount % 100000 == 0):
				print("+", whileCount, " while count listAllPermutations")

			# Turns the current integer number into a list of single numbers
			digitsOfCurrentNum = [int(d) for d in str(currentNumber)]

			# Checks the digits of the current list against those of the original
			if (sorted(digitsOfCurrentNum) == self.permutationNumberAsList):

				# If the digits are the same add them as a tuple to the set
				self.permSet.add(tuple(digitsOfCurrentNum))

			currentNumber += 1

		# Exits if the while loop gets too large and print a statement to know
		if (whileCount >= maxCount):
			print("You done goofed in while listOfPermutations")
			exit(-1)

		# Adds each of the tuples as an integer to the permListArray
		for tup in self.permSet:

			# Converts tuple into a string with the integers all next to one another
			intTup = ''.join(str(i) for i in tup)

			# Converts string into integer to index into the shared array
			self.permListArray[self.index] = int(intTup)
			self.index += 1


class solutionsWithPermutations(Process):
	"""
	Variables:
		index <int>
		permSolutionArray [<int>] <- shared Array between processes
		permListAsTuples [(<int>)] 
		permSetOfTuples {(<int>)}
		count <int> 4 bit
		count.value <int>
		solutionSet {(<int>)}
	Methods:
		__init__(sself, index, permSolutionArray, permListAsTuples): Initializes the process turns the list into a set 
		run(self) For every element in the set of tuples compares it against the equations, and if it is not
		 already a solution adds it to the set.
		 Adds each of the tuples in the set to the permSolutionArray, which is shared between the processes, sequentially
	"""
	def __init__(self, index, permSolutionArray, permListAsTuples):
		Process.__init__(self)

		self.index = index

		self.permSolutionArray = permSolutionArray

		self.permSetOfTuples = set(permListAsTuples)

		self.solutionSet = set()

	def run(self):

		for number in self.permSetOfTuples:

			# (number[0] + 13 * number[1] / number[2] + number[3] + 12 * number[4] - number[5] - 11 + number[6] * number[7]\
		 	#	 / number[8] - 10 == 66)
			if (number[0] + 2 * number[1] / number[2] + number[3] + 12 * number[4] == 43 and (number not in self.solutionSet)):	
				self.solutionSet.add(number)

		# Adds each of the tuples as an integer to the permSolutionArray
		for tup in self.solutionSet:

			# Converts tuple into a string with the integers all next to one another
			intTup = ''.join(str(i) for i in tup)

			# Converts string into integer to index into the shared array
			self.permSolutionArray[self.index] = int(intTup)
			self.index += 1
