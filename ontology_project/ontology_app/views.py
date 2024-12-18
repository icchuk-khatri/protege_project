from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from owlready2 import get_ontology
from sympy import sympify
import matplotlib.pyplot as plt
import io
import base64
import os
import sympy as sp
import json
import numpy as np
# from ontology_logic  import add_initial_data

# Load ontology with error handling

# Load ontology
onto = get_ontology(r"C:\Users\bijay\Desktop\its\math_ontology.owl").load()


def index(request):
    return render(request, "ontology_app/index.html")

from django.contrib import messages

# def teacher_dashboard(request):
#     # Fetch all formulas and organize them hierarchically
#     area_formulas = [f for f in onto.Formula.instances() if "AreaFormula" in f.is_a]
#     shape_formulas = [f for f in onto.Formula.instances() if "Shape" in f.is_a]

#     if request.method == "POST":
#         selected_formulas = request.POST.getlist("formulas")
#         if not selected_formulas:
#             messages.error(request, "Please select at least one topic.")
#             return redirect("teacher_dashboard")
        
#         # Save selected formulas in session
#         request.session["selected_formulas"] = selected_formulas
        
#         # Add a success message
#         messages.success(request, "Topics have been successfully selected.")
#         return redirect("teacher_dashboard")

#     return render(request, "ontology_app/teacher_dashboard.html", {
#         "area_formulas": area_formulas,
#         "shape_formulas": shape_formulas,
#     })

# # Student Dashboard

# def student_dashboard(request):
#     """Handles the student dashboard for calculating and visualizing formulas."""
#     selected_formulas = request.session.get("selected_formulas", [])
#     formulas = [onto.search_one(iri=formula) for formula in selected_formulas]

#     if request.method == "POST":
#         formula_id = request.POST.get("formula")
#         inputs = {var: float(request.POST[var]) for var in request.POST if var not in ["formula", "csrfmiddlewaretoken"]}
#         formula = onto.search_one(iri=formula_id)
#         try:
#             result = evaluate_formula(formula.hasExpression[0], inputs)
#             graph = generate_graph(formula, inputs)
#         except Exception as e:
#             messages.error(request, f"Error: {e}")
#             result, graph = None, None
#         return render(request, "ontology_app/student_dashboard.html", {
#             "formulas": formulas,
#             "selected_formula": formula,
#             "result": result,
#             "inputs": inputs,
#             "graph": graph,
#         })

#     return render(request, "ontology_app/student_dashboard.html", {"formulas": formulas})
# Teacher Dashboard View

# Teacher Dashboard
from django.shortcuts import render
from django.http import JsonResponse
from owlready2 import *
import json

from django.shortcuts import render
from django.http import JsonResponse
from owlready2 import *
import json

# # Load ontology file globally
# ONTOLOGY_PATH = "file://C:/Users/bijay/Desktop/its/ontology_project/math.owl"
# onto = get_ontology(ONTOLOGY_PATH).load()


# Ensure ontology is populated
def ensure_ontology_data():
    # Check if there are existing instances
    if not list(onto.Shape.instances()) or not list(onto.Formula.instances()):
        print("Ontology is empty. Adding initial data...")
        add_initial_data()

def add_initial_data():
    with onto:
        # Check if instances already exist to avoid duplication
        if not list(onto.Shape.instances()) and not list(onto.Formula.instances()):
            print("Populating ontology with initial data...")

            # Shapes
            triangle = onto.Triangle("Triangle_Shape")
            rectangle = onto.Rectangle("Rectangle_Shape")
            circle = onto.Circle("Circle_Shape")
            square = onto.Square("Square_Shape")

            # Formulas
            triangle_formula = onto.TriangleAreaFormula("Triangle_Area_Formula")
            triangle_formula.hasExpression = "0.5 * base * height"
            triangle_formula.hasVariables = json.dumps(["base", "height"])

            rectangle_formula = onto.RectangleAreaFormula("Rectangle_Area_Formula")
            rectangle_formula.hasExpression = "length * breadth"
            rectangle_formula.hasVariables = json.dumps(["length", "breadth"])

            circle_formula = onto.CircleAreaFormula("Circle_Area_Formula")
            circle_formula.hasExpression = "3.14 * radius ** 2"
            circle_formula.hasVariables = json.dumps(["radius"])

            square_formula = onto.SquareAreaFormula("Square_Area_Formula")
            square_formula.hasExpression = "side ** 2"
            square_formula.hasVariables = json.dumps(["side"])

            # Save Ontology
            onto.save(file="math_ontology.owl", format="rdfxml")
            print("Ontology populated and saved.")
        else:
            print("Ontology already has data.")

