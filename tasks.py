from invoke import task


@task
def start(ctx):
    ctx.run("uvicorn src.main:app --reload")


@task
def black_check(ctx):
    ctx.run("black --check src/", pty=True)


@task
def black_fix(ctx):
    ctx.run("black src/", pty=True)


@task
def mypy(ctx):
    ctx.run("mypy src/")


@task
def test(ctx):
    ctx.run("pytest src/")


@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest", pty=True)


@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage report -m", pty=True)
    ctx.run("coverage html", pty=True)
