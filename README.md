# IR Remote Devices for Home Assistant

Custom Home Assistant integration for IR-controlled devices using the first-class
`infrared` entity platform introduced in Home Assistant 2026.4.

The integration currently supports:

- Samsung TV power commands from `samsung-tv-remote.yaml`
- Pioneer receiver power, mute, volume, source, and tuner station commands from
  `esphome-pioneer-remote.yaml`

It creates a Home Assistant config flow where you select:

1. The device profile to control.
2. The existing `infrared` emitter entity that is physically pointed at that
   device.

## Installation

Use HACS as a custom integration repository, or copy
`custom_components/ir_remote_devices` into your Home Assistant
`custom_components` directory.

Restart Home Assistant, then add **IR Remote Devices** from **Settings >
Devices & services > Add integration**.

## Notes for Upstreaming

Home Assistant's preferred architecture is for common protocol encoders and
known device code sets to live in `infrared-protocols`. This custom integration
keeps Samsung and Pioneer protocol encoders local so it is immediately usable,
but the intended upstream path is:

- Contribute `SamsungCommand` and `PioneerCommand` to `infrared-protocols`.
- Contribute the Samsung TV and Pioneer receiver code sets to
  `infrared-protocols.codes`.
- Split this repository's device profiles into upstream-style Home Assistant
  integrations, likely `samsung_infrared` and `pioneer_infrared`.

## Development

Local checks that do not require a Home Assistant checkout:

```bash
python -m compileall custom_components tests
```

The test suite expects Home Assistant 2026.4 or newer and the
`infrared-protocols` package.

