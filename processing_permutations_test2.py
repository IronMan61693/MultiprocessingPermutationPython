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

	# numberMin = int("".join(str(x) for x in numberMinList))


	# If there are too many processes, reduce the number of processes to the number of input values
	processCount = min(processCount, len(numberMinList))

	# Calculate the index step size. Make sure the step is at least 1.
	remainder = len(numberMinList) % processCount
	step = max(1, len(numberMinList) // processCount)

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

		#self.count = Value('L')

		self.index = index

		#self.count.value = index

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

		currentNumberAsList = [int(d) for d in str(currentNumber)]

		print ("Min input number is: ", str(self.minNumber), " max input: ", str(self.maxNumber))


		# A check to ensure I do not enter an infinite while loop
		whileCount = 0
		maxCount = 1e6

		# This is the number of digits input and the -1 puts us at the last indexed spot
		length = len(currentNumberAsList) -1


		'''
		 This is almost working, I need it to always take the next smallest permutation, and if no permutation was
		 added I want to increment the currentnumber count by 1 until I find the next permutation, and then begin the 
		 swapping. This will take out the vast majority of the counting. It will also break up the permutations properly
		 It is currently swapping the input number, not one that is a permutation. This means first I need to find the lowest
		 permutation and once I do begin the swapping. It is also not doing the next smallest every time,
		 I need to check that it is correct 
		 i.e. 12345 -> 12354 -> 12435 -> 12453 ->12534 -> 12543 -> 13245 -> 13254 -> 13425 -> 13452 and so on.
		'''

		while (currentNumber <= self.maxNumber and whileCount < maxCount):
			# A sanity check that the code did not freeze for large permutation checks
			whileCount += 1
			if (whileCount % 100000 == 0):
				print("+", whileCount, " while count listAllPermutations")

						# Checks the digits of the current list against those of the original
			if (sorted(currentNumberAsList) == self.permutationNumberAsList):

				# If the digits are the same add them as a tuple to the set
				self.permSet.add(tuple(currentNumberAsList))


				# We will be working right to left
				ind = length
				
				# This finds the first time a singular number in the list is larger than the number to its left
				while (currentNumberAsList[ind - 1] >= currentNumberAsList[ind]):
					ind -= 1


					if (ind <= 0):
						break

				# This represents the start of the numbers we can replace with
				replace = ind

				# ind is now the number which will be switched
				ind -= 1


				if (replace < length):
					# This finds the smallest number to the right of the number which will be changed
					while ((currentNumberAsList[replace] >= currentNumberAsList[replace +1]) \
							and currentNumberAsList[replace +1] > currentNumberAsList[ind]):
						
						replace += 1

						if (replace >= length):
							break

				currentNumberAsList[ind], currentNumberAsList[replace] = currentNumberAsList[replace], currentNumberAsList[ind]

				currentNumberAsList[ind+1: ] = sorted(currentNumberAsList[ind+1: ])

				currentNumberString = ("".join(str(x) for x in currentNumberAsList))
				#print("Here is the STRING!!!!!!!!!!!!!!!!!!", currentNumberString)
				currentNumber = int(currentNumberString)

			else:
				currentNumber += 1
				currentNumberAsList = [int(d) for d in str(currentNumber)]


			

		# Exits if the while loop gets too large
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

		self.count = Value('L')

		self.count.value = index

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
			self.permSolutionArray[self.count.value] = int(intTup)
			self.count.value += 1
