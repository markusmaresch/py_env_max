#
# -*- coding: utf-8 -*-
#


class ReqCmd:
    @staticmethod
    def req_import() -> bool:
        # Import 'requirements.txt' into internal database
        print('req_import')
        return True

    @staticmethod
    def req_export() -> bool:
        # Export existing python environment to 'requirements.txt' script
        print('req_export')
        return True
