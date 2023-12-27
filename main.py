from simple_database.database import Table
from simple_database.database import Database


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

