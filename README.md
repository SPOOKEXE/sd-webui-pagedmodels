
# sd-webui-pagedmodels

Hard-code for Stable Diffusion WebUI **FORGE** that has paged models instead of displaying them all into an infinite scroll.
I made this extension because my web ui freezes for a considerable time period when I open the Lora tab, having so many models.

## Installation

1. Copy "ui_extra_networks.py" from the scripts folder into your **FORGE** webui folder under "modules" and replace the file.
2. Done.

## Usage

This extension edits the "Checkpoints", "LORAs", "Hypernetworks" and "Textual Inversion" widgets on the stable diffusion webui.
This extension changes it by making clickable page numbers with a hardcoded amount of '200' by default.

_You can edit this on line 652 in the "ui_extra_networks.py" file._
