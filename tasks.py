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
def test(ctx):
    ctx.run(
        'http POST http://127.0.0.1:8000/delivery_fee cart_value:=100 delivery_distance:=5 number_of_items:=3 time="2024-01-18T12:00:00"'
    )


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
