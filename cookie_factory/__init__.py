import json
from hashlib import md5
from colorsys import hsv_to_rgb
from pathlib import Path
from struct import pack

from .pokemons import pokemons

DATA_FILES_FOLDER = Path(__file__).absolute().parent / Path("data")

with open(DATA_FILES_FOLDER / Path("adjectifs.txt")) as file:
    adjectives = file.read().splitlines()

with open(DATA_FILES_FOLDER / Path("metiers.txt")) as file:
    jobs = file.read().splitlines()

with open(DATA_FILES_FOLDER / Path("villes.json")) as file:
    cities = json.load(file)

with open(DATA_FILES_FOLDER / Path("sexualite.txt")) as file:
    sexual_orient = file.read().splitlines()


class VoiceParameters:

    def __init__(self, speed: int, pitch: int, voice_id: int):
        self.speed: int = speed
        self.pitch: int = pitch
        self.voice_id: int = voice_id

    @classmethod
    def from_cookie_hash(cls, cookie_hash):
        return cls(
            speed=(cookie_hash[5] % 80) + 90,
            pitch=cookie_hash[0] % 100,
            voice_id=cookie_hash[1]
        )


class PokeParameters:

    def __init__(self, color: str, poke_id: int, adj_id: int):
        self.poke_id: int = poke_id
        self.pokename: str = pokemons[self.poke_id]
        self.adj_id: int = adj_id
        self.poke_adj: str = adjectives[self.adj_id]
        self.img_id: str = str(self.poke_id).zfill(3)
        self.color: str = color

    @property
    def fullname(self):
        return "%s %s" % (self.pokename, self.poke_adj)

    @classmethod
    def from_cookie_hash(cls, cookie_hash):
        color_rgb = hsv_to_rgb(cookie_hash[4] / 255, 0.8, 0.9)
        return cls(
            color='#' + pack('3B', *(int(255 * i) for i in color_rgb)).hex(),
            poke_id=(cookie_hash[2] | (cookie_hash[3] << 8)) % len(pokemons) + 1,
            adj_id=(cookie_hash[5] | (cookie_hash[6] << 13)) % len(adjectives) + 1
        )


class PokeProfile:

    def __init__(self, job_id: int, age: int, city_id: int, sex_orient_id: int):
        self.job_id: int = job_id
        self.job: str = jobs[self.job_id]
        self.age: int = age
        self.city_id: int = city_id
        self.sex_orient_id: int = sex_orient_id
        self.city: str
        self.departement: str
        self.city, self.departement = cities[self.city_id]
        self.sex_orient: str = sexual_orient[self.sex_orient_id]

    def to_dict(self):
        return {"job": self.job,
                "age": self.age,
                "city": self.city,
                "departement": self.departement,
                "orientation": self.sex_orient}

    @classmethod
    def from_cookie_hash(cls, cookie_hash):
        return cls(
            job_id=(cookie_hash[4] | (cookie_hash[2] << 7)) % len(jobs),
            age=(cookie_hash[3] | (cookie_hash[5] << 6)) % 62 + 18,
            city_id=((cookie_hash[6] * cookie_hash[4] << 17)) % len(cities),
            sex_orient_id=(cookie_hash[2] | (cookie_hash[3] << 4)) % len(sexual_orient)
        )


def hash_cookie(raw_cookie: str, salt: str) -> bytes:
    return md5((raw_cookie + salt).encode('utf8')).digest()
