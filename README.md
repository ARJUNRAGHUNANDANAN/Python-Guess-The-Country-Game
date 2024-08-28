# Python-Guess-The-Country-Game

This project is under development. There are MD Files in each sub folder describing the details of each folder for the time being. 

## Stack:
![HTML](https://img.shields.io/badge/HTML-%23E34F26?logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-%231572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-%23F7DF1C?logo=javascript&logoColor=black)
![Python](https://img.shields.io/badge/Python-%23239CFF?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-%23000?logo=flask&logoColor=white)


![MIT License](https://img.shields.io/badge/License-MIT-green)
![Google Project IDX](https://img.shields.io/badge/Assisted%20By-Google%20Project%20IDX-lightgrey)
![Google Gemini](https://img.shields.io/badge/Assisted%20By-Google%20Gemini-lightgrey)

---
## Main Home Repo Structure

The project is organized into several components, each with a specific purpose. Here's an overview of the main directories:

### Shape Generator
**Module-Country-Shape-Generator/**: This folder contains the code and resources for generating country shape images used in the game. The images are saved in the format `ISOStandardCode-CountryName.jpg`. Note that this directory contains a partial project focused on the generation of country shapes and not the entire game logic.


| Saudi Arabia  | Germany         | The Bahamas  | Vietnam         |
|:--------------|:----------------|:--------------|:----------------|
| ![SA-SaudiArabia](Module-Country-Shape-Generator/sample_images/SA-SaudiArabia.jpg) | ![DE-Germany](Module-Country-Shape-Generator/sample_images/DE-Germany.jpg) | ![BS-TheBahamas](Module-Country-Shape-Generator/sample_images/BS-TheBahamas.jpg) | ![VN-Vietnam](Module-Country-Shape-Generator/sample_images/VN-Vietnam.jpg) |

### Game UI
**Module-Country-Guesser-Simple-UI/**: This folder contains the code and resources for a simple country guesser game.This app uses a copy of the data generated by the previous module. This is a Flask App. 


| Re-Try  | Correct | Wrong |
|:----|:------|:-------|
| ![Retry](Module-Country-Guesser-Simple-UI/output_sample/attempt-retry.jpg) | ![Correct](Module-Country-Guesser-Simple-UI/output_sample/attempt-correct.jpg) |![Wrong](Module-Country-Guesser-Simple-UI/output_sample/attempt-wrong.jpg) |
|                |                 |

### Better Game UI

| Mobile | Desktop |
|:----|:------|
| ![Mobile](Module-Country-Guesser-Game-UI-(New)/screenshots/betterUI-mobile.jpg) | ![Desktop](Module-Country-Guesser-Game-UI-(New)/screenshots/betterUI-desktop.jpg) |
|                |                 |

Other Improvements may be done later. For now, Shape Generation and Game UI are kept seperate. I haven't packages everything into a single application yet. Maybe later. 

## Demo Video (Click For Video)
[![Better UI Desktop Screenshot](Module-Country-Guesser-Game-UI-(New)/screenshots/betterUI-desktop.jpg)](https://github.com/ARJUNRAGHUNANDANAN/Python-Guess-The-Country-Game/raw/main/Module-Country-Guesser-Game-UI-(New)/screenshots/guess-the-country-demo-2024-08-29_00.41.56.mp4)

## Notes for Shape Generator.

- While the shape generator script accurately generates most of the shape files. its not High Definition and shapes are not that clear for countries that are massive or spread across a wide area or water body. For Example. USA is weird at the moment. Russia is too stretched. Some small countries are just blobs. Island groups spread accross water are very small to see. 
- Ensure that you have an active internet connection if the shapefile needs to be downloaded.

## Notes for Game UI.

- I am not that good at Full Stack Development. My best option was to use Flask. Using IDX helped a lot with running Flask App but it's not perfect. 
- Feel free to use the project or add your improvements if you are a skilled Full Stack Dev.

## License for Code

This code is open-source and free to use under the MIT License. Modify and reuse as you wish.

## License for Shapefile Dataset
> World Bank Official Boundaries 
>
> Classification: Public
> 
> This dataset is classified as Public under the Access to Information Classification Policy. Users inside and outside the Bank can access this dataset. 
>
>License: Creative Commons Attribution 4.0
> 
> URL : https://datacatalog.worldbank.org/search/dataset/0038272/World-Bank-Official-Boundaries
>
