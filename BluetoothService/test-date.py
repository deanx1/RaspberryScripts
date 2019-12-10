import datetime

dt = datetime.datetime.today()
print dt.year
print dt.month
# date = datetime.strptime(a, "%Y-%m-%d")
# print date


def checkMonth():
    # logger.info("Setting discoverable to on")
    cmd = 'sudo hciconfig hci0 piscan'
    subprocess.check_output(cmd, shell = True )  
