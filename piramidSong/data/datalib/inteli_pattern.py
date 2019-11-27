#! /usr/bin/python3 -s

SIMPLEX_AUTOINT = "mode 0"

class simplex_num_url():
	"""
		Patter with form :
		<some url>xxxxxxxxxx<some extension>
		where, "xxxxxxxxxx" is an incremental number
		(the step value can be define)
		default step = 1
	"""
	def __init__(self, main_url, pattern, extension, step= 1, dynamic_number_length = False):
		super(simplex_num_url, self).__init__()

		self.base_url = pattern
		self.extension_type = "." + extension

		
		self.dynamic_number_length = dynamic_number_length

		self._set_number_pattern(main_url)
		self.step = step

		self.current_value = self.start_value

	def _set_number_pattern(self, main_url):
		self.number_pattern = main_url.split(self.base_url)[1][:-4]
		self.start_value = int(self.number_pattern)


	def update(self, main_url, pattern, extension, step= 1, dynamic_number_length = False):
		self.base_url = pattern
		self.extension_type = "." + extension

		
		self.dynamic_number_length = dynamic_number_length

		self._set_number_pattern(main_url)
		self.step = step

		self.current_value = start_value

	def _int_str_url(self, number=None):
		if number is None:
			number = self.current_value
		else:
			pass

		if not self.dynamic_number_length:
			expected_length = len(self.number_pattern)
			output = "0" * expected_length

			str_number = str(number)

			try:
				output = output[:-len(str_number)] + str_number
			except:
				print("Number Value bigger than the pattern'd number expected length")
				print("Try updating the example url and pattern \" .update(sample url, pattern)\"")

				return None
			else:
				return str_number
		else:
			return str(number)

	def get_url(self, number=None):
		if number is None:
			number = self.current_value
		else:
			pass
	
		out_str = self.base_url + self._int_str_url(number) + self.extension_type
		return out_str

	def beging(self, start_value):
		self.start_value = start_value
		self.current_value = self.start_value

	def next(self):
		self.current_value += 1
		return self.get_url()

	def previus(self):
		self.current_value += 1
		return self.get_url()

	def n_next(self, step):
		self.current_value += 1
		return self.get_url()
	def n_previus(self, step):
		self.current_value += 1
		return self.get_url()

	def restart(self):
		self.current_value = self.start_value

	def range_vstr(self, range_length, start_value=None, step=None):
		if start_value is None:
			start_value = self.start_value
		else:
			pass
		if step is None:
			step = self.step
		else:
			pass

		for num_val in range(start_value, start_value + range_length, step):
			yield(self.get_url(num_val))

	def range_auto(self, iterations, incremental=1):
		relative_val = self.start_value
		for _ in range(iterations):
			yield(self.get_url(relative_val))
			relative_val += incremental

def detection():
	pass



		