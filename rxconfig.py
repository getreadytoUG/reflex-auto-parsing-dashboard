import platform
from pathlib import Path

import reflex as rx
import reflex_xy

# Fixed install locations used by the offline bundle (see OFFLINE_SETUP.md).
# Pinning bun_path keeps Reflex's frontend-install cache fingerprint
# (.web/reflex.install_frontend_packages.cached) identical across the build
# machine and every offline target of the same OS, so `reflex run` can skip
# re-resolving packages against the npm registry. Only applied when the path
# actually exists, so developers using a different local bun install are
# unaffected.
_OFFLINE_BUN_PATH = (
    Path(r"C:\bun\bun.exe")
    if platform.system() == "Windows"
    else Path("/opt/bun/bun")
)

_config_kwargs = {
    "app_name": "app",
    "plugins": [
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        reflex_xy.XYPlugin(),
    ],
}
if _OFFLINE_BUN_PATH.exists():
    _config_kwargs["bun_path"] = _OFFLINE_BUN_PATH

config = rx.Config(**_config_kwargs)
