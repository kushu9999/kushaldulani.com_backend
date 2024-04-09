import boto3
from fastapi import APIRouter, HTTPException
from app.db.model import BlogModel
from dotenv import load_dotenv, find_dotenv

load_dotenv()

router = APIRouter()

# DynamoDB configuration
dynamodb = boto3.resource('dynamodb', region_name="ap-south-1")
table_name = "kushal_blogs"

table = dynamodb.Table(table_name)


@router.get("/blogs", tags=["Blogs"])
def read_all_blogs():
    response = table.scan()
    blogs = response.get('Items', [])
    return {"message": "blogs fetched sucessfully", "result": blogs}


@router.post("/blogs", tags=["Blogs"])
def create_blog(blog: BlogModel):
    _ = table.put_item(Item=blog.dict())
    return {"message": "blog created successfully"}


@router.get("/blogs/{id}", tags=["Blogs"])
def read_blog(id: str):
    response = table.get_item(Key={'id': id})
    if 'Item' not in response:
        raise HTTPException(status_code=404, detail="blog not found")
    return {"message": "blog fetched sucessfully", "result": response['Item']} 


@router.put("/blogs/{id}", tags=["Blogs"])
def update_blog(id: str, blog: BlogModel):
    _ = table.update_item(
        Key={'id': id},
        UpdateExpression='SET title = :title, description = :description, thumbnail_link = :thumbnail_link, read_url = :read_url, featured = :featured, tags = :tags',
        ExpressionAttributeValues={
            ':title': blog.title,
            ':description': blog.description,
            ':thumbnail_url': blog.thumbnail_url,
            ':read_url': blog.read_url,
            ':featured': blog.featured,
            ':tags': blog.tags
        }
    )
    return {"message": "blog updated successfully"}


@router.patch("/blogs/{id}", tags=["Blogs"])
def patch_blog(id: str, update_data: dict):
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
    return {"message": "blog patched successfully"}


@router.delete("/blogs/{id}", tags=["Blogs"])
def delete_blog(id: str):
    _ = table.delete_item(Key={'id': id})
    return {"message": "blog deleted successfully"}
