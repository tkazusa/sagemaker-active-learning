# ACCOUNT_ID=`aws sts get-caller-identity --query 'Account' --output text`
ACCOUNT_ID='815969174475'
REGION='us-east-1'
TAG=':latest'
ECR_REPOGITORY='aws-batch-inference'
REGISTRY_URL="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com" 
IMAGE_URI="${REGISTRY_URL}/${ECR_REPOGITORY}"

aws ecr get-login-password | docker login --username AWS --password-stdin $REGISTRY_URL
aws ecr create-repository --repository-name $ECR_REPOGITORY


docker build -t $ECR_REPOGITORY containers/batch/
docker tag "${ECR_REPOGITORY}${TAG}" $IMAGE_URI
docker push $IMAGE_URI

echo "Container registered. URI:${IMAGE_URI}"