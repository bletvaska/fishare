from fastapi.responses import JSONResponse


class ProblemDetailsResponse(JSONResponse):
    media_type = "application/problem+json"
