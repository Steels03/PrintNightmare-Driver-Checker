import os
import subprocess


def check():
    here = 0
    while here != 1:
        if b'spoolsv.exe' in subprocess.Popen('tasklist', stdout=subprocess.PIPE).communicate()[0] :
            try:
                subprocess.Popen('sc stop "spooler"')
                subprocess.Popen('sc config "spooler" start=disabled')
                here = 1
                print("Print Spooler Service has been disabled!")
            except os.error as e:
                here = 1
                print(e)
        else:
            if b'STOPPED' in subprocess.Popen('sc query "spooler"', stdout=subprocess.PIPE).communicate()[0] :
                print("Print Spooler Service is already stopped.")
                here = 1
            else:
                print("Print Spooler Service was not found.")
                here = 1


def compromise():
    files_list = []
    suspicious = {}

    try:
        for root, dirs, files in os.walk("C:/windows/system32/spool/drivers/", topdown=False):
            for name in files:
                files_list.append((os.path.join(root, name)))
        for i in files_list:
            data = str(subprocess.Popen('powershell.exe "Get-AuthenticodeSignature -FilePath ' +"'"+ i +"'"+ ' | Format-List"', stdout=subprocess.PIPE).communicate()[0])
            if "CN=Microsoft Windows" not in data:
                if "CN" not in data:
                    suspicious[i] = "Not signed"
                else:
                    data = data.split("CN=")[1]
                    data = data.split(",")[0]
                    suspicious[i] = data
    except os.error as e:
        print(e)

    if suspicious:
        print("Some drivers are not signed by Mircosoft, you should check their provenance :")
        for i in suspicious:
            print("- " + i + ' | ' + suspicious[i])
    else:
        print("All of your drivers are signed by Microsoft.")


def main():
    print("Print Spooler Service checking started... (Ctrl + C to quit)")
    check()
    print("Print Spooler Service checking ended...")
    print("Checking drivers signature... (Ctrl + C to quit)")
    compromise()
    print("End of drivers signature checking...")



if __name__ == "__main__":
    main()
