import taggy.modules.Queries
from FYP import settings
import FYP

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'FYP.settings'


qryObject = taggy.modules.Queries.Queries()

qryObject.getAnnotators()
