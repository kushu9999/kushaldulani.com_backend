from pydantic import BaseModel


class ProjectModel(BaseModel):
    id: str
    title: str
    subtitle: str
    description: str
    thumbnail_url: str
    live_url: str
    github_url: str
    featured: bool = False
    tags: list = []


class BlogModel(BaseModel):
    id: str
    title: str
    description: str
    thumbnail_url: str
    read_url: str
    featured: bool = False
    tags: list = []
