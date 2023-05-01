# Pokemon Q Learning Monte Carlo Agent
This is the code for the project titled 'Combining Reinforcement Learning and Monte Carlo Search Algorithms for Pokémon Battling' by Christopher Davis.

## Usage
This project uses Python and the Poke-env module which can be installed using a package manager like Pip.
The battle simulation is done using Pokemon Showdown. The majority of simulating is done using a local installation of Pokemon Showdown whilst the testLadder.py file uses the primary Pokemon Showdown server at https://play.pokemonshowdown.com/ 
Instructions for setting up Pokemon Showdown can be found in the documentaion of the Poke-env module found here: https://poke-env.readthedocs.io/en/stable/index.html under the gettig started category.
Once a local instance of Pokemon Showdown is running, the files data_collection_rr.py, data_collection.py, testChallengeMe, and testCrossEvaluation can be used to simulate battles.
Agent type and other parameters are all hardcoded in the files, so opening the files to configure them should be done before running as the files may not work before configured.
test

## Knowledge Base
The Q learning and all Hybrid agents require a knowledge base file to be present. The QLearningAgent requires a KB.json while the others use KBLite.json The only knowledge base file supplied is the KBLiteDemo.json which contains observations. To use this file, make a copy called KBLite.json. To reset the KB file to empty, or to generate a new one, use the resetKB or resetLiteKB files for the respective knowledge base

## Results
The data_collection files write results to the file results/results.txt.
format_results.py can be used to format the results into a JSON file.
results.ipynb uses the formatted results to produce graphs of performance metrics.
The QLite agent records updated Q values in the qvaluetracking/QLite.txt file which is also used in the results notebook