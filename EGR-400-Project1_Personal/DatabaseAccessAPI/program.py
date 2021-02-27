from DatabaseAccessAPI.db import DB

"""
Driver for creating the database, showing rows, and editing it
@authors: Tomas Perez, Lauren Nelson, Roberto Rodriguez 
"""
def main():
    print("DBAPI Lab starting up...")
    print()
    db = DB()
    db.create_db()
    db.insert_base_data()
    db.show_all_rows()
    db.show_funny_rows()

    txt = input("Want to search for something? Enter a phrase: ")
    db.search(txt)


if __name__ == '__main__':
    main()
