NAME='kushaldulani_website'
TAG='image-lambda'
VERSION='1.0.0'
AWS_ACCOUNT_NUMBER='502280061966'
AWS_REGION='ap-south-1'

aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_NUMBER.dkr.ecr.$AWS_REGION.amazonaws.com

# docker build -t $NAME:$TAG-$VERSION .
# docker build --platform linux/amd64 -t $NAME:$TAG-$VERSION .
docker build --platform linux/amd64 -f Dockerfile.lambda -t $NAME:$TAG-$VERSION .

docker tag $NAME:$TAG-$VERSION $AWS_ACCOUNT_NUMBER.dkr.ecr.$AWS_REGION.amazonaws.com/$NAME:$TAG-$VERSION

docker push $AWS_ACCOUNT_NUMBER.dkr.ecr.$AWS_REGION.amazonaws.com/$NAME:$TAG-$VERSION