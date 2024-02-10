
import os
import html

import gradio as gr
import modules.ui_extra_networks as ui_extra_networks
import modules.shared as shared
import modules.scripts as scripts

class Script(scripts.Script):

	def __init__( self ):
		print('Monkeypatching Extra Network Pages')
		self.monkey_patch( )

	def monkey_patch( self ) -> None:
		# ui_extra_networks.ITEMS_PER_PAGE = 5
		# ui_extra_networks.CURRENT_PAGE_NUMBER = 0
		# ui_extra_networks.PAGE_ITEM_COUNTS = { 'Textual Inversion' : 0, 'Lora' : 0, 'Checkpoints' : 0, 'Hypernetworks' : 0 }
		# ui_extra_networks.ACTIVE_CATEGORY_NAME = 'Textual Inversion'

		# ui_extra_networks.ExtraNetworksPage.create_html = create_html_overriden
		# ui_extra_networks.create_ui = create_ui_overriden
		pass
