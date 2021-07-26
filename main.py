import os
import hashlib
import sqlite3
import datetime


db_path_var = ""

def connect_to_sqlite_db(db_name):
    cursor = sqlite3.connect(str(db_name))

    # Only, when a new database or table is requiered
    cursor.execute("CREATE TABLE hashes (file_name PRIMARY KEY, hash_value)")

    cursor.commit()
    cursor.close()

#connect_to_sqlite_db("test/FPcheck.db")

def new_sqlite_table_timestamps(db_name):
    cursor = sqlite3.connect(str(db_name))

    # Only, when a new database or table is requiered
    cursor.execute("CREATE TABLE timestamps (timestamp String)")

    cursor.commit()
    cursor.close()

#new_sqlite_table_timestamps("test/FPcheck.db")


def get_current_time():
    return str(str(datetime.datetime.now()).split(" ")[0])

def add_timestamp(db_name, the_time):
    cursor = sqlite3.connect(str(db_name))

    cursor.execute("INSERT INTO timestamps (timestamp) VALUES ('" + str(the_time) + "')")

    cursor.commit()
    cursor.close()


def get_all_timestamps(db_name):
    cursor = sqlite3.connect(str(db_name))

    the_timestamps_get = cursor.execute("SELECT * FROM timestamps").fetchall()

    cursor.commit()
    cursor.close()

    if(len(the_timestamps_get) >= 2):
        return str(the_timestamps_get[len(the_timestamps_get) - 2][0])
    else:
        return "NO TIMESTAMPS AVAILABLE"



def replace_unwanted_chars_in_string(the_string):

    the_string = the_string.replace("/", '0')
    the_string = the_string.replace("'", '0')
    the_string = the_string.replace('"', '0')
    the_string = the_string.replace("%", '0')
    the_string = the_string.replace("/", '0')
    the_string = the_string.replace("|", '0')
    the_string = the_string.replace(":", '0')
    the_string = the_string.replace(">", '0')
    the_string = the_string.replace("<", '0')
    the_string = the_string.replace("?", '0')

    return the_string




def check_value_in_database(db_name, file_name, hash_value, normal_file_name):
    cursor = sqlite3.connect(str(db_name))

    if(len(cursor.execute("SELECT * FROM hashes WHERE file_name == '" + file_name + "'").fetchall()) == 0):
        cursor.execute("INSERT INTO hashes (file_name, hash_value) VALUES ('" + file_name + "', '" + hash_value + "')")
        print("| NEW FILE (" + str(normal_file_name) + ") |")
    else:
        #print(cursor.execute("SELECT * FROM hashes WHERE file_name == '" + file_name + "'").fetchall()[0][1])
        if(cursor.execute("SELECT * FROM hashes WHERE file_name == '" + file_name + "'").fetchall()[0][1] == hash_value):
            print("| No Change |")
        else:
            cursor.execute("REPLACE INTO hashes (file_name, hash_value) VALUES ('" + file_name + "', '" + hash_value + "')")
            print("| FILE CHANGED (" + str(normal_file_name) + ") |")

    cursor.commit()
    cursor.close()

    print("----<>----")

#check_value_in_database("FPcheck.db", "test.txt")



#print(os.getcwd())
#print(os.listdir())


def main_part(the_path, db_path_var):

    final_path_to_use = ""

    if(the_path == "" or the_path == None):
        the_list = os.listdir()
        final_path_to_use = ""
    else:
        the_list = os.listdir(the_path)
        final_path_to_use = the_path



    if(os.path.exists(str(os.path.join(str(db_path_var), "FPcheck.db")))):
        pass
    else:
        connect_to_sqlite_db(str(os.path.join(str(db_path_var), "FPcheck.db")))
        new_sqlite_table_timestamps(str(os.path.join(str(db_path_var), "FPcheck.db")))


    if(len(the_list) > 0):
        the_time_get = get_current_time()
        the_time_get_checked = replace_unwanted_chars_in_string(the_time_get)
        add_timestamp(str(os.path.join(str(db_path_var), "FPcheck.db")), the_time_get_checked)

    for counter in the_list:
        if(os.path.isfile(str(os.path.join(str(final_path_to_use), counter)))):
            if(counter != "FPcheck.db"):
                print(counter)
                file = open(str(os.path.join(str(final_path_to_use), counter)), 'rb')
                the_hash_value = hashlib.sha256(file.read()).hexdigest()
                #print(the_hash_value)
                file.close()

                the_hashed_file_name = hashlib.sha256(bytes(counter, 'utf-8')).hexdigest()
                #print(the_hashed_file_name)

                the_file_name_filtered = replace_unwanted_chars_in_string(the_hashed_file_name)
                the_hash_value_filtered = replace_unwanted_chars_in_string(the_hash_value)
                #print(the_file_name_filtered)
                print("FILTERED-HASH: " + the_hash_value_filtered)

                check_value_in_database(str(os.path.join(str(db_path_var), "FPcheck.db")), the_file_name_filtered, the_hash_value_filtered, counter)
            else:
                pass
        else:
            #print("-> SOMETHING ELSE")
            pass

    print("LAST RUN: " + str(get_all_timestamps(str(os.path.join(str(db_path_var), "FPcheck.db")))) + "  =>  This Run: " + str(get_current_time()))



def selector_part():

    db_path_var = ""

    input_cmd = input("</>: ")

    if(input_cmd == "scan"):
        main_part("", "")

    if(input_cmd == "scan -p"):
        add_path_set = input("path: ")
        main_part(add_path_set, "")



    if(input_cmd == "scan -chdb"):
        db_path = input("database path: ")

        if (os.path.exists(db_path)):
            db_path_var = db_path
        else:
            db_path_var = ""

        main_part("", db_path_var)



    if(input_cmd == "scan -p -chdb"):
        db_path = input("database path: ")
        add_path_set = input("path: ")

        if (os.path.exists(db_path)):
            db_path_var = db_path
        else:
            db_path_var = ""

        main_part(add_path_set, db_path)



    if(input_cmd == "help"):
        print("scan [-p, -chdb, -p -chdb]")
        print("help")
        print("exit")

    if(input_cmd == "exit"):
        return 0

    selector_part()

#print(open(os.path.join("", "ein_t.txt"), "r").read())
#print(os.path.exists("testw"))

selector_part()

