![OpenIPC logo](https://openipc.org/assets/openipc-logo-black.svg)

# opendrm-web

Web interface for [OpenDRM](https://github.com/openipc/opendrm) — the OpenIPC
Digital Rights Management service for IP cameras.

Available on port 80 of your device after installation.

## Features

- **Dashboard** — real-time device status, DRM service state, network info
- **DRM Settings** — configure the OpenDRM service (port, log level, stream limit)
- **License Management** — activate and manage your OpenDRM license key
- **Stream Protection** — add and manage protected RTSP/HTTP streams
- **Network Settings** — configure Ethernet (DHCP or static IP)
- **Interface Settings** — change web UI password and color theme
- **Firmware Update** — update device firmware over the network
- **Tools** — web console and file browser

## Installation

Copy the `www/` directory to `/www` on your device:

```sh
scp -r www/* root@<camera-ip>:/www/
```

Or use the provided update script from the device itself:

```sh
/usr/sbin/updateopendrm
```

## Requirements

- OpenIPC firmware with [haserl](https://haserl.sourceforge.net/) CGI support
- A running HTTP server (e.g. `uhttpd` or `lighttpd`) serving `/www/`
- OpenDRM daemon (`opendrm`) installed at `/usr/sbin/opendrm`

## Default Credentials

> ⚠️ **SECURITY WARNING**: The web interface uses the system root credentials.
> You **must** change the default password immediately after first login.
> The interface enforces this — you will be redirected to the password change
> page on every access until a custom password is set.
>
> Default password: `12345`

## Directory Structure

```
www/
├── index.html              # Redirects to /cgi-bin/status.cgi
├── a/
│   ├── logo.svg            # OpenDRM logo
│   ├── main.css            # Web UI stylesheet
│   └── main.js             # Web UI JavaScript
└── cgi-bin/
    ├── status.cgi          # Dashboard
    ├── drm-settings.cgi    # DRM service configuration
    ├── drm-license.cgi     # License management
    ├── drm-streams.cgi     # Protected stream management
    ├── fw-network.cgi      # Network settings
    ├── fw-interface.cgi    # UI settings (password, theme)
    ├── fw-update.cgi       # Firmware update
    ├── tool-console.cgi    # Web console
    ├── tool-files.cgi      # File browser
    └── p/
        ├── common.cgi      # Shared helper functions
        ├── header.cgi      # HTML header & navigation
        └── footer.cgi      # HTML footer

sbin/
├── setnetwork              # Network configuration helper
└── updateopendrm           # Self-update script
```

## Support

OpenIPC offers two levels of support:

- **Free** community support via [Telegram chat](https://openipc.org/#telegram-chat-groups)
- **Paid** commercial support directly from the development team

For specific questions, contact [dev@openipc.org](mailto:dev@openipc.org).

## Contributing

Contributions are welcome. Please keep scripts minimal and optimized for
embedded Linux. Avoid external JavaScript libraries — plain JS is sufficient.
Use valid HTML5. See [OpenIPC contributing guidelines](https://openipc.org/).

## License

MIT — see [LICENSE](LICENSE).
