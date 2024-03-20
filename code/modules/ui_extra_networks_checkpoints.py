import html
import os
import time

from modules import shared, ui_extra_networks, sd_models
from modules.ui_extra_networks_checkpoints_user_metadata import CheckpointUserMetadataEditor


class ExtraNetworksPageCheckpoints(ui_extra_networks.ExtraNetworksPage):
    def __init__(self):
        super().__init__('Checkpoints')

        self.allow_prompt = False

    def refresh(self):
        st = time.time()
        shared.refresh_checkpoints()
        print( "took ", time.time() - st, " to refresh checkpoints." )

    def create_item(self, name, index=None, enable_filter=True):
        checkpoint: sd_models.CheckpointInfo = sd_models.checkpoint_aliases.get(name)
        if checkpoint is None:
            return

        path, ext = os.path.splitext(checkpoint.filename)
        search_terms = [self.search_terms_from_path(checkpoint.filename)]
        if checkpoint.sha256:
            search_terms.append(checkpoint.sha256)
        return {
            "name": checkpoint.name_for_extra,
            "filename": checkpoint.filename,
            "shorthash": checkpoint.shorthash,
            "preview": self.find_preview(path),
            "description": self.find_description(path),
            "search_terms": search_terms,
            "onclick": html.escape(f"return selectCheckpoint({ui_extra_networks.quote_js(name)})"),
            "local_preview": f"{path}.{shared.opts.samples_format}",
            "metadata": checkpoint.metadata,
            "sort_keys": {'default': index, **self.get_sort_keys(checkpoint.filename)},
        }

    def get_items_raw(self) -> list:
        return list(sd_models.checkpoints_list)

    def list_items(self):
        # instantiate a list to protect against concurrent modification
        names = list(sd_models.checkpoints_list)
        for index, name in enumerate(names):
            item = self.create_item(name, index)
            if item is not None:
                yield item

    def allowed_directories_for_previews(self):
        return [v for v in [shared.cmd_opts.ckpt_dir, sd_models.model_path] if v is not None]

    def create_user_metadata_editor(self, ui, tabname):
        return CheckpointUserMetadataEditor(ui, tabname, self)
