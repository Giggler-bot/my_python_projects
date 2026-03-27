import json

def collect_student_info():
    name = input("Enter your full name: ")
    sem = input("Enter your semester: ")
    course_input = (input(
        "Enter at least 7 courses each separated by a comma (you can chose to shorten them. E.g calculus as CAL): "))

    courses = [course.strip()
                            for course in course_input.split(",") if course.strip()]
    return name, sem, courses


print("Welcome to the GPA Calculator!")
name, sem, courses = collect_student_info()


def validate_courses(courses):
    while len(courses) < 7:
        print("\nYou must enter at least 7 courses. Please try again.")
        print("1. Add remaining courses")
        print("2. Re-enter all courses")
        print("3. Exit")

        choice = input("Enter your option (1, 2, or 3): ")

        if choice == '1':
            remaining_courses = 7 - len(courses)
            print(
                f"You need to add at least {remaining_courses} more course(s).")
            additional_courses = input(
                "Enter the additional courses separated by a comma: ")
            new_courses = [c.strip()
                                   for c in additional_courses.split(",") if c.strip()]
            courses.extend(new_courses)
        elif choice == '2':
            course_input = input(
                "Re-enter at least 7 courses each separated by a comma: ")
            courses = [course.strip()
                                    for course in course_input.split(",") if course.strip()]
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            exit()
        else:
            print("Invalid option. Please try again.")

    return courses


def confirm_courses(courses):
    print("\nYou have entered the following courses:")
    for i in range(len(courses)):
        print(f"{i+1}. {courses[i]}")

    while True:
        confirmation = input(
            "Are these courses correct? (yes/no): ").strip().lower()
        if confirmation == 'yes':
            return True
        elif confirmation == 'no':
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


courses = validate_courses(courses)
while True:
    if confirm_courses(courses):
        print("\nCourses confirmed. Proceeding to GPA calculation...")
        break
    else:
        print("\nLet's re-enter your courses.")
        course_input = input("Enter your courses separated by comma: ")
        courses = [c.strip() for c in course_input.split(",") if c.strip()]
        courses = validate_courses(courses)

# I need student to input, exams score over hundred and we should get 60% of the exam score. Take class assesments over 40 and course credits for each course as well. Then we can determine the gradepoint for each coourse.


def collect_scores(courses):
   course_records = []
#    Exam score
   for course in courses:
       while True:
           try:
               exam_score = float(
                   input(f"Enter your exam score for {course} (out of 100): "))
               if 0 <= exam_score <= 100:
                   break
               else:
                   print("Exam score must be between 0 and 100. Please try again.")
           except ValueError:
               print("Invalid input. Please enter a number.")

       # Class assessment score
       while True:
           try:
               class_assessment = float(
                   input(f"Enter your class assessment score for {course} (out of 40): "))
               if 0 <= class_assessment <= 40:
                   break
               else:
                   print(
                       "Class assessment score must be between 0 and 40. Please try again.")
           except ValueError:
               print("Invalid input. Please enter a number.")

       # Course credits
       while True:
           try:
               credits = int(
                   input(f"Enter the course credits for {course}: "))
               if credits > 0:
                   break
               else:
                   print("Course credits must be a positive number. Please try again.")
           except ValueError:
               print("Invalid input. Please enter a number.")

       # Calculate total score (60% of exam score + class assessment)
       total_score = round((0.6 * exam_score) + class_assessment, 2)

       course_records.append({
           "course": course,
           "exam_score": exam_score,
           "class_assessment": class_assessment,
           "credits": credits,
           "total_score": total_score
       })
   
   return course_records
course_records = collect_scores(courses)


def get_grade_point(score):
    if score >= 80:
        return "A", 4.0
    elif score >= 75:
        return "A-", 3.75
    elif score >= 70:
        return "B+", 3.50
    elif score >= 65:
        return "B", 3.25
    elif score >= 60:
        return "B-", 3.00
    elif score >= 55:
        return "C+", 2.75
    elif score >= 50:
        return "C", 2.50
    elif score >= 45:
        return "C-", 2.00
    elif score >= 40:
        return "D", 1.50
    else:
        return "F", 0.00
    

def calculate_gpa(records):
    total_quality_points = 0
    total_credits = 0

    print("\nCourse Results:")

    for record in records:
        score = record["total_score"]
        credit = record["credits"]

        grade, grade_point = get_grade_point(score)
        quality_points = grade_point * credit
        
        total_quality_points += quality_points
        total_credits += credit

        print(f"{record['course']}: Total Score = {score}, Grade = {grade}, Grade Point = {grade_point}, Quality Point = {quality_points}")

    if total_credits == 0:
        return 0
    
    cgpa = total_quality_points / total_credits
    return round(cgpa, 2)


def determine_class(cgpa):
    if cgpa >= 3.60:
        return "First Class"
    elif cgpa >= 3.00:
        return "Second Class Upper"
    elif cgpa >= 2.50:
        return "Second Class Lower"
    elif cgpa >= 2.00:
        return "Third Class"
    else:
        return "Fail"


cgpa = calculate_gpa(course_records)
class_type = determine_class(cgpa)
print("\n========== FINAL RESULT ==========")
print(f"Name: {name}")
print(f"Semester: {sem}")
print(f"Cumulative GPA (CGPA): {cgpa}")
print(f"Class: {class_type}")

def save_results(name, sem, course_records, cgpa, class_type):
    data = {
        "name": name,
        "semester": sem,
        "courses": [],
        "cgpa": cgpa,
        "class": class_type
    }

    # Build course list
    for record in course_records:
        grade, grade_point = get_grade_point(record["total_score"])

        data["courses"].append({
            "course": record["course"],
            "exam_score": record["exam_score"],
            "class_assessment": record["class_assessment"],
            "credits": record["credits"],
            "total_score": record["total_score"],
            "grade": grade,
            "grade_point": grade_point
        })

        # load existing data from JSON file if it exists, otherwise start with an empty list
        try:
            with open("gpa_results.json", "r") as file:
                existing_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

        # Remove duplicate (Same name + same sem)
        existing_data = [
            entry for entry in existing_data
            if not (entry["name"] == name and entry["semester"] == sem)
        ]

        # append new data to existing data
        existing_data.append(data)

        # save updated data back to JSON file
        with open("gpa_results.json", "w") as file:
            json.dump(existing_data, file, indent=4)

    print("\nResults saved to gpa_results.json")

save_results(name, sem, course_records, cgpa, class_type)
