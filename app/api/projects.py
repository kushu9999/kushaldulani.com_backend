import boto3
from fastapi import APIRouter, HTTPException
from app.db.model import ProjectModel
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()


# DynamoDB configuration
dynamodb = boto3.resource('dynamodb', region_name="ap-south-1")
table_name = "kushal_projects"

table = dynamodb.Table(table_name)


@router.get("/projects", tags=["Projects"])
def read_all_projects():
    response = table.scan()
    projects = response.get('Items', [])
    return {"message": "projects fetched sucessfully", "result": projects}


@router.post("/projects", tags=["Projects"])
def create_project(project: ProjectModel):
    _ = table.put_item(Item=project.dict())
    return {"message": "project created successfully"}


@router.get("/projects/{id}", tags=["Projects"])
def read_project(id: str):
    response = table.get_item(Key={'id': id})
    if 'Item' not in response:
        raise HTTPException(status_code=404, detail="project not found")
    return {"message": "project fetched sucessfully", "result": response['Item']}


@router.put("/projects/{id}", tags=["Projects"])
def update_project(id: str, project: ProjectModel):
    _ = table.update_item(
        Key={'id': id},
        UpdateExpression='SET title = :title, subtitle = :subtitle, description = :description, thumbnail_url = :thumbnail_url, live_url = :live_url, github_url = :github_url, featured = :featured, tags = :tags',
        ExpressionAttributeValues={
            ':title': project.title,
            ':subtitle': project.subtitle,
            ':description': project.description,
            ':thumbnail_url': project.thumbnail_url,
            ':live_url': project.live_url,
            ':github_url': project.github_url,
            ':featured': project.featured,
            ':tags': project.tags
        }
    )
    return {"message": "project updated successfully"}


@router.patch("/projects/{id}", tags=["Projects"])
def patch_project(id: str, update_data: dict):
    update_expression = 'SET '
    expression_attribute_values = {}
    for key, value in update_data.items():
        update_expression += f"{key} = :{key}, "
        expression_attribute_values[f':{key}'] = value

    update_expression = update_expression.rstrip(', ')
    _ = table.update_item(
        Key={'id': id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    return {"message": "project patched successfully"}


@router.delete("/projects/{id}", tags=["Projects"])
def delete_project(id: str):
    _ = table.delete_item(Key={'id': id})
    return {"message": "project deleted successfully"}
