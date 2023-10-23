import random
import math

def collect_course_data():
    code = input("Enter course code: ")
    title = input("Enter course title: ")
    credits = int(input("Enter course credits: "))
    prerequisites = input("Enter prerequisites (comma-separated course codes, or 'none' if none): ").split(",") if 'none' not in input("Enter prerequisites (comma-separated course codes, or 'none' if none): ") else []
    return (code, title, credits, prerequisites)

def collect_instructor_data():
    name = input("Enter instructor name: ")
    specialties = input("Enter courses the instructor can teach (comma-separated course codes): ").split(",")
    preferences = input("Enter preferred time slots (comma-separated, e.g., Mon9-10,Tue10-11): ").split(",")
    availability = input("Enter available time slots (comma-separated, e.g., Mon9-12,Tue10-3): ").split(",")
    max_load = int(input("Enter maximum teaching load in hours per week for the instructor: "))
    restricted_courses = input("Enter courses the instructor cannot or prefers not to teach (comma-separated course codes, or 'none' if none): ").split(",") if 'none' not in input("Enter courses the instructor cannot or prefers not to teach (comma-separated course codes, or 'none' if none): ") else []
    return (name, specialties, preferences, availability, max_load, restricted_courses)

def collect_room_data():
    room_number = input("Enter room number: ")
    capacity = int(input("Enter room capacity: "))
    room_type = input("Enter room type (lecture/lab/seminar): ")
    facilities = input("Enter available facilities in the room (comma-separated, e.g., projector,whiteboard): ").split(",")
    return (room_number, capacity, room_type, facilities)

def simulated_annealing(courses, instructors, rooms, initial_temperature=100, cooling_rate=0.995, max_iterations=1000):
    current_solution = generate_initial_timetable(courses, instructors, rooms)
    current_fitness = fitness(current_solution)
    best_solution = current_solution
    best_fitness = current_fitness
    temperature = initial_temperature

    for _ in range(max_iterations):
        # Generate a neighboring solution
        neighbor = mutate(current_solution.copy())
        neighbor_fitness = fitness(neighbor)

        # If the neighboring solution is better, or if we decide to explore a worse solution
        if neighbor_fitness > current_fitness or random.random() < (math.e ** ((neighbor_fitness - current_fitness) / temperature)):
            current_solution = neighbor
            current_fitness = neighbor_fitness

            # Update best solution
            if current_fitness > best_fitness:
                best_solution = current_solution
                best_fitness = current_fitness

        # Cool down the temperature
        temperature *= cooling_rate

    return best_solution

def hill_climbing(courses, instructors, rooms, solution, max_iterations=1000):
    current_solution = solution
    current_fitness = fitness(current_solution)
    for _ in range(max_iterations):
        # Generate neighbors
        neighbors = [mutate(current_solution.copy()) for _ in range(5)]
        next_solution = max(neighbors, key=fitness)
        next_fitness = fitness(next_solution)

        # If no better neighbors found, terminate
        if next_fitness <= current_fitness:
            break

        current_solution, current_fitness = next_solution, next_fitness

    return current_solution

# Modifying the ensemble function
def extended_ensemble(courses, instructors, rooms, num_instances=10):
    # Generate timetables using both Genetic Algorithm and Simulated Annealing
    best_timetables = [genetic_algorithm(courses, instructors, rooms) for _ in range(num_instances)]
    best_timetables += [simulated_annealing(courses, instructors, rooms) for _ in range(num_instances)]
    
    # Select the best timetable
    best_timetable = max(best_timetables, key=fitness)
    
    # Refine the best timetable using Hill Climbing
    refined_timetable = hill_climbing(courses, instructors, rooms, best_timetable)

    return refined_timetable

def fitness(schedule):
    score = 100  # Starting score

    for i, entry1 in enumerate(schedule):
        _, instructor1, room1, timeslot1 = entry1
        for j, entry2 in enumerate(schedule):
            if i != j:
                _, instructor2, room2, timeslot2 = entry2

                if room1 == room2 and timeslot1 == timeslot2:
                    score -= 10

                if instructor1 == instructor2 and timeslot1 == timeslot2:
                    score -= 10

    return score

def handle_cancellation(schedule, course_code):

    new_schedule = [s for s in schedule if s[0] != course_code]
    canceled_timeslot = next((timeslot for course, _, room, timeslot in schedule if course == course_code), None)
    if canceled_timeslot:
        for i, (course, instructor, room, timeslot) in enumerate(new_schedule):
            if room == room1 and timeslot.start_time > canceled_timeslot.start_time:
                new_schedule[i] = (course, instructor, room, canceled_timeslot)
                break

    return new_schedule

