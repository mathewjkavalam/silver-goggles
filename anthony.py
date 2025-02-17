import pathlib
import duckdb

import localLLM

root_path_initial_segment = "C:\\Users\\Mathew Jacob Kavalam\\\
OneDrive - Robert Gordon University\\\
Feb 16th onwards\\AI+Dataanalysis+python"
# Define starting point of searching
root_path = pathlib.Path(root_path_initial_segment) / "test"
root = pathlib.Path(root_path)
# truncate/create catalogue file
try: 
    with open("catalogue.csv", "w") as catalogue_file:
        catalogue_file.write("file_name_with_extension,\
path,most_recent_access_time_in_seconds")
        catalogue_file.write("\n")
except OSError:
    # indicate error source
    print("Something wrong with catalogue file creation!")
# Visit each item in the directory tree 
everything_within_glob_pattern = "**/*"
for file_or_subdirectory in root.glob(everything_within_glob_pattern):
    # Construct a line similar to file.txt,C:\Users\,292282
    file_or_folder_detail = str(file_or_subdirectory.name) + ',' \
                            + str(file_or_subdirectory.parent) + "," \
                      + str(file_or_subdirectory.stat().st_atime) # access time
    # Inorder to make a catalogue of items in the directory
    # append the information of each item to a file
    try: 
        #Comma separated value file - a,b,c\nd,e,f\n...
        with open("catalogue.csv", "a") as catalogue_file:
            catalogue_file.write(file_or_folder_detail)
            catalogue_file.write('\n')
    except OSError:
        # indicate error source
        print("Something wrong with catalogue file writing!")
def get_user_request():
    user_request = "get text files in folders with images"
    return user_request

def from_ai():
    user_request = get_user_request()
    system_prompt = "You are a SQL select query generator AI which is very helpful. You give response which is only SQL select query." \
+ '''The schema of the table that you should generate select queries for is the following:
file_name_with_extension,
path,
most_recent_access_time_in_seconds.
path column gives absolute path of parent
file_name_with_extension column gives filename with file estension at end
''' \
+ "The select query will be used to filter a table that contains information about files and folders in a filesystem. The ensure the table name is exactly catalogue"
    completion = localLLM.client.chat.completions.create(
      model="llama-3.2-1b-instruct",
      messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_request}
      ],
      temperature=0.22,
    )
    query = completion.choices[0].message.content
    # adjust the query portion FROM <tablename>, 
    # wierdly AI does not give FROM catalogue.csv
    # but always gives FROM catalogue!!
    replaceWord = 'FROM catalogue'
    before = query.find(replaceWord)
    after = before+len(replaceWord)
    query = query[:before] + 'FROM catalogue.csv' + query[after:]
    print(query)
    return query

query = from_ai()
result = duckdb.sql(query)
print(result)

