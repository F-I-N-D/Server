import os
import time
import enum
from pynput import keyboard
from datetime import datetime
from threading import Thread
from rich.console import Console
from rich.table import Table
from rich import box
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.panel import Panel
from rich.tree import Tree
from rich.spinner import Spinner
from rich.align import Align
from Server.Swarm.Swarm import Action

console = Console()

class State(enum.Enum):
    Connect = 0
    Connecting = 1
    Connected = 2
    Kill = 3

class Gui:
    def __init__(self):
        self.generateLayout()
        self.state = State.Connect
        self.buttonSelected = 0
        self.buttonPressed = False
        self.buttons = 0
        self.key = None
        self.action = None

    def update(self):
        self.checkInput()

        self.layout["header"].update(self.generateHeaderGrid())
        self.layout["buttons"].update(self.generateButtonArea())

        if self.buttonPressed:
            if self.state == State.Connect:
                if self.buttonSelected == 0:
                    self.action = Action.Connect
                    self.state = State.Connecting
            elif self.state == State.Connected:
                if self.buttonSelected == 0:
                    self.action = Action.Search
                    self.state = State.Kill
                elif self.buttonSelected == 1:
                    self.action = Action.Calibrate
                    self.state = State.Kill
                elif self.buttonSelected == 2:
                    self.action = Action.Scatter
                    self.state = State.Kill
                elif self.buttonSelected == 3:
                    self.action = Action.Disconnect
                    self.state = State.Connect
            elif self.state == State.Kill:
                if self.buttonSelected == 0:
                    self.action = Action.Kill
                    self.state = State.Connect

            self.buttonSelected = 0
            self.buttonPressed = False

    def generateLayout(self):
        self.layout = Layout(name = "root")

        self.layout.split(
            Layout(name="header", size = 3),
            Layout(name="logger"),
            Layout(name="buttons", size = 5),
        )

    def generateHeaderGrid(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "Drone server",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid, style="white on blue")

    def generateButtonArea(self) -> Layout:
        layout = Layout(name = "buttons")

        if self.state == State.Connect:
            self.buttons = 1

            layout.split_row(
                Layout(name="connect")
            )

            connectText = Align.center(Text("Connect", justify="center"), vertical="middle")
            layout["connect"].update(Panel(connectText, border_style=("green" if self.buttonSelected == 0 else "blue")))
        elif self.state == State.Connecting:
            self.buttons = 1

            layout.split_row(
                Layout(name="connecting")
            )

            connectText = Align.center(Text("Connecting...", justify="center"), vertical="middle")
            layout["connecting"].update(Panel(connectText, border_style="blue"))
        elif self.state == State.Connected:
            self.buttons = 4

            layout.split_row(
                Layout(name="search"),
                Layout(name="calibrate"),
                Layout(name="scatter"),
                Layout(name="disconnect"),
            )

            searchText = Align.center(Text("Search", justify="center"), vertical="middle")
            layout["search"].update(Panel(searchText, border_style=("green" if self.buttonSelected == 0 else "blue")))

            calibrateText = Align.center(Text("Calibrate", justify="center"), vertical="middle")
            layout["calibrate"].update(Panel(calibrateText,border_style=("green" if self.buttonSelected == 1 else "blue")))

            scatterText = Align.center(Text("Scatter", justify="center"), vertical="middle")
            layout["scatter"].update(Panel(scatterText,border_style=("green" if self.buttonSelected == 2 else "blue")))

            disconnectText = Align.center(Text("Disconnect", justify="center"), vertical="middle")
            layout["disconnect"].update(Panel(disconnectText,border_style=("green" if self.buttonSelected == 3 else "blue")))
        elif self.state == State.Kill:
            self.buttons = 1

            layout.split_row(
                Layout(name="kill")
            )

            killText = Align.center(Text("Kill", justify="center"), vertical="middle")
            layout["kill"].update(Panel(killText, border_style=("green" if self.buttonSelected == 0 else "blue")))
        
        return layout

    def checkInput(self):
        if self.key == keyboard.Key.tab:
            self.buttonSelected += 1
            self.buttonSelected = 0 if self.buttonSelected >= self.buttons else self.buttonSelected
        elif self.key == keyboard.Key.right:
            self.buttonSelected += 1
            self.buttonSelected = self.buttons - 1 if self.buttonSelected >= self.buttons else self.buttonSelected
        elif self.key == keyboard.Key.left:
            self.buttonSelected -= 1
            self.buttonSelected = 0 if self.buttonSelected <= 0 else self.buttonSelected
        elif self.key == keyboard.Key.enter:
            self.buttonPressed = True