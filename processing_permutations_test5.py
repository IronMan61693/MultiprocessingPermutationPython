#!/usr/bin/env python3

# Homework Assignment 3 
# Requirements: Given a function, and possible values for the variables
#  calculate the number of permutations, solve for all possible solutions,
#  run the above with multiprocessing
# Owner: Dominic Pontious
# This uses Pipe

# Makes use of process and pipe
from multiprocessing import Process, Pipe


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

	# Ensures there is at least 1 process
	processCount = max(1, processCount)

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

	# Ensures there is at least 1 process
	processCount = max(1, processCount)

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

	def __init__(self, minNumber, maxNumber, permConn, permutationNumberAsList):
		"""
		Initializes the process, calls the Process class __init__ and then sets each of the variables equal to their
		 respective inputs

		Input: 	minNumber <int>
				maxNumber <int>
				permConn <Object> <- The sending end of a Pipe object
				permutationNumberAsList [<int>]
				comparePermutation <str>
				permSet {(int)} <- set of tuples of ints
		Output: None
		"""
		Process.__init__(self)

		self.minNumber = minNumber

		self.maxNumber = maxNumber

		self.permConn = permConn

		self.permutationNumberAsList = permutationNumberAsList

		self.comparePermutation = sorted("".join(str(n) for n in permutationNumberAsList))

		self.permSet = set()


	def run(self):
		"""
		Increments by one for every number in the range, from minimum to maximum,
		 compares the digits of the current number with the permutation number, 
		 if they are the same adds them to the set
		 Once a permutation is found, finds the next largest permutation
		 Adds each of the tuples in the set to a tuple to pipe to the parent process
		Input: None
		Output: None
		"""

		######################################################################################################
		# Initialize variables
		######################################################################################################

		# This is the starting number
		currentNumber = self.minNumber	
		currentNumberString = str(currentNumber)	


		# A check to ensure I do not enter an infinite loop
		ifCount = 0
		maxCount = 1e9

		# This is the number of digits input 
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

				# Ensures the final permutation is added to the set
				if (currentNumber == self.maxNumber):
					break

				######################################################################################################
				# Find the next largest permutation numerically
				######################################################################################################

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
				for replacement in reversed(range(switchNum,length)):

					if ((currentNumberAsList[replacement] > currentNumberAsList[switchNum])):
						replaceNum = replacement
						break


				# Here we swap the switchNum and the replace 
				currentNumberAsList[switchNum], currentNumberAsList[replaceNum] = \
				currentNumberAsList[replaceNum], currentNumberAsList[switchNum]

				# Here we sort everything past where the swap occured
				currentNumberAsList[switchNum+1: ] = sorted(currentNumberAsList[switchNum+1: ])

				# Here we turn the list into an int to run again
				currentNumber = int("".join(str(x) for x in currentNumberAsList))

			######################################################################################################
			# A permutation was not found, check the next 8 numbers 
			######################################################################################################

			# This means the current number is not a permutation so we will increment by 1 we can then check it against the original
			# This speeds the code up because if a number is not a permutation there will be at most one permutation in the next 8 numbers
			else:
				currentNumber += 1
				numberPlus1 = currentNumber +1
				numberPlus2 = currentNumber +2
				numberPlus3 = currentNumber +3
				numberPlus4 = currentNumber +4
				numberPlus5 = currentNumber +5
				numberPlus6 = currentNumber +6
				numberPlus7 = currentNumber +7
				currentNumberString = str(currentNumber)
				currentSet = set(currentNumberString)
				if (sorted(currentNumberString) == self.comparePermutation):
					pass

				elif (sorted(str(numberPlus1)) == self.comparePermutation):
					currentNumber = numberPlus1
					currentNumberString = str(currentNumber)

				elif (sorted(str(numberPlus2)) == self.comparePermutation):
					currentNumber = numberPlus2
					currentNumberString = str(currentNumber)

				elif (sorted(str(numberPlus3)) == self.comparePermutation):
					currentNumber = numberPlus3
					currentNumberString = str(currentNumber)

				elif (sorted(str(numberPlus4)) == self.comparePermutation):
					currentNumber = numberPlus4
					currentNumberString = str(currentNumber)

				elif (sorted(str(numberPlus5)) == self.comparePermutation):
					currentNumber = numberPlus5
					currentNumberString = str(currentNumber)

				elif (sorted(str(numberPlus6)) == self.comparePermutation):
					currentNumber = numberPlus6
					currentNumberString = str(currentNumber)

				else:
					currentNumber = numberPlus7
					currentNumberString = str(currentNumber)




			

			# Exits if the while loop gets too large
			if (ifCount >= maxCount):
				print("You done goofed in while listOfPermutations")
				exit(-1)

		# Pipe the permutations as a tuple to the parent process
		self.permConn.send(tuple(self.permSet))




