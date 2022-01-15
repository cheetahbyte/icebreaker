from fastapi import APIRouter, Depends
from dto.user import CurrentUser
from docker_client import client
from utils.util import lifter, flatten
from core.security import has_container_perms

router = APIRouter(prefix="/container")


@router.get("/")
async def list_containers(
    limit: int = -1, all: bool = False, user: CurrentUser = Depends(has_container_perms)
) -> list:
    """lists all containers"""
    return [lifter(m) for m in client().containers.list(all=all, limit=limit)]


@router.get("/{id}", tags=["container"])
async def get_container(
    id: str, user: CurrentUser = Depends(has_container_perms)
) -> dict:
    """gets container by id"""
    return flatten(client().containers.get(id).attrs)


@router.put("/{id}/start", tags=["container"])
async def start_container(
    id: str, user: CurrentUser = Depends(has_container_perms)
) -> dict:
    """starts container by id"""
    return client().containers.get(id).start()


@router.put("/{id}/stop", tags=["container"])
async def stop_container(
    id: str, user: CurrentUser = Depends(has_container_perms)
) -> dict:
    """stops container by id"""
    return client().containers.get(id).stop()


@router.put("/{id}/restart", tags=["container"])
async def restart_container(
    id: str, user: CurrentUser = Depends(has_container_perms)
) -> dict:
    """restarts container by id"""
    return client().containers.get(id).restart()


@router.put("/{id}/pause", tags=["container"])
async def pause_container(
    id: str, user: CurrentUser = Depends(has_container_perms)
) -> dict:
    """pauses container by id"""
    return client().containers.get(id).pause()


@router.put("/{id}/resume", tags=["container"])
async def resume_container(
    id: str, user: CurrentUser = Depends(has_container_perms)
) -> dict:
    """unpauses container by id"""
    return client().containers.get(id).unpause()
