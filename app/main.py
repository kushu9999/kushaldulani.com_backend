import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from app.api import projects, blogs, s3media

# creating fastapi
app = FastAPI(title="KushalDulani.com")

# connect router to main api
app.include_router(s3media.router)
app.include_router(projects.router)
app.include_router(blogs.router)

# origins = ["https://csmqbaeac3g3lvz4t5xk5ck3a40tflkq.lambda-url.ap-south-1.on.aws/", "https:kushaldulani.com", "http://kushaldulani.com"]
origins = ["*"]
# adding middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# homeurl
@app.get("/", tags=["Home"])
def index():
    return {
        "Message": "Hello, Welcome to KushalDulani.com API, goto /docs for more information"
    }


###############################################################################
#   Handler for AWS Lambda                                                    #
###############################################################################


handler = Mangum(app)

###############################################################################
#   Run the self contained application for AWS Lambda                         #
###############################################################################

if __name__ == "__main__":
    uvicorn.run(app, host="https://0.0.0.0", port=5000)