def generate_initial_timetable(courses, instructors, rooms):
    schedule = []
    for course in courses:
        instructor = random.choice([i for i in instructors if course[0] in i[1] and course[0] not in i[5]])
        room = random.choice(rooms)
        day = random.choice(['Mon', 'Tue', 'Wed', 'Thu', 'Fri'])
        hour = random.choice(range(9, 17))
        timeslot = (day, f"{hour}:00", f"{hour + 1}:00")
        schedule.append((course[0], instructor[0], room[0], timeslot))
    return schedule

def initialize_population(courses, instructors, rooms, population_size=100):
    return [generate_initial_timetable(courses, instructors, rooms) for _ in range(population_size)]

def tournament_selection(population, tournament_size=5):
    tournament = random.sample(population, tournament_size)
    return max(tournament, key=fitness)

def crossover(parent1, parent2):
    child = []
    for gene1, gene2 in zip(parent1, parent2):
        child.append(gene1 if random.random() < 0.5 else gene2)
    return child

def mutate(individual, mutation_rate=0.05):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            _, instructor, room, _ = individual[i]
            day = random.choice(['Mon', 'Tue', 'Wed', 'Thu', 'Fri'])
            hour = random.choice(range(9, 17))
            timeslot = (day, f"{hour}:00", f"{hour + 1}:00")
            individual[i] = (individual[i][0], instructor, room, timeslot)
    return individual

def genetic_algorithm(courses, instructors, rooms, generations=100, population_size=100):
    population = initialize_population(courses, instructors, rooms, population_size)
    for _ in range(generations):
        new_population = []
        for _ in range(population_size):
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)
        population = new_population
    return max(population, key=fitness)

def ensemble_genetic_algorithm(courses, instructors, rooms, num_instances=10):
    best_timetables = [genetic_algorithm(courses, instructors, rooms) for _ in range(num_instances)]
    return max(best_timetables, key=fitness)

def display_timetable_in_table_format(timetable):
    # Header
    header = ["Course Code", "Instructor", "Room", "Day", "Time"]
    table_widths = [max(len(item), 12) for item in header]  # Initial widths based on header

    # Update widths based on data
    for entry in timetable:
        course, instructor, room, timeslot = entry
        day, start_time, end_time = timeslot
        table_widths[0] = max(table_widths[0], len(course))
        table_widths[1] = max(table_widths[1], len(instructor))
        table_widths[2] = max(table_widths[2], len(room))
        table_widths[3] = max(table_widths[3], len(day))
        table_widths[4] = max(table_widths[4], len(f"{start_time}-{end_time}"))

    # Print header
    for i, item in enumerate(header):
        print(item.ljust(table_widths[i] + 2), end="|")
    print("\n" + "-" * (sum(table_widths) + len(table_widths) * 3 + 1))

    # Print data rows
    for entry in timetable:
        course, instructor, room, timeslot = entry
        day, start_time, end_time = timeslot
        print(course.ljust(table_widths[0] + 2), end="|")
        print(instructor.ljust(table_widths[1] + 2), end="|")
        print(room.ljust(table_widths[2] + 2), end="|")
        print(day.ljust(table_widths[3] + 2), end="|")
        print(f"{start_time}-{end_time}".ljust(table_widths[4] + 2), end="|")
        print()

if __name__ == "__main__":
    num_courses = int(input("Enter the number of courses: "))
    courses = [collect_course_data() for _ in range(num_courses)]
    
    num_instructors = int(input("Enter the number of instructors: "))
    instructors = [collect_instructor_data() for _ in range(num_instructors)]

    num_rooms = int(input("Enter the number of rooms: "))
    rooms = [collect_room_data() for _ in range(num_rooms)]

    # Using ensemble genetic algorithm to get an optimized timetable
    best_timetable = ensemble_genetic_algorithm(courses, instructors, rooms)

    # Handling course cancellations
    canceled_course_code = input("Enter the course code of the canceled class (or 'none' if no cancellation): ")
    if canceled_course_code != 'none':
        best_timetable = handle_cancellation(best_timetable, canceled_course_code)
    
    # Displaying the optimized timetable in tabular format
    print("\nGenerated Timetable:")
    print("-" * 80)
    print("{:<15}|{:<15}|{:<15}|{:<15}|{:<15}".format("Course Code", "Instructor", "Room", "Day", "Time"))
    print("-" * 80)
    for entry in best_timetable:
        print("{:<15}|{:<15}|{:<15}|{:<15}|{}:00-{}:00".format(entry[0], entry[1], entry[2], entry[3][0], entry[3][1], entry[3][2]))


