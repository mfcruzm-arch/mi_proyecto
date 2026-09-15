class File:
    def __init__(self, path: str):
        self.path = path
        self.contents = []

    def add_content(self, content: str):
        self.contents.append(content)

    @property
    def size(self) -> int:
        return sum(len(content) for content in self.contents)

    @property
    def info(self) -> str:
        return f"{self.path} [size={self.size}B]"


class MediaFile(File):
    def __init__(self, path: str, codec: str, geoloc: tuple[float, float], duration: int):
        super().__init__(path)
        self.codec = codec
        self.geoloc = geoloc
        self.duration = duration

    @property
    def info(self) -> str:
        return (
            f"{super().info}\n"
            f"Codec: {self.codec}\n"
            f"Geolocalization: {self.geoloc}\n"
            f"Duration: {self.duration}s"
        )


class VideoFile(MediaFile):
    def __init__(self, path: str, codec: str, geoloc: tuple[float, float], duration: int, dimensions: tuple[int, int]):
        super().__init__(path, codec, geoloc, duration)
        self.dimensions = dimensions

    @property
    def info(self) -> str:
        return (
            f"{super().info}\n"
            f"Dimensions: {self.dimensions}"
        )