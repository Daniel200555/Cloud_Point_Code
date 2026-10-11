from sharepoint.models import *

import requests

class SharePointClient:

    def get_library_metadata(self, url: str) -> SourceMetadataLib:
        pass;

    def get_list_metadata(self, url: str) -> SourceMetadataList:
        pass;

    def get_list_quid(self) -> None:
        pass;
