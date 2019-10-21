from django.db import models

from transkribus.trp_utils import (
    trp_get_doc_overview_md,
    crowd_base_url
)


class TrpBaseModel(models.Model):
    """ An abstract base class to add transkribus collection and document IDs to an object """
    col_id = models.CharField(
        max_length=25, blank=True, verbose_name="Collection ID",
        help_text="The collection's Identifier"
    )
    doc_id = models.CharField(
        max_length=25, blank=True, verbose_name="Document ID",
        help_text="The document's Identifier"
    )

    class Meta:
        abstract = True

    def trp_fetch_md(self):
        try:
            result = trp_get_doc_overview_md(self.doc_id)
        except Exception as e:
            result = None
            print(e)
        return result

    def trp_fetch_crowd_link(self):
        try:
            result = crowd_base_url.format(self.col_id, self.doc_id, '1')
        except Exception as e:
            print(e)
            result = None
        return result
