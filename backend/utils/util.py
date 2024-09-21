#  Utility functions for the backend


def convert_list_to_dict(cursor):
    # Convert the list of tuples to a list of dictionaries
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
