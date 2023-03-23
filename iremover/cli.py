import sys
import time
import click
import pathlib
import filetype
from tqdm import tqdm
from typing import IO, cast
from iremover.bg import remove
from iremover import __version__
from watchdog.observers import Observer
from iremover.session import new_session
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query, Form, Depends, File
from watchdog.events import FileSystemEvent, FileSystemEventHandler

@click.group()
@click.version_option(version=__version__)
def main() -> None:
    pass


@main.command(help="for a file as input")
@click.option(
    "-m",
    "--model",
    default="u2net",
    type=click.Choice(
        ["u2net", "u2netp", "u2net_human_seg", "u2net_cloth_seg", "silueta"]
    ),
    show_default=True,
    show_choices=True,
    help="model name",
)
@click.option(
    "-a",
    "--alpha-matting",
    is_flag=True,
    show_default=True,
    help="use alpha matting",
)
@click.option(
    "-af",
    "--alpha-matting-foreground-threshold",
    default=240,
    type=int,
    show_default=True,
    help="trimap fg threshold",
)
@click.option(
    "-ab",
    "--alpha-matting-background-threshold",
    default=10,
    type=int,
    show_default=True,
    help="trimap bg threshold",
)
@click.option(
    "-ae",
    "--alpha-matting-erode-size",
    default=10,
    type=int,
    show_default=True,
    help="erode size",
)
@click.option(
    "-om",
    "--only-mask",
    is_flag=True,
    show_default=True,
    help="output only the mask",
)
@click.option(
    "-ppm",
    "--post-process-mask",
    is_flag=True,
    show_default=True,
    help="post process the mask",
)
@click.argument(
    "input", default=(None if sys.stdin.isatty() else "-"), type=click.File("rb")
)
@click.argument(
    "output",
    default=(None if sys.stdin.isatty() else "-"),
    type=click.File("wb", lazy=True),
)
def i(model: str, input: IO, output: IO, **kwargs) -> None:
    output.write(remove(input.read(), session=new_session(model), **kwargs))


@main.command(help="for a folder as input")
@click.option(
    "-m",
    "--model",
    default="u2net",
    type=click.Choice(
        ["u2net", "u2netp", "u2net_human_seg", "u2net_cloth_seg", "silueta"]
    ),
    show_default=True,
    show_choices=True,
    help="model name",
)
@click.option(
    "-a",
    "--alpha-matting",
    is_flag=True,
    show_default=True,
    help="use alpha matting",
)
@click.option(
    "-af",
    "--alpha-matting-foreground-threshold",
    default=240,
    type=int,
    show_default=True,
    help="trimap fg threshold",
)
@click.option(
    "-ab",
    "--alpha-matting-background-threshold",
    default=10,
    type=int,
    show_default=True,
    help="trimap bg threshold",
)
@click.option(
    "-ae",
    "--alpha-matting-erode-size",
    default=10,
    type=int,
    show_default=True,
    help="erode size",
)
@click.option(
    "-om",
    "--only-mask",
    is_flag=True,
    show_default=True,
    help="output only the mask",
)
@click.option(
    "-ppm",
    "--post-process-mask",
    is_flag=True,
    show_default=True,
    help="post process the mask",
)
@click.option(
    "-w",
    "--watch",
    default=False,
    is_flag=True,
    show_default=True,
    help="watches a folder for changes",
)
@click.argument(
    "input",
    type=click.Path(
        exists=True,
        path_type=pathlib.Path,
        file_okay=False,
        dir_okay=True,
        readable=True,
    ),
)
@click.argument(
    "output",
    type=click.Path(
        exists=False,
        path_type=pathlib.Path,
        file_okay=False,
        dir_okay=True,
        writable=True,
    ),
)
def p(
    model: str, input: pathlib.Path, output: pathlib.Path, watch: bool, **kwargs
) -> None:
    session = new_session(model)

    def process(each_input: pathlib.Path) -> None:
        try:
            mimetype = filetype.guess(each_input)
            if mimetype is None:
                return
            if mimetype.mime.find("image") < 0:
                return

            each_output = (output / each_input.name).with_suffix(".png")
            each_output.parents[0].mkdir(parents=True, exist_ok=True)

            if not each_output.exists():
                each_output.write_bytes(
                    cast(
                        bytes,
                        remove(each_input.read_bytes(), session=session, **kwargs),
                    )
                )

                if watch:
                    print(
                        f"processed: {each_input.absolute()} -> {each_output.absolute()}"
                    )
        except Exception as e:
            print(e)

    inputs = list(input.glob("**/*"))
    if not watch:
        inputs = tqdm(inputs)

    for each_input in inputs:
        if not each_input.is_dir():
            process(each_input)

    if watch:
        observer = Observer()

        class EventHandler(FileSystemEventHandler):
            def on_any_event(self, event: FileSystemEvent) -> None:
                if not (
                    event.is_directory or event.event_type in ["deleted", "closed"]
                ):
                    process(pathlib.Path(event.src_path))

        event_handler = EventHandler()
        observer.schedule(event_handler, input, recursive=False)
        observer.start()

        try:
            while True:
                time.sleep(1)

        finally:
            observer.stop()
            observer.join()


@main.command(help="for a http server")
@click.option(
    "-p",
    "--port",
    default=5000,
    type=int,
    show_default=True,
    help="port",
)
@click.option(
    "-l",
    "--log_level",
    default="info",
    type=str,
    show_default=True,
    help="log level",
)
@click.option(
    "-t",
    "--threads",
    default=None,
    type=int,
    show_default=True,
    help="number of worker threads",
)
def s(port: int, log_level: str, threads: int) -> None:
    sessions: dict[str, BaseSession] = {}
    tags_metadata = [
        {
            "name": "Background Removal",
            "description": "Endpoints that perform background removal with different image sources.",
            "externalDocs": {
                "description": "GitHub Source",
                "url": "https://github.com/pchchv/iremover",
            },
        },
    ]
    app = FastAPI(
        title="iremover",
        description="iremover is a tool to remove images background.",
        version=__version__,
        contact={
            "name": "Daniel Gatis",
            "url": "https://github.com/pchchv",
            "email": "ipchchv@gmail.com",
        },
        license_info={
            "name": "MIT License",
            "url": "https://github.com/pchchv/iremover/blob/main/LICENSE.txt",
        },
        openapi_tags=tags_metadata,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    class ModelType(str, Enum):
        u2net = "u2net"
        u2netp = "u2netp"
        u2net_human_seg = "u2net_human_seg"
        u2net_cloth_seg = "u2net_cloth_seg"
        silueta = "silueta"
