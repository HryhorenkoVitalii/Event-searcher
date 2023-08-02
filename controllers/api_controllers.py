from typing import Any, Dict

from fastapi import APIRouter
from controllers.responses import DefaultApiResponse
from fastapi import HTTPException
from starlette import status
from controllers.responses import ArtistDataResponse, ConcertDataResponse
from entities import ArtistData, ConcertData
from helpers import Mapper

from entities import ClientRequest

from services import ServiceLocator

router = APIRouter()

@router.get("/get_artists", name='artists', response_model=DefaultApiResponse)
def get_artists(client_request: ClientRequest):
    client_repository = ServiceLocator.get_service("client_repository")
    print(client_request)
    client_repository.store(client_request)
    
    # aggregator = ServiceLocator.get_service("aggregator")
    # payload = aggregator.get_artists(client_request.request)
    
    # mapper =  Mapper[ArtistData, ArtistDataResponse]()

    # if payload is []:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Artist:{client_request} not found')
    return DefaultApiResponse(success=True, payload=[])


@router.get("/get_concerts", name='concerts', response_model=DefaultApiResponse)
def get_concerts(client_request: ClientRequest):
    
    client_repository = ServiceLocator.get_service("client_repository")
    client_repository.store(client_request)
    
    aggregator = ServiceLocator.get_service("aggregator")
    payload: list[ConcertData] = aggregator.get_concerts(client_request.request) 
    
    mapper = Mapper[ConcertData, ConcertDataResponse]()

    if payload is []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Concert: not found')
    return DefaultApiResponse(success=True, payload=mapper.create(payload))
