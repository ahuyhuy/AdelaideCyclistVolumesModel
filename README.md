# Modelling Cyclist Volumes In Adelaide, South Australia

description here pls

# Setup guide



# Directory guide

`all-data/`: Contains census data, geo data for census data geographical regions (mesh blocks, destination zones), and cyclist count data

`bicycling-infrastructure-classification/`: A different repository for __Developing a bicycling infrastructure classification system for Greater Melbourne, Australia using OpenStreetMap__ by Debjit Bhowmick and Ben Beck. This work formed the basis of the bicycle infrastructure classification for this model. https://www.researchgate.net/publication/373296593_Developing_a_bicycling_infrastructure_classification_system_for_Greater_Melbourne_Australia_using_OpenStreetMap

`graph_generation/`: Python notebooks for the Greater Adelaide cycle network graph setup and graph loading. These notebooks combined create the graph network that can be used by any regression model.

`investigation/`: Earlier notebooks, test scripts, and models

`scripts/`: Shared code used in graph generation

# AI Usage

__NVIDIA Nemotron 3 Ultra (free)__ was the AI model used to assist with coding in python and managing the python environment. It was run __Deepseek Harness__ (see https://www.deepseek.com/en/harness/) - a locally run code harness that enables file read/write and maintains work context across sessions and models. Deepseek Harness was connected to the chosen model via __OpenRouter__, a service allowing users to connect harnesses such as copilot, claude code, cursor, and deepseek harness, to any available LLM model. This setup was primarily used for coding and technical support, not for design decisions or documentation.