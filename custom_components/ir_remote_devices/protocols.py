"""IR protocol encoders for local Samsung and Pioneer commands."""

from __future__ import annotations

from typing import override

from infrared_protocols import Command

SAMSUNG_MODULATION = 38000
SAMSUNG_HEADER_HIGH_US = 4500
SAMSUNG_HEADER_LOW_US = 4500
SAMSUNG_BIT_HIGH_US = 560
SAMSUNG_BIT_ONE_LOW_US = 1690
SAMSUNG_BIT_ZERO_LOW_US = 560
SAMSUNG_FOOTER_HIGH_US = 560
SAMSUNG_FOOTER_LOW_US = 560

PIONEER_MODULATION = 40000
PIONEER_HEADER_HIGH_US = 9000
PIONEER_HEADER_LOW_US = 4500
PIONEER_BIT_HIGH_US = 560
PIONEER_BIT_ONE_LOW_US = 1690
PIONEER_BIT_ZERO_LOW_US = 560
PIONEER_TRAILER_SPACE_US = 25500

DEFAULT_REPEAT_TIMES = 4
DEFAULT_REPEAT_WAIT_US = 10000


def _append_repeats(
    timings: list[int], frame: list[int], repeat_count: int, repeat_wait_us: int,
) -> None:
    """Append frame repeats, adding a low interval between complete frames."""
    for repeat_index in range(repeat_count + 1):
        current_frame = list(frame)
        if repeat_index < repeat_count:
            if current_frame[-1] < 0:
                current_frame[-1] -= repeat_wait_us
            else:
                current_frame.append(-repeat_wait_us)
        timings.extend(current_frame)


class SamsungCommand(Command):
    """Samsung IR command matching ESPHome's transmit_samsung encoder."""

    def __init__(
        self,
        *,
        data: int,
        nbits: int = 32,
        modulation: int = SAMSUNG_MODULATION,
        repeat_count: int = DEFAULT_REPEAT_TIMES - 1,
        repeat_wait_us: int = DEFAULT_REPEAT_WAIT_US,
    ) -> None:
        """Initialize a Samsung IR command."""
        super().__init__(modulation=modulation, repeat_count=repeat_count)
        self.data = data
        self.nbits = nbits
        self.repeat_wait_us = repeat_wait_us

    @override
    def get_raw_timings(self) -> list[int]:
        """Get raw timings for the Samsung command."""
        frame: list[int] = [SAMSUNG_HEADER_HIGH_US, -SAMSUNG_HEADER_LOW_US]

        for bit in range(self.nbits, 0, -1):
            low_us = (
                SAMSUNG_BIT_ONE_LOW_US
                if (self.data >> (bit - 1)) & 1
                else SAMSUNG_BIT_ZERO_LOW_US
            )
            frame.extend([SAMSUNG_BIT_HIGH_US, -low_us])

        frame.extend([SAMSUNG_FOOTER_HIGH_US, -SAMSUNG_FOOTER_LOW_US])

        timings: list[int] = []
        _append_repeats(timings, frame, self.repeat_count, self.repeat_wait_us)
        return timings


class PioneerCommand(Command):
    """Pioneer IR command matching ESPHome's transmit_pioneer encoder."""

    def __init__(
        self,
        *,
        rc_code_1: int,
        rc_code_2: int = 0,
        modulation: int = PIONEER_MODULATION,
        repeat_count: int = DEFAULT_REPEAT_TIMES - 1,
        repeat_wait_us: int = DEFAULT_REPEAT_WAIT_US,
    ) -> None:
        """Initialize a Pioneer IR command."""
        super().__init__(modulation=modulation, repeat_count=repeat_count)
        self.rc_code_1 = rc_code_1
        self.rc_code_2 = rc_code_2
        self.repeat_wait_us = repeat_wait_us

    @override
    def get_raw_timings(self) -> list[int]:
        """Get raw timings for the Pioneer command."""
        frame = _build_pioneer_frame(self.rc_code_1)

        if self.rc_code_2:
            frame.append(-PIONEER_TRAILER_SPACE_US)
            frame.extend(_build_pioneer_frame(self.rc_code_2))

        timings: list[int] = []
        _append_repeats(timings, frame, self.repeat_count, self.repeat_wait_us)
        return timings


def _build_pioneer_frame(rc_code: int) -> list[int]:
    """Build a single Pioneer IR frame for an ESPHome rc_code value."""
    address = (rc_code & 0xFF00) | (~(rc_code >> 8) & 0xFF)
    command = _reverse_pioneer_command_byte(rc_code & 0xFF)
    command = (command << 8) | ((~command) & 0xFF)

    frame = [PIONEER_HEADER_HIGH_US, -PIONEER_HEADER_LOW_US]
    _append_pioneer_word(frame, address)
    _append_pioneer_word(frame, command)
    frame.append(PIONEER_BIT_HIGH_US)
    return frame


def _reverse_pioneer_command_byte(command: int) -> int:
    """Reverse the low and high nibbles as ESPHome does for Pioneer codes."""
    reversed_command = 0

    for bit in range(4):
        if (command >> bit) & 1:
            reversed_command |= 1 << (7 - bit)

    for bit in range(4):
        if (command >> (bit + 4)) & 1:
            reversed_command |= 1 << (3 - bit)

    return reversed_command


def _append_pioneer_word(timings: list[int], word: int) -> None:
    """Append a 16-bit Pioneer word, most significant bit first."""
    for mask in (1 << bit for bit in range(15, -1, -1)):
        timings.extend(
            [
                PIONEER_BIT_HIGH_US,
                (
                    -PIONEER_BIT_ONE_LOW_US
                    if word & mask
                    else -PIONEER_BIT_ZERO_LOW_US
                ),
            ],
        )
