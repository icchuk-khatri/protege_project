from owlready2 import *
import math
import json

# Load or create ontology
onto = get_ontology("file://C:/Users/bijay/Desktop/its/ontology_project/math.owl").load()

with onto:
    # Base Classes
    class Thing(Thing): pass
    class Subject(Thing): pass
    class Formula(Thing): pass
    class Shape(Thing): pass
    class User(Thing): pass
    class Student(User): pass
    class Teacher(User): pass

    # Shapes
    class TwoDShape(Shape): pass
    class ThreeDShape(Shape): pass
    class Triangle(TwoDShape): pass
    class Square(TwoDShape): pass
    class Rectangle(TwoDShape): pass
    class Circle(TwoDShape): pass

    # Formulas
    class TriangleAreaFormula(Formula): pass
    class RectangleAreaFormula(Formula): pass
    class CircleAreaFormula(Formula): pass
    class SquareAreaFormula(Formula): pass

    # Properties

    class hasExpression(DataProperty, FunctionalProperty):
        domain = [Formula]
        range = [str]

    class hasVariables(DataProperty, FunctionalProperty):
        domain = [Formula]
        range = [str]  # JSON string to store variables list

    class hasResult(DataProperty, FunctionalProperty):
        domain = [Formula]
        range = [float]

    class associatedWith(ObjectProperty):
        domain = [Formula]
        range = [Shape]

    class usedIn(ObjectProperty):
        domain = [Formula]
        range = [Subject]

    class teaches(ObjectProperty):
        domain = [Teacher]
        range = [Formula]

    class studies(ObjectProperty):
        domain = [Student]
        range = [Formula]

# Initialize data
def add_initial_data():
    # Subjects
    math_subject = onto.Subject("Math_Subject")
    physics_subject = onto.Subject("Physics_Subject")

    # Shapes
    triangle = onto.Triangle("Triangle_Shape")
    rectangle = onto.Rectangle("Rectangle_Shape")
    circle = onto.Circle("Circle_Shape")
    square = onto.Square("Square_Shape")

    # Formulas
    triangle_formula = onto.TriangleAreaFormula("Triangle_Area_Formula")
    triangle_formula.hasExpression = "0.5 * base * height"
    triangle_formula.hasVariables = json.dumps(["base", "height"])
    triangle_formula.associatedWith = [triangle]
    triangle_formula.usedIn = [math_subject]

    rectangle_formula = onto.RectangleAreaFormula("Rectangle_Area_Formula")
    rectangle_formula.hasExpression = "length * breadth"
    rectangle_formula.hasVariables = json.dumps(["length", "breadth"])
    rectangle_formula.associatedWith = [rectangle]
    rectangle_formula.usedIn = [math_subject]

    circle_formula = onto.CircleAreaFormula("Circle_Area_Formula")
    circle_formula.hasExpression = "3.14 * radius ** 2"
    circle_formula.hasVariables = json.dumps(["radius"])
    circle_formula.associatedWith = [circle]
    circle_formula.usedIn = [math_subject]

    square_formula = onto.SquareAreaFormula("Square_Area_Formula")
    square_formula.hasExpression = "side ** 2"
    square_formula.hasVariables = json.dumps(["side"])
    square_formula.associatedWith = [square]
    square_formula.usedIn = [math_subject]


    
    # Teachers and Students
    teacher = onto.Teacher("Teacher_1")
    teacher.teaches = [triangle_formula, rectangle_formula, circle_formula, square_formula]

    student = onto.Student("Student_1")
    student.studies = [triangle_formula, rectangle_formula, circle_formula, square_formula]

    # Save Ontology
    onto.save(file="math_ontology.owl", format="rdfxml")
    print("Ontology saved successfully!")

# Query ontology
def query_ontology():
    for formula in onto.RectangleAreaFormula.instances():
        print(f"Name: {formula.name}, Expression: {formula.hasExpression}, Variables: {formula.hasVariables}")

    shapes = [shape.name for shape in onto.Shape.instances()]
    formulas = [
        {
            "name": formula.name,
            "expression": formula.hasExpression,
            "variables": formula.hasVariables,
        }
        for formula in onto.Formula.instances()
    ]
    print(f"Shapes: {shapes}")
    print(f"Formulas: {formulas}")
# Run the code
if __name__ == "__main__":
    add_initial_data()
    query_ontology()
