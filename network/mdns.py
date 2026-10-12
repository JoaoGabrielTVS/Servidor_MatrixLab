import socket
from zeroconf import ServiceInfo, Zeroconf


def start_mdns():
    try:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as connection:
                connection.connect(("8.8.8.8", 80))
                local_ip = connection.getsockname()[0]
        except OSError:
            local_addresses = socket.getaddrinfo(
                socket.gethostname(), None, socket.AF_INET
            )
            local_ip = next(
                (
                    address[4][0]
                        for address in local_addresses
                    if not address[4][0].startswith("127.")
                ),
                None,
            )
            if local_ip is None:
                raise OSError("Nenhum endereço IPv4 de rede local foi encontrado")

        desc = {'path': '/chat'}

        info = ServiceInfo(
            "_http._tcp.local.",
            "MatrixLab._http._tcp.local.",
            addresses=[socket.inet_aton(local_ip)],
            port=8000,
            properties=desc,
            server="matrixlab.local.",
        )

        zeroconf = Zeroconf()
        zeroconf.register_service(info, allow_name_change=True)

        print(f"📡 mDNS Ativo: Servidor rodando em http://{local_ip}:8000")
        print("📡 Anunciando na rede local como: MatrixLab (_http._tcp.local.)")

        return zeroconf

    except Exception as e:
        print(f"⚠️ Erro ao iniciar mDNS: {type(e).__name__}: {e!r}")
        return None
