
'''
Author : Musa Khan (Original starting date)
Date : 25/8/2016 
'''

try:
    from simple_database.str_to_list_converter import Str_List_Converter
except ImportError:
    from str_to_list_converter import Str_List_Converter

import sqlite3

class Database:
    def __init__(self, path):
        self.path = path

    def connect(self):
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row # this makes sures the cursor returns row objects instance tuple
        self.cursor = self.conn.cursor()

    def get_table_names(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = self.cursor.fetchall()

        return [table_name[0] for table_name in table_names]

    def get_cols_of(self, table_name):
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        col_info_data = self.cursor.fetchall()

        rows = {}

        for row in col_info_data:
            name = row["name"]
            type_ = row["type"]
            rows[name] = type_


        return rows




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
    def __init__(self, table_name, database):
        self.db = database
        self.table_name = table_name

    def create(self, table_structure):
        self.data_names,self.datatypes=get_keys_values(table_structure)

        self.db.cursor.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name = ?",(self.table_name,))
        table_exists = self.db.cursor.fetchone()


        if table_exists == None:
            query="CREATE TABLE {} ".format(self.table_name)
            temp=''

            for dataname,datatype in zip(self.data_names,self.datatypes):
                temp+=(dataname+" "+datatype+",")


            temp="(" + temp.strip(',') + ")"
            query += temp


            print("Creating table {}".format(self.table_name))
            self.db.cursor.execute(query)
            print("table created")

            self.table_structure = table_structure


    def get_scheme(self):
        return self.db.get_cols_of(table_name=self.table_name)



    def insert(self,row_dict):

        keys,values=get_keys_values(row_dict)
        query = "INSERT INTO {}".format(self.table_name) + "("
        converter = Str_List_Converter()
        string = converter.list_to_string(word_list = keys,concate_with=',')
        query+= string+ ")"

        string = ''

        for _ in range(len(keys)):
            string += '?,'

        string=string.strip(',')
        query  += " VALUES (" + string +")"
        insert_values=tuple(values)




        self.db.cursor.execute(query,insert_values)
        self.db.conn.commit()


    def drop_table(self):
        self.db.conn.execute("drop table if exists {}".format(self.table_name,))

    def delete_row(self,row_dict):

        if self.data_exists(row_dict) == False:
            print("No data name {} exists in the database to delete".format(row_dict))
            return



        keys , values = get_keys_values(row_dict)
        query = "DELETE FROM {} ".format(self.table_name) + " WHERE "
        query += self._make_spesific_data_query(keys,concatinate_with='and')
        values = tuple(values)

        self.db.conn.execute(query,values)
        self.db.conn.commit()






    def select_where(self,row_dict):

        '''
        return a list of match results.
        '''

        keys , values = get_keys_values(row_dict)
        query = "SELECT * FROM {}".format(self.table_name)+" WHERE "
        query += self._make_spesific_data_query(keys,concatinate_with='and')

        values = tuple(values)
        self.db.cursor.execute(query,values)
        results = self.db.cursor.fetchall()

        match_results = []

        if results:
            for result in results:
                match_results.append(dict(result))


        return match_results





    def update(self,olddata_dict,newdata_dict):
        new_keys,new_values = get_keys_values(newdata_dict)
        query = "UPDATE {}".format(self.table_name) + " SET "
        query += self._make_spesific_data_query(new_keys)
        query += " WHERE "
        old_keys,old_values = get_keys_values(olddata_dict)

        query += self._make_spesific_data_query(old_keys,concatinate_with ='and')

        values=new_values  + old_values
        values = tuple(values)

        self.db.conn.execute(query,values)
        self.db.conn.commit()






    def get_all_rows(self):

        '''
        Return a list of dict objects where  each dict represents a row

        '''

        self.db.cursor.execute("SELECT * FROM {}".format(self.table_name))
        rows = self.db.cursor.fetchall()

        result = []

        for row in rows:
            result.append(dict(row))


        return result


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

        if type(id_) != int:
            raise TypeError("Id must be a int")

        row_dict={"ROWID" :id_}

        row = self.select_where(row_dict)

        if len(row) == 0:
            print("No data with id {}".format(id_))

        elif len(row) > 1:
            print("Warrning: {} data with id {} was found.".format(len(row),id_))

        return row[0]


    def last_insert_id(self):
        query = "SELECT MAX(ROWID) FROM {}".format(self.table_name)
        result=dict(self.db.cursor.execute(query).fetchone())
        return result['MAX(ROWID)']


    def get_data_of_index(self, start_index , end_index):
        length = (end_index + 1)- start_index
        
        query = f"SELECT * FROM {self.table_name} LIMIT {length} OFFSET {start_index};" 
        self.db.cursor.execute(query)
        rows = self.db.cursor.fetchall()

        results = []

        for row in rows:
            results.append(dict(row))

        return results









if __name__ == "__main__":

    database = Database(path="test.db")
    database.connect()

    table_structure={"name":"text","city":"text"}
    table = Table(table_name="test", database=database)
    table.create(table_structure=table_structure)


    h1 = {"name" : "Superman", "city" : "metropolis"}
    h2 = {"name" : "Spiderman", "city" : "New york"}
    h3 = {"name": "Batman","city": "Gotham"}

    h4={"name" : "Iron Man" , "city": "New york"}

    table.insert(h1)
    table.insert(h2)
    table.insert(h3)

    rows = table.get_all_rows()
    print("1.After inserting ..")
    table.show_rows_of(rows)

    print("data with id 1")
    print(table.select_by_id(1))



    print("2.After deleting {}".format(h2['name']))
    table.delete_row(h2)
    rows = table.get_all_rows()
    table.show_rows_of(rows)



    print("3.After updating {} to {}".format(h1['name'],h2['name']))
    table.update(h1,h4)
    rows = table.get_all_rows()
    table.show_rows_of(rows)

    print("4.After getting Batman")
    rows = table.select_where(h3)

    table.show_rows_of(rows)

