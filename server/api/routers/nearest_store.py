from fastapi import APIRouter, HTTPException
from server.services.nearest_store import store_info

router = APIRouter()


@router.get("/api/v1/nearest_store")
async def nearest_store(city: str = "Aarhus"):
    try:
        lon, lan = store_info.get_coordinates(city)
        location = store_info.get_closest_store(lon, lan)
        response = {"msg": f"Den nærmeste butik fra din by ligger i {location['data']['name']} " +
                           f"med {location['data']['dist']} kilometers afstand i fuglelinje",
                    "data": location}
    except Exception as exception:
        raise HTTPException(status_code=404, detail=exception)
    else:
        return response


@router.get("/api/v1/weather_forecast")
async def nearest_store(city: str = "Aarhus"):
    try:
        forecast = store_info.get_weather_forecast(city)
        response = {"msg": f"Temperaturen for {city} vil i dag svinge mellem {forecast['today']['min_temp']} og " +
                           f"{forecast['today']['max_temp']} grader 🌡, med en gennemsnitlig blæst på " +
                           f"{forecast['today']['avg_wind']} km/t og vindstød op til {forecast['today']['max_wind']} " +
                           f"km/t 💨. Til gengæld er der lige nu {forecast['currently']['temp']} grader, en " +
                           f"gennemsnitlig blæst på {forecast['currently']['wind_speed']} km/t og en fugtighed på " +
                           f"{forecast['currently']['humidity']}% 🌈",
                    "data": forecast}
    except Exception as exception:
        raise HTTPException(status_code=404, detail=exception)
    else:
        return response

