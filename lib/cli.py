@cli.command()
@click.argument("instructor_id", type=int)
def sql_instructor_courses(instructor_id):
    """List courses for an instructor using raw SQL"""
    try:
        courses = get_instructor_courses_sql(instructor_id)
        if not courses:
            click.echo(f"No courses found for instructor ID {instructor_id}.")
            return
        click.echo(f"Courses for instructor ID {instructor_id}:")
        for course in courses:
            click.echo(f"Title: {course[0]}, Duration: {course[1]} hours")
    except Exception as e:
        click.echo(f"Error: {str(e)}")