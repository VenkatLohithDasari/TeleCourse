import os
from natsort import natsorted


def add_course(course_name):
    filtered_course_name = course_name.replace(" ", "")
    f = open(f"./Database/{filtered_course_name}_db.json", "w")
    f.close()
    return f"./Database/{filtered_course_name}_db.json"


def course_list():
    list_course = os.scandir("./Database")
    sorted_course = natsorted(list_course, key=lambda x: x.name)
    final_sorted_course = []
    for file in sorted_course:
        final_sorted_course.append(file.name.replace("_db.json", ""))
    return final_sorted_course
