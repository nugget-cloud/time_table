# This is the content for run_scheduler.py
from scheduler import ensemble_genetic_algorithm, display_timetable_in_table_format, handle_cancellation

# Sample inputs
courses = [
    ("CS101", "Intro to Computer Science", 3, []),
    ("MATH201", "Advanced Mathematics", 4, ["CS101"])
]

instructors = [
    ("Dr. Alice", ["CS101"], ["Mon9-10", "Tue10-11"], ["Mon9-12", "Tue10-3"], 10, []),
    ("Prof. Bob", ["MATH201"], ["Wed10-11"], ["Tue10-3", "Wed9-12"], 8, [])
]

rooms = [
    ("101", 30, "lecture", ["projector", "whiteboard"]),
    ("102", 20, "lab", ["computers", "projector"])
]

# Running the scheduler with the sample inputs
best_timetable = ensemble_genetic_algorithm(courses, instructors, rooms)

# Optionally handle a course cancellation
canceled_course_code = "none"  # Or any course code to simulate cancellation
if canceled_course_code != 'none':
    best_timetable = handle_cancellation(best_timetable, canceled_course_code)

# Displaying the optimized timetable
print("\nGenerated Timetable:")
display_timetable_in_table_format(best_timetable)
