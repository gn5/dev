import nox

# https://cjolowicz.github.io/posts/hypermodern-python-02-testing/


@nox.session(python=["3.10"])
def black(session):
    args = session.posargs or locations
    # install_with_constraints(session, "black")
    session.install("black")
    session.run("black", *args)


locations = "src", "tests", "noxfile.py"


@nox.session(python=["3.10"])
def lint(session):
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
    )
    session.run("flake8", *args)


@nox.session(python=["3.10"])
def run(session):
    # args = session.posargs or ["main"]
    session.run("poetry", "install", external=True)


#    session.run("poetry", "run", *args, external=True)
