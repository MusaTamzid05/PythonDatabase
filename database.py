
'''
Author : Musa Khan
Date : 25/8/2016
'''

from str_to_list_converter import Str_List_Converter




import sqlite3


def raise_error_if_not_dict(dict_row):

	if type(dict_row) != dict:
		raise TypeError("Data type must be a dict")

def get_keys_values(dict_row):

	'''
	function to return key and values from dict


	'''

	raise_error_if_not_dict(dict_row)
	keys,values=[],[]

	for key,value in dict_row.items():
		keys.append(key)
		values.append(value)

	return keys,values







class Table:

	def __init__(self,table_name,table_structure,database_name='test.db'):

		self.table_name = table_name
		self.data_names,self.datatypes=get_keys_values(table_structure)
		self.database_name = database_name


		self.connect()
		

		

		
		self.cursor.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name = ?",(self.table_name,))

		table_exists = self.cursor.fetchone()

		if table_exists == None:

			'''
			if the table already does not exists , it creates the table with the given staructure
			'''

			

			
		

			query="CREATE TABLE {} ".format(self.table_name)
		

			temp=''

			for dataname,datatype in zip(self.data_names,self.datatypes):
				temp+=(dataname+" "+datatype+",")
				

			temp="(" + temp.strip(',') + ")"
			
			query += temp

			

			

			
			print("Creating table {}".format(self.table_name))
			self.cursor.execute(query)
			print("table created")

		self.close()

	def connect(self):

		self.db =sqlite3.connect(self.database_name)
		self.db.row_factory = sqlite3.Row # this makes sures the cursor returns row objects instance tuple
		self.cursor = self.db.cursor()


		

	def close(self):

		self.db.close()
		


	def insert(self,row_dict):

		

		keys,values=get_keys_values(row_dict)

		query = "INSERT INTO {}".format(self.table_name) + "("

		converter = Str_List_Converter()

		string = converter.list_to_string(word_list = keys,concate_with=',')

		query+= string+ ")"

		string = ''

		for index in range(len(keys)):
			string += '?,'

		string=string.strip(',')

		query  += " VALUES (" + string +")"

		insert_values=tuple(values)

		self.connect()
		self.cursor.execute(query,insert_values)
		self.db.commit()
		self.close()


	def drop_table(self):

		self.db.execute("drop table if exists {}".format(self.table_name,))

	def delete_row(self,row_dict):

		

		if self.data_exists(row_dict) == False:
			print("No data name {} exists in the database to delete")
			return
			


		keys , values = get_keys_values(row_dict)

		query = "DELETE FROM {} ".format(self.table_name) + " WHERE "



		query += self._make_spesific_data_query(keys,concatinate_with='and')

		

		


		values = tuple(values)

		self.connect()
		self.db.execute(query,values)
		self.db.commit()
		self.close()
		



		

	def select_where(self,row_dict):

		self.connect()

		'''

		return a list of match results.

		'''

		keys , values = get_keys_values(row_dict)

		query = "SELECT * FROM {}".format(self.table_name)+" WHERE "
		query += self._make_spesific_data_query(keys,concatinate_with='and')

		

		

		values = tuple(values)

		self.cursor.execute(query,values)

		results = self.cursor.fetchall()

		match_results = []


		if results:
		
			for result in results:
				match_results.append(dict(result))

		self.close()


		return match_results


	def update(self,olddata_dict,newdata_dict):

		if self.data_exists((olddata_dict)) == False:
			return

		


		new_keys,new_values = get_keys_values(newdata_dict)

		query = "UPDATE {}".format(self.table_name) + " SET "

		query += self._make_spesific_data_query(new_keys)

		query += " WHERE "

		old_keys,old_values = get_keys_values(olddata_dict)


		query += self._make_spesific_data_query(old_keys,concatinate_with ='and')

		values=new_values  + old_values
		values = tuple(values)




		
       
		self.connect()
		self.db.execute(query,values)
		self.db.commit()

		self.close()





	def get_all_rows(self):

		self.connect()

		'''

		Return a list of dict objects where  each dict represents a row

		'''

		rows = []
		
		temp_rows=self.db.execute("SELECT * FROM {}".format(self.table_name))

		

		if temp_rows:
			
			for row in temp_rows:

				rows.append(dict(row))

		self.close()
		

		return rows

	def _make_spesific_data_query(self,keys,concatinate_with=','):


		string = ""
	

		for key in keys:

			string += " {} =? {}".format(key,concatinate_with)

		return string.strip(concatinate_with)

		
	def show_rows_of(self,list_dict):

		if len(list_dict):
			for data in list_dict:
				print(data)

		else:
			print("No rows where returned!!")


	def data_exists(self,row_dict):

		return True if len(self.select_where(row_dict)) else False

	def select_by_id(self,id_):

		'''
		In SQLite , data id increments automaticly and
		it is save in ROWID.
		Note that if ROWID id is not specified then
		it is giveb automaticly by SQLite.

		'''

		if type(id_) != int:
			raise TypeError("Id must be a int")

		row_dict={"ROWID" :id_}

		row = self.select_where(row_dict)

		if len(row) == 0:
			print("No data with id {}".format(id_))

		if len(row) > 1:
			print("More one data with {} was found.".fomat(id_))

		return row[0]












		



		

			

		

if __name__ == "__main__":

	table_structure={"name":"text","id":"int"}



	

	db = Table("test",table_structure=table_structure)

	

	
	
	h1 = {"name" : "Superman", "id" : 1}
	h2 = {"name" : "Spiderman", "id" : 2}
	h3 = {"name": "Batman","id":3}

	h4={"name" : "Iron Man" , "id": 4}



	

	

	db.insert(h1)
	db.insert(h2)
	db.insert(h3)

	print("Selecting data with id 1")

	row=db.select_by_id(1) 
	print(row)





	rows = db.get_all_rows()
	print("1.After inserting ..")
	db.show_rows_of(rows)

	
	
	print("2.After deleting {}".format(h2['name']))
	db.delete_row(h2)
	rows = db.get_all_rows()
	db.show_rows_of(rows)



	print("3.After updating {} to {}".format(h1['name'],h2['name']))
	db.update(h1,h4)
	rows = db.get_all_rows()
	db.show_rows_of(rows)

	print("4.After getting Batman")
	rows = db.select_where(h3)

	db.show_rows_of(rows)

