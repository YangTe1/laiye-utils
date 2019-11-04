tag=$(docker container ls | grep laiye-utils | awk '{print $1}')
echo $tag
docker container stop $tag
docker container rm $tag
cd /home/works/yangte/laiye-utils/
docker build -t manbug/laiye-utils:v1 -f Dockerfile-dev .
docker run -p 8603:8603 -d manbug/laiye-utils:v1
