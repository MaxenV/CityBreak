# Overview

This project builds a chat application using the RASA framework to answer questions about locations and populations of Polish cities.
Application is still under development, it currently functions and will be expanded upon in the future.
The chat use Docker for service delivery.
Users can interact with the chat to ask about population figures or locations of Polish cities.
User also can ask about interesting places in city.
The chat retrieves real-time information by querying GUS (Główny Urząd Statystyczny) and Google search API.

## Example questions

- Gdzie leży Wrocław
- Ilu mieszkańców ma Lublin
- A gdzie on się znajduje
- W jakim województwie znajduje się Łódź
- Ilu ludzi mieszka w tym mieście
- Co można tam zobaczyć
- Co można zobaczyć w Zamościu

# How to use

To utilize the chat, you'll need Docker installed on your system.

## Build the chat

### Build docker image

Build container image

```
docker build -t local/citybreak .
```

### Run the Docker Container

```
docker run --rm -dt --env-file .env  -v ./app:/usr/src/app --name CityBreak local/citybreak
```

This command runs a detached container named CityBreak, mounts the app directory from your local system to the /usr/src/app directory within the container, and assigns the name CityBreak to the container.

#### API keys

Without providing Google service keys, queries about interesting places in the city will be unavailable. Other queries about population and location will still function. Providing a GUS key is not required, but it will increase the number of possible queries.

## Run the Chat Interface

This command run chat on shell
Wait few seconds after run container to give the model time to train

```
docker exec -it CityBreak /bin/sh -c "rasa shell"
```

This command starts the RASA shell within the running container, allowing you to interact with the chat. Important: Grant the container a few seconds to allow the model to train before interacting with it.

### Issues

`EOFError: Compressed file ended before the end-of-stream marker was reached` or `The path 'models' does not exist. Please make sure to use the default location ('models') or specify it with '--model'.`: This error might occur if the model doesn't have sufficient time to train. If you encounter this, simply wait a few seconds and retry the docker exec command.

# Future features

This functions will be append in next versions: <br>

- Development of a web interface (GUI) to provide a more user-friendly experience.
- Creation of two Docker image variants:
  - A production-ready image optimized for usability.
  - A development image facilitating easier modification and debugging.
- Exploration of building a lighter-weight Docker image based on a smaller base image.
