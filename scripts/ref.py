
# stable-diffusion-webui\modules\ui_extra_networks.py

### INJECT HERE
ITEMS_PER_PAGE : int = 5
CURRENT_PAGE_NUMBER : int = 0
PAGE_ITEM_COUNTS : dict[str, int] = { 'Textual Inversion' : 0, 'Lora' : 0, 'Checkpoints' : 0, 'Hypernetworks' : 0 }
ACTIVE_CATEGORY_NAME : str = 'Textual Inversion'
###

class ExtraNetworksPage:

	### INJECTED HERE ####
	def create_html( self, tabname : str ) -> str: # inject this
		print(f'Creating overriden paginated tab for {tabname}')
		items_html = ''
		self.metadata = {}
		subdirs = {}
		for parentdir in [os.path.abspath(x) for x in self.allowed_directories_for_previews()]:
			for root, dirs, _ in sorted(os.walk(parentdir, followlinks=True), key=lambda x: shared.natural_sort_key(x[0])):
				for dirname in sorted(dirs, key=shared.natural_sort_key):
					x = os.path.join(root, dirname)
					if not os.path.isdir(x):
						continue

					subdir = os.path.abspath(x)[len(parentdir):].replace("\\", "/")
					while subdir.startswith("/"):
						subdir = subdir[1:]

					is_empty = len(os.listdir(x)) == 0
					if not is_empty and not subdir.endswith("/"):
						subdir = subdir + "/"

					if ("/." in subdir or subdir.startswith(".")) and not shared.opts.extra_networks_show_hidden_directories:
						continue

					subdirs[subdir] = 1
		if subdirs:
			subdirs = {"": 1, **subdirs}
		subdirs_html = "".join([f"""
	<button class='lg secondary gradio-button custom-button{" search-all" if subdir=="" else ""}' onclick='extraNetworksSearchButton("{tabname}_extra_search", event)'>
	{html.escape(subdir if subdir!="" else "all")}
	</button>
	""" for subdir in subdirs])
		self.items = { x["name"]: x for x in self.list_items() }

		network_items : list = list(self.items.values())
		total_items : int = len( network_items )

		global CURRENT_PAGE_NUMBER, MAX_PAGE_NUMBER, PAGE_ITEM_COUNTS
		print(tabname, total_items)
		PAGE_ITEM_COUNTS[tabname] = total_items

		import numpy as np
		MAX_PAGE_NUMBER = int(np.ceil(total_items / ITEMS_PER_PAGE))
		if CURRENT_PAGE_NUMBER > MAX_PAGE_NUMBER:
			CURRENT_PAGE_NUMBER = MAX_PAGE_NUMBER
		elif CURRENT_PAGE_NUMBER < 0:
			CURRENT_PAGE_NUMBER = 0

		page_index : int = int(CURRENT_PAGE_NUMBER * ITEMS_PER_PAGE)
		items : list = network_items[int(max(page_index, 0)):int(min(page_index+ITEMS_PER_PAGE, total_items))]

		for item in items:
			metadata = item.get("metadata")
			if metadata:
				self.metadata[item["name"]] = metadata
			if "user_metadata" not in item:
				self.read_user_metadata(item)
			items_html += self.create_html_for_item(item, tabname)
		if items_html == '':
			dirs = "".join([f"<li>{x}</li>" for x in self.allowed_directories_for_previews()])
			items_html = shared.html("extra-networks-no-cards.html").format(dirs=dirs)
		self_name_id = self.name.replace(" ", "_")
		res = f"""
	<div id='{tabname}_{self_name_id}_subdirs' class='extra-network-subdirs extra-network-subdirs-cards'>
	{subdirs_html}
	</div>
	<div id='{tabname}_{self_name_id}_cards' class='extra-network-cards'>
	{items_html}
	</div>
	"""
		return res
	###


