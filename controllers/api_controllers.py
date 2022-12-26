from typing import Any, Dict

from fastapi import APIRouter
from controllers.responses import DefaultApiResponse
from fastapi import HTTPException
from starlette import status
from responses import ArtistDataResponse, ConcertDataResponse
from entities import ArtistData, ConcertData
from action import Action
from helpers import Mapper

router = APIRouter()
controller_action = Action()

@router.get("/get_artists", name='names', response_model=DefaultApiResponse)
def get_artists(artist_name):
    payload = controller_action.get_artists(artist_name)    
    mapper =  Mapper[ArtistData, ArtistDataResponse]()

    if payload is []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Artist:{artist_name} not found')
    return DefaultApiResponse(success=True, payload=mapper.create(payload))


@router.get("/get_concerts", name='concerts', response_model=DefaultApiResponse)
def get_concerts(artist_name):
    payload: list[ConcertData] = controller_action.get_concerts(artist_name) 
    mapper = Mapper[ConcertData, ConcertDataResponse]()
    
    if payload is []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Concert:{artist_name} not found')
    return DefaultApiResponse(success=True, payload=mapper.create(payload))
