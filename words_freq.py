#importing the libraries to be used
import threading
from collections import Counter
import string
import queue

#***************************************************************************
#**********************GENERAL PURPOSE FUNCTIONS****************************
#***************************************************************************

#Initializing a queue to store output from the threads
my_queue = queue.Queue()

#Function to store the output from the thread into a queue
def storeInQueue(f):
	def wrapper(*args):
		my_queue.put(f(*args))
	return wrapper

#Function to divide the input file into n chunks
def chunks(lista, n):
	for i in range(0, n):
		yield lista[i::n]

#Function to read the input file from the user
def read_file(in_file):
	f = open(in_file, 'r')
	data = f.read()
	list = data.splitlines()
	f.close()
	return list

#Function to count the words
@storeInQueue
def count_words(list, x):
	dict_temp = {}
	for item in list[x]:
		sentence = item.translate(str.maketrans('', '', string.punctuation))
		counts = Counter(sentence.split())
		dict_temp = Counter(dict_temp)
		dict_temp = dict_temp + counts
	return dict_temp

#Function to create n threads as required
def create_threads(file_chunks, thread):
	threads = []
	dict_temp = {}
	#creating threads
	for x in range(0, int(thread)):
		t = threading.Thread(target=count_words, args=(file_chunks, x,))
		threads.append(t)

	#Starting threads
	for t in threads:
		print('Started: %s' % t)
		t.start()
		thread_out = my_queue.get()
		dict_temp = Counter(dict_temp)
		dict_temp = dict_temp + thread_out
	return dict_temp

#Function to write output to file
def out_to_file(dict):
	with open("Output.txt", 'w') as f: 
		for key, value in dict.items(): 
			f.write('%s:%s\n' % (key, value))

#***************************************************************************
#****************************THE MAIN FUNCTION******************************
#***************************************************************************

def main():
	in_file = input("Enter the path of the text file you want to read:\n")
	file_data = read_file(in_file)
	thread = input("Enter the number of threads needed:\n")
	file_chunks = list(chunks(file_data, int(thread)))
	output_counter = create_threads(file_chunks, thread)
	output_dict = dict(output_counter)
	out_to_file(output_dict)
	print("The output of words and their frequecies has been saved into Output.txt file................!!!!")


#***************************************************************************
#****************************DRIVER CODE************************************
#***************************************************************************

if __name__ == '__main__':
	main()  # calling main function