def teacher_dashboard(request):
    ensure_ontology_data()  # Ensure ontology data is populated

    if request.method == "POST":
        selected_topics = request.POST.getlist("topics")  # Extract topics selected by the teacher
        print("Selected Topics:", selected_topics)

        data = {"shapes": [], "formulas": []}

        # Fetch shapes if "Shape" is selected
        if "Shape" in selected_topics:
            shapes = [shape.name for shape in onto.Shape.instances()]
            data["shapes"] = shapes
            print("Fetched Shapes:", shapes)

        # Fetch formulas if "Formula" is selected
        if "Formula" in selected_topics:
            formulas = [
                {
                    "name": formula.name,
                    "expression": formula.hasExpression,
                    "variables": json.loads(formula.hasVariables),
                }
                for formula in onto.Formula.instances()
            ]
            data["formulas"] = formulas
            print("Fetched Formulas:", formulas)

        return JsonResponse({"data": data})

    return render(request, 'ontology_app/teacher_dashboard.html')
# Student Dashboard View

# Student Dashboard View
def student_dashboard(request):
    # Fetch all available topics dynamically from 'usedIn' property of formulas
    topics = list({subject.name for formula in onto.Formula.instances() for subject in formula.usedIn})
    print("Available Topics:", topics)  # Debugging
    return render(request, 'ontology_app/student_dashboard.html', {"topics": topics})


# Fetch formulas based on the selected topic
def get_formulas(request):
    if request.method == "GET":
        topic = request.GET.get("topic")
        formulas = [
            {"name": formula.name, "expression": formula.hasExpression}
            for formula in onto.Formula.instances()
            for subject in formula.usedIn
            if subject.name == topic
        ]
        print(f"Formulas for Topic '{topic}':", formulas)  # Debugging
        return JsonResponse({"formulas": formulas})

# Fetch variables for a selected formula
def get_variables(request):
    if request.method == "GET":
        formula_name = request.GET.get("formula")
        formula = onto[formula_name]
        variables = json.loads(formula.hasVariables)
        return JsonResponse({"variables": variables})

# Calculate result for the selected formula and generate graph
import json
from django.http import JsonResponse

import json
from django.http import JsonResponse

import json
from django.http import JsonResponse
def calculate_formula(request):
    try:
        # Step 1: Parse the JSON input
        data = json.loads(request.body)
        print("Parsed Data:", data)

        # Step 2: Extract formula name and variables
        formula_name = data.get("formula_name")
        variables = data.get("variables", {})
        print("Formula Name:", formula_name)
        print("Variables:", variables)

        # Step 3: Retrieve formula from ontology
        formula = getattr(onto, formula_name, None)  # Use `getattr` to fetch the formula dynamically
        if not formula:
            raise ValueError(f"Formula '{formula_name}' not found in ontology.")

        # Step 4: Fetch expression and variables
        expression = getattr(formula, "hasExpression", None)
        if not expression:
            raise ValueError(f"No expression found for formula '{formula_name}'.")

        # Step 5: Safely evaluate the expression
        try:
            result = evaluate_formula(expression, variables)
            print("Calculation Result:", result)
        except Exception as eval_error:
            raise ValueError(f"Error evaluating formula: {eval_error}")

        # Step 6: Generate graph
        graph = generate_graph(formula, variables)

        return JsonResponse({"result": result, "graph": graph})

    except Exception as e:
        print("Error in calculate_formula:", e)
        return JsonResponse({"error": str(e)}, status=400)

# Utility to evaluate a formula
def evaluate_formula(expression, variables):
    try:
        print("Evaluating Expression:", expression)
        print("With Variables:", variables)
        safe_expr = sp.sympify(expression)  # Safely parse the formula
        result = safe_expr.evalf(subs=variables)  # Substitute variables
        return float(result)
    except Exception as e:
        print("Evaluation Error:", e)
        raise ValueError(f"Error evaluating formula: {e}")
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-GUI rendering
import sympy as sp
import matplotlib.pyplot as plt
import io
import base64