def create_ui(interface: gr.Blocks, unrelated_tabs, tabname):
	from modules.ui import switch_values_symbol

	ui = ExtraNetworksUi()
	ui.pages = []
	ui.pages_contents = []
	ui.user_metadata_editors = []
	ui.stored_extra_pages = pages_in_preferred_order(extra_pages.copy())
	ui.tabname = tabname
	related_tabs = []

	for page in ui.stored_extra_pages:
		with gr.Tab(page.title, id=page.id_page) as tab:
			elem_id = f"{tabname}_{page.id_page}_cards_html"
			page_elem = gr.HTML('Loading...', elem_id=elem_id)
			### INJECTED HERE ###
			def set_page_as_mine( ):
				nonlocal page
				if page.title in ['Textual Inversion', 'Lora', 'Checkpoints', 'Hypernetworks']:
					global ACTIVE_CATEGORY_NAME
					ACTIVE_CATEGORY_NAME = page.title
			###
			ui.pages.append(page_elem)
			page_elem.change(fn=lambda: set_page_as_mine, _js='function(){applyExtraNetworkFilter(' + quote_js(tabname) + '); return []}', inputs=[], outputs=[])
			editor = page.create_user_metadata_editor(ui, tabname)
			editor.create_ui()
			ui.user_metadata_editors.append(editor)
			related_tabs.append(tab)

	edit_search = gr.Textbox('', show_label=False, elem_id=tabname+"_extra_search", elem_classes="search", placeholder="Search...", visible=False, interactive=True)
	dropdown_sort = gr.Dropdown(choices=['Default Sort', 'Date Created', 'Date Modified', 'Name'], value='Default Sort', elem_id=tabname+"_extra_sort", elem_classes="sort", multiselect=False, visible=False, show_label=False, interactive=True, label=tabname+"_extra_sort_order")
	button_sortorder = ToolButton(switch_values_symbol, elem_id=tabname+"_extra_sortorder", elem_classes="sortorder", visible=False)
	button_refresh = gr.Button('Refresh', elem_id=tabname+"_extra_refresh", visible=False)
	checkbox_show_dirs = gr.Checkbox(True, label='Show dirs', elem_id=tabname+"_extra_show_dirs", elem_classes="show-dirs", visible=False)

	### injected here ###
	dropdown_page_number = gr.Dropdown(choices=['1'], value='1', elem_id=tabname+"_extra_page_numbers", elem_classes="pagenum", multiselect=False, visible=False, show_label=False, interactive=True, label=tabname+"_page_number_selector")
	import numpy as np
	def update_total_page_numbers() -> None:
		global PAGE_ITEM_COUNTS, ACTIVE_CATEGORY_NAME, ITEMS_PER_PAGE
		total : int = int(np.ceil(PAGE_ITEM_COUNTS[ACTIVE_CATEGORY_NAME] / ITEMS_PER_PAGE))
		print('UPDATE_TOTAL_PAGES: ', total)
		dropdown_page_number.choices = [ (str(c), c) for c in range(total) ]
	update_total_page_numbers()
	###

	ui.button_save_preview = gr.Button('Save preview', elem_id=tabname+"_save_preview", visible=False)
	ui.preview_target_filename = gr.Textbox('Preview save filename', elem_id=tabname+"_preview_filename", visible=False)

	for tab in unrelated_tabs: # injected in list / range(6)
		tab.select(fn=lambda: [gr.update(visible=False) for _ in range(6)], inputs=[], outputs=[edit_search, dropdown_sort, button_sortorder, button_refresh, checkbox_show_dirs, dropdown_page_number], show_progress=False)

	for tab in related_tabs: # injected in list / range(6)
		tab.select(fn=lambda: [gr.update(visible=True) for _ in range(6)], inputs=[], outputs=[edit_search, dropdown_sort, button_sortorder, button_refresh, checkbox_show_dirs, dropdown_page_number], show_progress=False)

	def pages_html():
		if not ui.pages_contents:
			return refresh()
		return ui.pages_contents

	def refresh():
		for pg in ui.stored_extra_pages: pg.refresh()
		ui.pages_contents = [pg.create_html(ui.tabname) for pg in ui.stored_extra_pages]
		# INJECT HERE
		global CURRENT_PAGE_NUMBER
		CURRENT_PAGE_NUMBER = int( dropdown_page_number.value )
		nonlocal update_total_page_numbers
		update_total_page_numbers()
		###
		return ui.pages_contents

	interface.load(fn=pages_html, inputs=[], outputs=[*ui.pages])
	button_refresh.click(fn=refresh, inputs=[], outputs=ui.pages)

	return ui
