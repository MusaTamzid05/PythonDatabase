
class Str_List_Converter:

	def __init__(self):pass


	def get_remove_list(self,remove_word,string):

		words = string.split()

		try:
			words.remove(remove_word)

		except ValueError as e:
			print(e)


		return words

	def get_all_words_starting_from(self,starting_word,string):

	
		
		words = string.split()
		word_index =words.index(starting_word)
		words = [word for index,word in enumerate(words) if index >  word_index]

		return words

	def list_to_string(self,word_list,concate_with=' '):

		string=''

		

		for word in word_list:
			string+= word + concate_with

		return string.strip(concate_with)
		






if __name__ == "__main__":

	converter = Str_List_Converter()
	data=converter.get_remove_list("my","this is my name",)
	print(data)
	data=converter.get_all_words_starting_from("define","Would you please define Sky ?")
	print(data)

	print(converter.list_to_string(data))
