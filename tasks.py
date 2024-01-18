from invoke import task


@task
def start(ctx):
    ctx.run("uvicorn src.main:app --reload")


@task
def black_check(ctx):
    ctx.run("black --check src/")


@task
def black_fix(ctx):
    ctx.run("black src/")
