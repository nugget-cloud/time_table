import unittest

# Assuming the main code is in a separate module named "timetable.py"
from scheduler import ensemble_genetic_algorithm, fitness, generate_initial_timetable

class TestTimetableGeneration(unittest.TestCase):
    
    def setUp(self):
        # Set up dummy data for testing
        self.courses = [
            ("CSC101", "Intro to CS", 3, []),
            ("CSC102", "Data Structures", 3, ["CSC101"]),
        ]
        
        self.instructors = [
            ("Dr. Smith", ["CSC101", "CSC102"], ["Mon9-10", "Tue10-11"], ["Mon9-12", "Tue10-3"], 10, []),
            ("Dr. Doe", ["CSC102"], ["Mon10-11", "Tue11-12"], ["Mon10-12", "Tue11-2"], 8, []),
        ]
        
        self.rooms = [
            ("R101", 30, "lecture", ["projector", "whiteboard"]),
            ("R102", 25, "lecture", ["projector"]),
        ]
    
    def test_ensemble_genetic_algorithm(self):
        # Test the ensemble genetic algorithm function
        timetable = ensemble_genetic_algorithm(self.courses, self.instructors, self.rooms)
        self.assertTrue(len(timetable) == len(self.courses))  # Ensure all courses are scheduled

    def test_fitness_evaluation(self):
        # Test the fitness function
        dummy_schedule = generate_initial_timetable(self.courses, self.instructors, self.rooms)
        score = fitness(dummy_schedule)
        self.assertTrue(score >= 0)  # Ensure fitness is non-negative

    def test_course_in_schedule(self):
        # Test that each course is in the generated schedule
        timetable = ensemble_genetic_algorithm(self.courses, self.instructors, self.rooms)
        scheduled_courses = [entry[0] for entry in timetable]
        for course in self.courses:
            self.assertIn(course[0], scheduled_courses)

    def test_no_duplicate_course_entries(self):
        # Test that no course is scheduled more than once
        timetable = ensemble_genetic_algorithm(self.courses, self.instructors, self.rooms)
        scheduled_courses = [entry[0] for entry in timetable]
        self.assertEqual(len(scheduled_courses), len(set(scheduled_courses)))

    def test_valid_timetable(self):
    # Generate a timetable using the ensemble genetic algorithm
        timetable = ensemble_genetic_algorithm(self.courses, self.instructors, self.rooms)
        
        # Extract the scheduled courses, instructors, rooms, and timeslots
        scheduled_courses = [entry[0] for entry in timetable]
        scheduled_instructors = [entry[1] for entry in timetable]
        scheduled_rooms = [entry[2] for entry in timetable]
        scheduled_timeslots = [entry[3] for entry in timetable]
        
        # 1. No overlapping classes for instructors
        for i in range(len(timetable)):
            for j in range(i+1, len(timetable)):
                if scheduled_instructors[i] == scheduled_instructors[j] and scheduled_timeslots[i] == scheduled_timeslots[j]:
                    self.fail(f"Instructor {scheduled_instructors[i]} has overlapping classes at {scheduled_timeslots[i]}")
        
        # 2. No overlapping classes in rooms
        for i in range(len(timetable)):
            for j in range(i+1, len(timetable)):
                if scheduled_rooms[i] == scheduled_rooms[j] and scheduled_timeslots[i] == scheduled_timeslots[j]:
                    self.fail(f"Room {scheduled_rooms[i]} has overlapping classes at {scheduled_timeslots[i]}")

        # 3. All courses scheduled
        for course in self.courses:
            self.assertIn(course[0], scheduled_courses, f"Course {course[0]} was not scheduled")

        for entry in timetable:
            course_code, instructor_name, _, _ = entry
            instructor_specialties = next((instructor[1] for instructor in self.instructors if instructor[0] == instructor_name), [])
            self.assertIn(course_code, instructor_specialties, f"Instructor {instructor_name} should not teach {course_code}")


    # Add more tests as needed

if __name__ == '__main__':
    unittest.main()
