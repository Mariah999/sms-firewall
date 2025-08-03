import logging

from flask.cli import FlaskGroup

from project import create_app

app = create_app()
cli = FlaskGroup(create_app=create_app)
app.logger.setLevel(logging.INFO)

if __name__ == "__main__":
    cli()
