#bind = "192.168.1.9:8001"
bind = "192.168.1.9:8000"
#bind = "192.168.1.9:8000"
#bind = "mbhousing.com:8000"
#bind = "0.0.0.0:8000"


errorlog = "/home/ayush/mbhousing/mbhousing/mbhousing-main/MBInventoryTool/gunicorn-error.log"
accesslog = "/home/ayush/mbhousing/mbhousing/mbhousing-main/MBInventoryTool/gunicorn-access.log"

loglevel = "debug"

workers = 4 