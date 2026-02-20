"""Simple interaction state machine for core retail flows."""
from __future__ import annotations

from enum import Enum


class InteractionState(str, Enum):
    IDLE = "idle"
    LISTEN = "listen"
    PROCESS = "process"
    RESPOND = "respond"


class InteractionStateMachine:
    """Finite-state helper for single-turn interactions."""

    def __init__(self) -> None:
        self.state = InteractionState.IDLE

    def begin(self) -> None:
        self.state = InteractionState.LISTEN

    def processing(self) -> None:
        self.state = InteractionState.PROCESS

    def responding(self) -> None:
        self.state = InteractionState.RESPOND

    def reset(self) -> None:
        self.state = InteractionState.IDLE
