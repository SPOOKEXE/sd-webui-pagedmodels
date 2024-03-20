
# sd-webui-pagedmodels

Hard-code for Stable Diffusion WebUI **FORGE** that has paged models instead of displaying them all into an infinite scroll.
I made this extension because my web ui freezes for a considerable time period when I open the Lora tab, having so many models.

## Installation

1. Copy and replace the files from "scripts -> modules" into the folder "webui -> modules":
	i.   ui_extra_networks.py
	ii.  ui_extra_networks_checkpoints.py
	iii. ui_extra_networks_hypernets.py
	iv.  ui_extra_networks_textual_inversion.py

2. Copy and replace the files from "scripts -> Lora" into the folder "extensions-builtin -> Lora":
	i. networks.py
	ii. ui_extra_networks_lora.py

3. Done.

## Usage

This extension edits the "Checkpoints", "LORAs", "Hypernetworks" and "Textual Inversion" widgets on the stable diffusion webui.
This extension changes it by making clickable page numbers with a hardcoded amount of '150' by default.

_You can edit this on line 715 in the "ui_extra_networks.py" file._
