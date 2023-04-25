1. Move to the project directory "cd eastvantage"
2. Install the Virtual env package with 
    "pip install virtualenv"
3. Create Virtualenv with 
    "virtualenv venv"
4. Activate Virtualenv with
    "source venv/bin/activate"
5. Change directory path to
    "cd src/"
6. Install all the pip packages requirements for the code to execute with
    "pip install -r requirements.txt"
6. Start the project server with
    "uvicorn app:app --reload"
7. Go to the postman and invoke all the routings and check.
    * Invoke first /create_tables routing which will create all the required tables for the project to execute.
    * Then invoke /create_location POST method with payload to create location details.
    * Invoke /get_location GET with query params latitude, longitude values to get within range of location details.
    * Invoke /get_location_by_id/{id} GET to get only location details for particular id.
    * Invoke /update_location/{id} PUT to update the location details by Id along with payload details.