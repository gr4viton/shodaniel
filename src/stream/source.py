from attr import attrib, attrs


@attrs
class StreamSource:
    ip = attrib()
    url = attrib()

    start_streaming = attrib(default=None)

    shodan_match = attrib(default=None)
    formats = ["http://{}/shot.json", "https://{}/shot.json", "http://{}", "https://{}"]

    form = "rtsp://{ip}:554/live/ch00_0"

    @property
    def code(self):
        txt = "source_{ip}".format(ip=self.ip)
        txt = txt.replace(".", "_")
        return txt

    @classmethod
    def from_shodan_match(cls, match):
        ip = match['ip_str']
        url = cls.form.format(ip=ip)
        return cls(
            ip=ip,
            url=url,
            shodan_match=match,
        )

    @classmethod
    def from_ip(cls, ip):
        form = "rtsp://{ip}:554/live/ch00_0"
        url = form.format(ip=ip)
        return cls(ip=ip, url=url)
