from starlette.responses import JSONResponse


class ProblemJSONResponse(JSONResponse):
    media_type = "application/problem+json"
