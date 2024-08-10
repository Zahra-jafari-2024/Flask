# AI Web Application

## Overview

This is a web application that utilizes the models of DeepFace for face analysis and BMR calculator 


## Setup and Installation

* Install Dependencies:

  ```bash
  pip install -r requirements.txt
  ```

* Run

  ```bash
  flask run
  ```
## Docker

  ```bash
  docker pull postgres
  docker run -p 5432:5432 --name some-postgres -e POSTGRES_PASSWORD=password -e POSTGRES_USER=username -e POSTGRES_DB=db_postgres -d postgres
  ```

  ```bash
  docker build -t ai_web_app .
  docker run --rm -p 5432:5432 -p 8080:5000 -v $(pwd):/myapp ai_web_app
  ```

## Docker Network

  ```bash
  docker network create ai_network
  ```
  ```bash
  docker build -t ai_web_app .
  ```
  ```bash
  docker run --network ai_network --name some-postgres -e POSTGRES_PASSWORD=password -e POSTGRES_USER=username -e POSTGRES_DB=db_postgres -d postgres
  ```
  ```bash
  docker run --rm --network ai_network --name ai_web_app -p 8080:5000 -v $(pwd):/myapp ai_web_app
  ```


  
