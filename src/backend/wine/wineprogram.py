import os
from typing import NewType

from bottles.backend.logger import Logger  # pyright: reportMissingImports=false
from bottles.backend.globals import Paths
from bottles.backend.wine.winecommand import WineCommand

logging = Logger()


class WineProgram:
    program: str = "unknown"
    command: str = ""
    config: dict = {}
    colors: str = "default"
    is_internal: bool = False
    internal_path: str = ""

    def __init__(self, config: dict, silent=False):
        self.config = config
        self.silent = silent

    def get_command(self, args: str = None):
        command = self.command

        if self.is_internal:
            command = os.path.join(Paths.base, self.internal_path, command)

        if args is not None:
            command += f" {args}"

        return command

    def launch(
            self,
            args: str = None,
            terminal: bool = False,
            minimal: bool = True,
            comunicate: bool = False,
            environment: dict = None,
            cwd: str = None,
            action_name: str = "launch"
    ):
        if environment is None:
            environment = {}

        if not self.silent:
            logging.info(f"Using {self.program} -- {action_name}", )

        command = self.get_command(args)
        res = WineCommand(
            self.config,
            command=command,
            terminal=terminal,
            minimal=minimal,
            comunicate=comunicate,
            colors=self.colors,
            environment=environment,
            cwd=cwd
        ).run()
        return res

    def launch_terminal(self, args: str = None):
        self.launch(args=args, terminal=True, action_name="launch_terminal")

    def launch_minimal(self, args: str = None):
        self.launch(args=args, minimal=True, action_name="launch_minimal")
