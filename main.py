from colorama import Fore, Style, Back
from src import database
from src import courseSections
from tinydb import TinyDB, Query
import src.sectionUpload as sU
import asyncio

print(Fore.LIGHTRED_EX + f'''
████████╗███████╗██╗░░░░░███████╗░█████╗░░█████╗░██╗░░░██╗██████╗░░██████╗███████╗
╚══██╔══╝██╔════╝██║░░░░░██╔════╝██╔══██╗██╔══██╗██║░░░██║██╔══██╗██╔════╝██╔════╝
░░░██║░░░█████╗░░██║░░░░░█████╗░░██║░░╚═╝██║░░██║██║░░░██║██████╔╝╚█████╗░█████╗░░
░░░██║░░░██╔══╝░░██║░░░░░██╔══╝░░██║░░██╗██║░░██║██║░░░██║██╔══██╗░╚═══██╗██╔══╝░░
░░░██║░░░███████╗███████╗███████╗╚█████╔╝╚█████╔╝╚██████╔╝██║░░██║██████╔╝███████╗
░░░╚═╝░░░╚══════╝╚══════╝╚══════╝░╚════╝░░╚════╝░░╚═════╝░╚═╝░░╚═╝╚═════╝░╚══════╝
''' + Style.RESET_ALL)

# Ask User if they want to create new course or Continue existing one!
while True:
    initial_choice = input(
        Fore.BLUE + f"Do you want to create [N]ew Course or [C]ontinue Existing one? [N]/[C]: " + Style.RESET_ALL).lower()
    if initial_choice == "n" or initial_choice == "c":
        break
    else:
        continue

if initial_choice == "n":
    course_name = input(Fore.CYAN + f"Type Course Name (Avoid using Spaces): ")
    folder_path = input(
        r"Input your Course Folder Path (Absolute Path Recommended): ")
    group_id = int(
        input("Input SuperGroup ID (Topics must be enabled): " + Style.RESET_ALL))
    database_file = database.add_course(course_name)
    db = TinyDB(database_file)
    db.insert({'type': 'Info',
               'folder': folder_path,
               'group': group_id
               })
    print("\n")

elif initial_choice == "c":
    clist = database.course_list()
    count = 1
    print(Fore.CYAN + f"Select one from Below:")
    for course in clist:
        print(Fore.BLACK + Back.WHITE + Style.BRIGHT +
              f"{count}. {course}" + Style.RESET_ALL)
        count += 1
    print('\n')
    course_selection = int(input("One Selection? : "))
    database_file = f"./Database/{clist[course_selection-1]}_db.json"
    db = TinyDB(database_file)
    course_db = Query()
    course_details = db.search(course_db.type == "Info")
    folder_path = course_details[0]["folder"]
    group_id = course_details[0]["group"]


async def teleCourse():
    course = courseSections.CourseSection(folder_path)
    final_sections_list = course.all_sections()
    for section in final_sections_list:
        await sU.start(section_name=section['name'],
                       section_path=section['path'],
                       database=database_file,
                       group_id=group_id
                       )


asyncio.run(teleCourse())
