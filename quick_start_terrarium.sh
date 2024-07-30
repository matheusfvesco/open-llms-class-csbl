git clone https://github.com/cohere-ai/cohere-terrarium.git && cd cohere-terrarium

docker build -t terrarium .

docker run -p 8080:8080 -d terrarium