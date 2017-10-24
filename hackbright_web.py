"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    rows = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           rows=rows)

    return html
    # return "{acct} is the GitHub account for {first} {last}".format(
    #     acct=github, first=first, last=last)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/new-student")
def form_for_new_student():
    """Display form for collecting new student info."""

    return render_template("new_student.html")


@app.route("/add-student", methods=["POST"])
def add_new_student():
    """Adds new student."""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)

    return render_template("student_confirmation.html",
                            first_name=first_name,
                            last_name=last_name,
                            github=github)


@app.route("/project")
def display_project_info():
    """Displays project details."""

    title = request.args.get('title')

    project = hackbright.get_project_by_title(title)

    return render_template("project_info.html",
                             title=project[0],
                             description=project[1],
                             max_grade=project[2])

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
