import click


@click.group()
@click.argument("file", type=click.File("r"))
def cli(file):
    print(file)


@cli.command()
def tabu():
    click.echo("Run Tabu")


@cli.command()
def bnb():
    click.echo("Run BnB")


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
