# #bind = "192.168.1.9:8001"
# bind = "192.168.31.203:2026"
# #bind = "192.168.1.9:8000"
# #bind = "0.0.0.0:8000"
#
#
# errorlog = "/home/utkarsh/Downloads/mbhousing-main/mbhousing-main/MBInventoryTool/gunicorn-error.log"
# accesslog = "/home/utkarsh/Downloads/mbhousing-main/mbhousing-main/MBInventoryTool/gunicorn-access.log"
#
# loglevel = "debug"
#
# workers = 4


bind = "0.0.0.0:8000"
workers = 3
loglevel = "debug"
accesslog = "-"
errorlog = "-"