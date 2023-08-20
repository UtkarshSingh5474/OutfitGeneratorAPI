# Flipkart 5.0 Conversational Fashion Outfit Generator API

This API allows you to generate outfit information in text form, search for clothing items using the Flipkart API, and more. It's part of the **Flipkart 5.0 Conversational Fashion Outfit Generator** project.

## Table of Contents

- [Overview](#overview)
- [Endpoints](#endpoints)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Running the API](#running-the-api)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

The **Flipkart 5.0 Conversational Fashion Outfit Generator** API is built using [FastAPI](https://fastapi.tiangolo.com/) and is designed to provide users with outfit information and clothing item search results using the Flipkart API.

## Endpoints

The API offers the following endpoints:

- `GET /`: Root endpoint that returns a "Hello World" message.
- `GET /ok`: Endpoint that returns a simple "ok" message.
- `GET /outfit_text`: Generates the overview of the outfit in text form.
- `GET /items_flipkart_results`: Finds clothing items in the overview text and returns Flipkart search results.
- `GET /flipkart_search`: Performs a search using the Flipkart API.

## Getting Started

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/UtkarshSingh5474/OutfitGeneratorAPI
   cd OutfitGeneratorAPI
   
2. Install the required dependencies
    ```
   pip install -r requirements.txt
4. Running the API locally
   ```
   uvicorn main:app --host 0.0.0.0 --port 8080

## Usage
1. Use the provided endpoints to interact with the API.
2. Detailed descriptions of each endpoint can be found in the [API documentation](https://outfitgeneratorapi-i3odb6kjxq-em.a.run.app/docs#/).
