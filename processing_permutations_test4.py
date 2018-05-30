#!/usr/bin/env python3

# Homework Assignment 3 
# Requirements: Given a function, and possible values for the variables
#  calculate the number of permutations, solve for all possible solutions,
#  run the above with multiprocessing
# Owner: Dominic Pontious
# This uses Queue

# Makes use of process and value
from multiprocessing import Process

def divideNumberListPermutations(numberList, processCount):
	"""
	Given a numberList as a list which has an integer in each spot and the number of processes,
	 divide the input up into even (as even as possible) chunks.

	Input:  numberList [<int>]
			process count <int>
	Output: list of sub-lists [sub-list [<int>]]
	"""

	######################################################################################################
	# Find the extremes (smallest and largest) possible values
	######################################################################################################

	numberMinList = sorted(numberList)
	numberMaxList = sorted(numberList, reverse = True)

	numberMin = int("".join(str(x) for x in numberMinList))
	numberMax = int("".join(str(x) for x in numberMaxList))

	######################################################################################################
	# Break it up by the processes
	######################################################################################################

	# Calculate the index step size. Make sure the step is at least 1.
	inputRange = numberMax - numberMin
	step = max(1, inputRange // processCount)

	# If there are too many processes, reduce the number of processes to the number of input values
	processCount = min(processCount, inputRange)


	# A list of the minimum and maximum number to find permutations for from the input numbers
	outputList = []

	######################################################################################################
	# Break the numbers into even(ish) chunks
	######################################################################################################

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

	######################################################################################################
	# Break it up by how many processes
	######################################################################################################

	# Calculate the index step size. Make sure the step is at least 1.
	step = max(1, len(permutationList) // processCount)

	# If there are too many processes, reduce the number of processes to the number of input values
	processCount = min(processCount, len(permutationList))

	# A list containing lists of chunked permutation tuples
	outputList = []

	######################################################################################################
	# Divide the permutations into chunks for each process to work with
	######################################################################################################

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

	def __init__(self, minNumber, maxNumber, permListQueue, permutationNumberAsList):
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

		self.permListQueue = permListQueue

		self.permutationNumberAsList = permutationNumberAsList

		self.permNumbAsSet = set(permutationNumberAsList)

		self.comparePermutation = sorted("".join(str(n) for n in permutationNumberAsList))

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

		######################################################################################################
		# Initialize variables
		######################################################################################################

		# This is the starting number
		currentNumber = self.minNumber	
		currentNumberString = str(currentNumber)	


		# A check to ensure I do not enter an infinite while loop
		ifCount = 0
		maxCount = 1e9

		# This is the number of digits input and the -1 puts us at the last indexed spot
		length = len(self.permutationNumberAsList)


		######################################################################################################
		# Loop through the minimum input number to the maximum number 
		######################################################################################################

		for number in range(self.minNumber, self.maxNumber):
			# A sanity check that the code did not freeze for large permutation checks
			ifCount += 1

			if (ifCount % 500000 == 0):

				print("+", ifCount, " if count listAllPermutations")

			# Stops when the current number has checked every permutation in the appropriate range
			if (currentNumber > self.maxNumber):
				break


			# Checks the digits of the current list against those of the original
			if (sorted(currentNumberString) == self.comparePermutation):

				currentNumberAsList = [int(d) for d in str(currentNumber)]

				# If the digits are the same add them as a tuple to the set
				self.permSet.add(tuple(currentNumberAsList))

				if (currentNumber == self.maxNumber):
					break

				######################################################################################################
				# Find the next largest permutation numerically
				######################################################################################################

				# 
				# ind = length
				
				# 
				# # i.e. 13254 this will check 4 < 5 go to next index 5 > 2 stop at index 3

				# We will be working right to left
				switchNum = -1
				replaceNum = -1

				# This finds the first time a singular number in the list is larger than the number to its left
				for isSmaller in reversed(range(0,length)):

					if currentNumberAsList[isSmaller] < currentNumberAsList[switchNum]:
						switchNum = isSmaller
						break

					switchNum = isSmaller

				# This finds the smallest number to the right of the number which will be changed
				# In example we check if 4 < 5 and then if 4 > 2
				# since it is we move to the next spot in the list i.e. replace = index 4
				for replacement in reversed(range(switchNum,length)):

					if ((currentNumberAsList[replacement] > currentNumberAsList[switchNum])):
						replaceNum = replacement
						break


				# Here we swap the switchNum and the replace 
				# i.e. now we have 13452
				currentNumberAsList[switchNum], currentNumberAsList[replaceNum] = currentNumberAsList[replaceNum], currentNumberAsList[switchNum]

				# Here we sort everything past where the index swap occured
				# i.e. 13425
				currentNumberAsList[switchNum+1: ] = sorted(currentNumberAsList[switchNum+1: ])

				# Here we turn the list into an int to run again
				currentNumber = int("".join(str(x) for x in currentNumberAsList))

			# This means the current number is not a permutation so we will increment by 1 we can then check it against a set
			# if the digits are not the same we can increment by 1 again and run the whole for loop.
			# This speeds the code up a bit by doing two checks at once
			else:
				currentNumber += 1
				currentNumberString = str(currentNumber)
				currentSet = set(currentNumberString)
				if (currentSet is not self.permNumbAsSet):
					currentNumber += 1
					currentNumberString = str(currentNumber)




			

		# Exits if the while loop gets too large
		if (ifCount >= maxCount):
			print("You done goofed in while listOfPermutations")
			exit(-1)

		# Adds each of the tuples as an integer to the permListArray
		for tup in self.permSet:

			# # Converts tuple into a string with the integers all next to one another
			# intTup = ''.join(str(i) for i in tup)

			# Converts string into integer to index into the shared array
			self.permListQueue.put(tup)


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
		__init__(self, index, permSolutionArray, permListAsTuples): Initializes the process turns the list into a set 
		run(self) For every element in the set of tuples compares it against the equations, and if it is not
		 already a solution adds it to the set.
		 Adds each of the tuples in the set to the permSolutionArray, which is shared between the processes, sequentially
	"""
	def __init__(self, permSolutionQueue, permListAsTuples):
		Process.__init__(self)

		self.permSolutionQueue = permSolutionQueue

		self.permSetOfTuples = set(permListAsTuples)

		self.solutionSet = set()

	def run(self):

		for number in self.permSetOfTuples:

			'''
				equation 1 5 input   (number[0] + 2 * number[1] / number[2] + number[3] + 12 * number[4] == 43)

				equation 2 9 input order of ops
				(number[0] + 13 * number[1] / number[2] + number[3] + 12 * number[4] - number[5] - 11 + number[6] * number[7]\
		 		 / number[8] - 10 == 66)

		 		equation 3 9 input no order of ops
		 		 (((((((((((((number[0] + 13) * number[1]) / number[2]) + number[3]) + 12) * number[4]) - number[5]) - 11) + number[6]) * number[7])\
		 		 / number[8]) - 10) == 66)

			'''

			if ((number[0] + 2 * number[1] / number[2] + number[3] + 12 * number[4] == 43) and (number not in self.solutionSet)):	
				self.solutionSet.add(number)

		# Adds each of the tuples as an integer to the permSolutionArray
		for tup in self.solutionSet:

			# # Converts tuple into a string with the integers all next to one another
			# intTup = ''.join(str(i) for i in tup)

			# Converts string into integer to index into the shared array
			self.permSolutionQueue.put(tup)
