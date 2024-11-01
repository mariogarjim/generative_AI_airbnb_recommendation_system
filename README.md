<a name="readme-top"></a>

<div align="center">

[![Contact](https://img.shields.io/badge/Contact-mariogarjim4%40gmail.com-green)](mailto:mariogarjim4@gmail.com)

</div>

# Generative AI-Powered Airbnb Recommendation System for Madrid 🏙️

## Table of Contents
- [Overview 🔍](#overview)
- [Real-World Need 🌍](#real-world-need)
- [Technical Motivation 🔧](#technical-motivation)
- [Example 👀](#example)

---


## Overview 🔍

Welcome to the **Madrid Airbnb Recommendation System**! This repository provides the code for a generative-AI-based recommendation system designed to help users to find the perfect Airbnb in Madrid (Spain) using natural language input. With this system, tourists can describe their plans and expectations in Madrid, and the system will use generative AI to suggest the best matching Airbnb listing across the city.

## Real-World Need 🌍

Travelers often spend considerable time searching for accommodations that fit their unique needs—be it proximity to local attractions, specific amenities, or budget requirements. This project aims to simplify that process, leveraging the power of generative AI to provide personalized recommendations based on natural language descriptions. By allowing users to convey their preferences in their own words, this system can offer more accurate and relevant Airbnb options, enhancing the overall travel experience in Madrid.

## Technical Motivation 🔧

Tabular data is one of the most commonly used formats for data processing and analysis. The use of pre-defined columns  enables easy filtering of records based on logical conditions, such as `night_price < 100$`. This process is relatively straightforward for programmers when they can  encpasulate the conditions specified by the user. However, when dealing with natural language sentences, it can be a hell of a challenge to accurately determine user needs and requirements. 

This challenge is particularly evident when it comes to search for accommodation, as the same place can be referred to in different ways. For example, a user might say:

    "I need an accommodation near the Cívitas Metropolitano stadium. We are two people."

While another user might describe it differently:

    "My sister and I are looking for an Airbnb because we’re traveling to watch the match of Atlético de Madrid."

Despite the differences in phrasing, both users are essentially requesting for an Airbnb near the Atelico de Madrid stadium for two people.

Traditional solutions often involve multiple drop-down menus filled with a bunch of options. Even Airbnb's own website uses a fancy menu for the user to select their Airbnb requirements. This approach can be frustrating for users, especially when they need a filter that hasn't been considered.

![Airbnb User Interface](docs/airbnb_bar.PNG)

This work explores the use of OpenAI's large language model (LLM) to improve the process of extracting user preferences from natural language input, and to reasonedly recommend the perfect Airbnb for the user's needs. 

## Example 👀

A simplistic frontend was implemented to show the system in a more visual way. 

![Recommendator Menu](docs/airbnb_recommendation_menu.PNG)

The procedure is quite straightforward. 
We give to the system some information about our travel.

![Recommendator Question Example](docs/airbnb_recommendation_question.png)

And we get a recommendation consisting of a picture of the accommodation, why it's perfect for us, and a link to the Airbnb website:

![Recommendator Answer Example](docs/airbnb_recommendation_answer.PNG)

