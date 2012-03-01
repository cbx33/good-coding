def function():
	special_numbers = []
	for number in number_list:
		print "Trying: ", number
		if number < 1000:
			if prime(number):
				special_numbers.append(number)
			elif even(number):
				special_numbers.append(number)
	print special_numbers