shape_defaults = {
    "Circle_Area_Formula": {"radius": range(1, 11)},
    "Triangle_Area_Formula": {"base": range(1, 11), "height": range(1, 11)},
    "Square_Area_Formula": {"side": range(1, 11)},
    "Rectangle_Area_Formula": {"length": range(1, 11), "width": range(1, 11)},
}

def generate_graph(formula, variables):
    try:
        formula_name = formula.name  # Extract the formula name

        # Initialize 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Calculate area using the formula expression
        expression = getattr(formula, "hasExpression", None)
        area = evaluate_formula(expression, variables)

        annotation_text = f"Inputs: {variables}\nArea: {area:.2f}"

        if formula_name == "Circle_Area_Formula":
            # Plot a 3D representation of a circle
            radius = variables.get("radius", 1)
            theta = np.linspace(0, 2 * np.pi, 100)
            x = radius * np.cos(theta)
            y = radius * np.sin(theta)
            z = np.zeros_like(x)  # Circle lies in the XY plane
            ax.plot(x, y, z, label=f"Circle (r={radius})")
            ax.text(0, 0, 0.1, annotation_text, color="red")
            ax.set_title("3D Circle")
            ax.set_xlabel("X-axis")
            ax.set_ylabel("Y-axis")
            ax.set_zlabel("Z-axis")

        elif formula_name == "Triangle_Area_Formula":
            # Plot a 3D representation of a triangle
            base = variables.get("base", 1)
            height = variables.get("height", 1)
            triangle_points = np.array([
                [0, 0, 0],
                [base, 0, 0],
                [base / 2, height, 0],
                [0, 0, 0]
            ])
            x, y, z = triangle_points[:, 0], triangle_points[:, 1], triangle_points[:, 2]
            ax.plot(x, y, z, marker="o", label=f"Triangle (base={base}, height={height})")
            ax.text(base / 2, height / 2, 0.1, annotation_text, color="red")
            ax.set_title("3D Triangle")
            ax.set_xlabel("X-axis")
            ax.set_ylabel("Y-axis")
            ax.set_zlabel("Z-axis")

        elif formula_name == "Square_Area_Formula":
            # Plot a 3D representation of a square
            side = variables.get("side", 1)
            square_points = np.array([
                [0, 0, 0],
                [side, 0, 0],
                [side, side, 0],
                [0, side, 0],
                [0, 0, 0]
            ])
            x, y, z = square_points[:, 0], square_points[:, 1], square_points[:, 2]
            ax.plot(x, y, z, marker="o", label=f"Square (side={side})")
            ax.text(side / 2, side / 2, 0.1, annotation_text, color="red")
            ax.set_title("3D Square")
            ax.set_xlabel("X-axis")
            ax.set_ylabel("Y-axis")
            ax.set_zlabel("Z-axis")

        elif formula_name == "Rectangle_Area_Formula":
            # Plot a 3D representation of a rectangle
            length = variables.get("length", 1)
            breadth = variables.get("width", 1)
            rectangle_points = np.array([
                [0, 0, 0],
                [length, 0, 0],
                [length, breadth, 0],
                [0, breadth, 0],
                [0, 0, 0]
            ])
            x, y, z = rectangle_points[:, 0], rectangle_points[:, 1], rectangle_points[:, 2]
            ax.plot(x, y, z, marker="o", label=f"Rectangle (length={length}, width={breadth})")
            ax.text(length / 2, breadth / 2, 0.1, annotation_text, color="red")
            ax.set_title("3D Rectangle")
            ax.set_xlabel("X-axis")
            ax.set_ylabel("Y-axis")
            ax.set_zlabel("Z-axis")

        else:
            raise ValueError(f"Unsupported formula for graphing: {formula_name}")

        # Display legend
        ax.legend()

        # Save the graph as Base64
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        graph_base64 = base64.b64encode(buf.read()).decode("utf-8")
        buf.close()
        plt.close()

        return graph_base64

    except Exception as e:
        print("Error in generate_graph:", e)
        raise ValueError(f"Error generating graph: {e}")

# Query Data Example

def query_data(request):
    """Sample query data for ontology."""
    sample_data = [
        {
            "Subject": "Math",
            "Code": "MTH101",
            "Teachers": ["Alice", "Bob"],
            "Students": ["Eve", "Mallory", "Trent"],
        },
    ]
    return render(request, 'ontology_app/query_data.html', {'data': sample_data})
