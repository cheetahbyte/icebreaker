from fastapi import APIRouter
from docker_client import client
from utils.util import lifter, flatten

router = APIRouter(prefix="/container", deprecated=True)


@router.get("/list")
async def list_containers(limit: int = -1, all: bool = False) -> list:
    """lists all containers"""
    return [lifter(m) for m in client().containers.list(all=all, limit=limit)]


@router.get("/{id}", tags=["container"])
async def get_container(id: str) -> dict:
    """gets container by id"""
    return flatten(client().containers.get(id).attrs)


@router.put("/{id}/start", tags=["container"])
async def start_container(id: str) -> dict:
    """starts container by id"""
    return client().containers.get(id).start()


@router.put("/{id}/stop", tags=["container"])
async def stop_container(id: str) -> dict:
    """stops container by id"""
    return client().containers.get(id).stop()


@router.put("/{id}/restart", tags=["container"])
async def restart_container(id: str) -> dict:
    """restarts container by id"""
    return client().containers.get(id).restart()


@router.put("/{id}/pause", tags=["container"])
async def pause_container(id: str) -> dict:
    """pauses container by id"""
    return client().containers.get(id).pause()


@router.put("/{id}/unpause", tags=["container"])
async def unpause_container(id: str) -> dict:
    """unpauses container by id"""
    return client().containers.get(id).unpause()
