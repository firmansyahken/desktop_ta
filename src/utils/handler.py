from PyQt6.QtSql import QSqlQuery

class DatabaseHandler:
    def insert_data(self, table_name, data):
        columns = ', '.join(data.keys())
        values = ', '.join([f":{key}" for key in data.keys()])
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        return self.execute_query(insert_query, data)

    def update_data(self, table_name, data, condition):
        set_clause = ', '.join([f"{key} = :{key}" for key in data.keys()])
        update_query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        return self.execute_query(update_query, data)

    def delete_data(self, table_name, condition):
        delete_query = f"DELETE FROM {table_name} WHERE {condition}"
        return self.execute_query(delete_query)

    def get_data(self, query, bind_values=None):
        result = []
        print(query)
        query_obj = QSqlQuery()
        query_obj.prepare(query)

        if bind_values:
            for key, value in bind_values.items():
                query_obj.bindValue(f":{key}", value)

        if query_obj.exec():
            while query_obj.next():
                row = {}
                for i in range(query_obj.record().count()):
                    row[query_obj.record().fieldName(i)] = query_obj.value(i)
                result.append(row)
        else:
            print("Error:", query_obj.lastError().text())

        return result

    def execute_query(self, query, bind_values=None):
        query_obj = QSqlQuery()
        query_obj.prepare(query)

        if bind_values:
            for key, value in bind_values.items():
                query_obj.bindValue(f":{key}", value)

        return query_obj.exec()


# Contoh penggunaan:
# db_manager = DatabaseManager("my_database.db")
# columns = ["id INTEGER PRIMARY KEY", "name TEXT", "age INTEGER"]
# db_manager.create_table("people", columns)

# data = {"name": "John Doe", "age": 30}
# db_manager.insert_data("people", data)

# update_data = {"name": "Jane Doe", "age": 35}
# condition = "id = 1"
# db_manager.update_data("people", update_data, condition)

# condition = "id = 1"
# db_manager.delete_data("people", condition)

# select_query = "SELECT * FROM people"
# result = db_manager.get_data(select_query)
# print(result)