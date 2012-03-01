<<<ref#1>>>def prime(number):
	for test in range(number/2+1)[2:]:
		if number%test == 0:
			return 0
	return 1

<<<ref#2>>>def even(number):
	if number%2 == 0:
		return 1
	else:
		return 0

number_list = range(1,50000)

def function():
	special_numbers = []
	for number in number_list:
		print "Trying: ", number
		if prime(number):
			if number < 1000:
				special_numbers.append(number)
		elif even(number):
			if number < 1000:
				special_numbers.append(number)
	print special_numbers
function()
