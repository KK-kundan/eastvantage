import uvicorn
from starlette.requests import Request
from starlette.responses import JSONResponse
import payload_models.request_body_mapping as req_mapping
from Log.logWrapper import CustomLogger, logging
from db import models

from fastapi import FastAPI, status
from db import Session
import uuid

logger=CustomLogger(logging.getLogger(__name__)).get_logger()

app=FastAPI(debug=True)

class LocationDetails:
    def __init__(self) -> None:
        self.session=None
        try:
            self.session=Session()
        except Exception as err:
            logger.error(f"Failed to create session with Error ::: {err}", exc_info=err)
    def __del__(self):
        if self.session:
            self.session.close()
    
    def create_location(self, request: Request, address_payload: req_mapping.AddressData):
        """
            Creates the location details based on request address details which 
            has latitude, longitude, location_name details

            Args:
                request (Request): Request context data object
                address_payload (req_mapping.AddressData): location details includes latitude, longitude, location_name details

            Returns:
                _type_: dict type of JSONResponse object
        """
        try:
            logger.info(f"address location data is: {address_payload}")
            add_book = models.AddressBook(
                id=str(uuid.uuid4()),
                latitude=address_payload.latitude,
                longitude=address_payload.longitude,
                location_name=address_payload.location_name
            )
            self.session.add(add_book)
            
            self.session.commit()
            return JSONResponse({"message" : "successfully created"}, status_code=status.HTTP_201_CREATED)
        except Exception as err:
            logger.exception(f"Failed to create location with error ::: {err}", exc_info=err)
            return JSONResponse({"message" : "Failed to create location data"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_location(self, request:Request, latitude:float, longitude: float):
        """
            Gets the array of address details that matches within or equal of
            latitude & longitude coordinates
            
            If data doesn't exists returns 404

            Args:
                request (Request): Request context data object
                latitude (float): latitude coordinate value
                longitude (float): longitude coordinate value

            Returns:
                _type_: dict type of JSONResponse object
        """
        try:
            logger.info(f"location data to fetch is latitude: {latitude} and longitude: {longitude}")
            
            location_data = self.session.query(models.AddressBook).filter(models.AddressBook.latitude<=latitude, models.AddressBook.longitude<=longitude)
            if location_data:
                return [loc for loc in location_data]
            else:
                return JSONResponse({"message" : "No Records Found"}, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            logger.exception(f"Failed to get the location data with err::: {err}",exc_info=err)
            return JSONResponse({"message": "failed to get location data"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    def get_location_by_id(self, request: Request, id:str):
        try:
            loc_details = self.session.query(models.AddressBook).filter(models.AddressBook.id==id).first()
            if loc_details:
                return loc_details
            else:
                return JSONResponse({"message" : "location data doesn't exists"}, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            logger.exception(f"Failed to get the location data with err::: {err}",exc_info=err)
            return JSONResponse({"message": "failed to get location data"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_location(self, request:Request, location_id: str, address_payload:req_mapping.AddressData):
        """
            Updates the location details based on its Identifier. If data doesn't exists returns error message
            Args:
                request (Request): Request context data object
                location_id (str): Location Identifier of the address
                address_payload (req_mapping.AddressData): location details includes latitude, longitude, location_name details

            Returns:
                _type_: dict type of JSONResponse object
        """
        try:
            logger.info(f"location_id: {location_id} going to update with {address_payload}")
            loc_data = self.session.query(models.AddressBook).filter(models.AddressBook.id==location_id).first()
            if loc_data:
                loc_data.latitude=address_payload.latitude
                loc_data.longitude=address_payload.longitude
                loc_data.location_name=address_payload.location_name
                self.session.commit()
                logger.info(f"location_id: {location_id} updated")
                return JSONResponse({"message" : "location address details updated"}, status_code=status.HTTP_200_OK)
            else:
                return JSONResponse({"message" : "location details not exists to update"}, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            logger.exception(f"Failed to update location details for location_id: {location_id} with error::: {err}", exc_info=err)
            return JSONResponse({"message": "Failed to update location details try again"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@app.get('/create_tables')
def create_tables(request: Request):
    try:
        from db.create_tables import creating_tables
        creating_tables()
        logger.info("tables data has been created successfully")
        return True
    except Exception as err:
        logger.exception(f"Failed to created tables & its schema data with error::: {err}", exc_info=err)
        return False

@app.post('/create_location')
def create_location(request: Request, address_payload:req_mapping.AddressData):
    loc_obj = LocationDetails()
    return loc_obj.create_location(request, address_payload)
        

@app.get('/get_location')
def get_location(request: Request, latitude:float, longitude: float):
    loc_obj = LocationDetails()
    return loc_obj.get_location(request, latitude, longitude)

@app.get('/get_location/{id}')
def get_location_by_id(request: Request, id: str):
    loc_obj = LocationDetails()
    return loc_obj.get_location_by_id(Request, id)


@app.put('/update_location/{location_id}')
def update_location(request:Request, location_id: str, address_payload: req_mapping.AddressData):
    loc_obj = LocationDetails()
    return loc_obj.update_location(request, location_id, address_payload)

@app.get('/live')
def get_location_by_id(request: Request, id: str):
    return "API Trigger Success"




if __name__=='__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
