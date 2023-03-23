from iremover import __version__
import click

@click.group()
@click.version_option(version=__version__)
def main() -> None:
    pass
