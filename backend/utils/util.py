import docker.models.containers
import docker.models.images

from docker_client import client


def lifter(ct: docker.models.containers.Container) -> dict:
    """converts container to usable dict"""
    return flatten(
        {
            "state": ct.attrs["State"],
            "name": ct.attrs["Name"],
            "id": ct.attrs["Id"],
            "image": Photograph.name(ct.attrs["Image"])[0],
        }
    )


def flatten(dct: dict) -> dict:
    new_dict: dict = {}
    for k, v in dct.items():
        if isinstance(v, dict):
            new_dict[k.lower()] = flatten(v)
        else:
            new_dict[k.lower()] = v
    return new_dict


class Photograph:
    """handles docker images"""

    @staticmethod
    def name(img: str, prefix: bool = True) -> tuple:
        """returns image name"""
        if prefix:
            img = img[7:]
        img: docker.models.images.Image = client().images.get(img)
        return (img.attrs["RepoTags"][0], img.attrs["Id"])
