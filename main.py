from simple_database.database import Table


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

	rows = db.get_all_rows()
	print("1.After inserting ..")
	db.show_rows_of(rows)

	print("data with id 1")
	print(db.select_by_id(1))



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

