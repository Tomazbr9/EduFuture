def slice_courses(courses):
    chunk_size = 5
    grouped_courses = [courses[i:i + chunk_size] for i in range(0, len(courses), chunk_size)]
    return grouped_courses