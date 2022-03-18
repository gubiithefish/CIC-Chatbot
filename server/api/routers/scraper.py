from fastapi import APIRouter, HTTPException
from server.services.configuration_dashboard import scraper

router = APIRouter()


@router.post("/api/v1/scraping")
async def scraping(input_url: str = "https://shop.rema1000.dk/brod-kager/baguetteflutes"):
    try:
        products = scraper.scraping(input_url)
        response = {"data": products}
    except Exception as exception:
        raise HTTPException(status_code=404, detail=exception)
    else:
        return response