class solutionsWithPermutations(Process):
	"""
	Variables:
		permSolutionConn <Object> <- The sending end of a Pipe object
		permListAsTuples [(<int>)] 
		permSetOfTuples {(<int>)}
		equationChoice <str>
		solutionList [(<int>)]
	Methods:
		__init__(self, index, permSolutionArray, permListAsTuples): Initializes the process turns the list into a set 
		exception_filert(self,fun,iter): Exception handler for the lambda functions
		run(self) For every element in the set of tuples compares it against the equations, and if it is not
		 already a solution adds it to the set.
		 Pipes each of the tuples in the set to the parent process
	"""
	def __init__(self, permSolutionConn, permListAsTuples, equationChoice):
		"""
		Initializes the process turns the list into a set 
		Input: None
		Output: None
		"""
		Process.__init__(self)

		self.permSolutionConn = permSolutionConn

		self.permSetOfTuples = set(permListAsTuples)

		self.equationChoice = equationChoice

		self.solutionList = []

	def exception_filter(self, func, iter):
		"""
		Exception handler for my lambda functions, specifically if the function called did not receive enough 
		 input values, i.e. an index error
		Input:	func <lambda func>
				iter {(<int>)}
		Output:	result [(int)]
		"""
		result = []
		for i in iter:
			try:
				if func(i):
					result.append(i)

			except IndexError:
				# Did not input enough digits for the requested equation
				SystemExit(-1)
				break

		return result



	def run(self):
		"""
		For every element in the set of tuples compares it against the equations, and if it is not
		 already a solution adds it to the set.
		 Pipes each of the tuples in the set to the parent process
		Input: None
		Output: None
		"""

		# A set of tuples is passed in and we filter the permSetOfTuples which is passed in by
		# the equation and solutionList becomes the resulting tuples after the filter

		if(self.equationChoice == "FiveDigitEquation"):
			self.solutionList = self.exception_filter(lambda x: x[0] + 2 * x[1] / x[2] + x[3] + 12 * x[4] == 43, self.permSetOfTuples)

		elif(self.equationChoice == "VietNoOrderOps"):
			self.solutionList = self.exception_filter(lambda x: ((((((((((((x[0] + 13) * x[1]) / x[2]) + x[3]) + 12) * x[4]) - x[5]) - 11) + x[6]) * x[7])\
	 		 / x[8]) - 10) == 66, self.permSetOfTuples)

		elif(self.equationChoice == "TenDIGITS"):
			self.solutionList = self.exception_filter(lambda x: x[0] + 13 * x[1] / x[2] + x[3] + 12 * x[4] - x[5] - 11 + x[6] * x[7]\
				/ x[8] - 10 + x[9] == 75, self.permSetOfTuples)

		else:
			self.solutionList = self.exception_filter(lambda x: x[0] + 13 * x[1] / x[2] + x[3] + 12 * x[4] - x[5] - 11 + x[6] * x[7]\
			/ x[8] - 10 == 66, self.permSetOfTuples)


			
		# Using the Pipe to send the solutions as a tuple
		self.permSolutionConn.send(tuple(self.solutionList))
