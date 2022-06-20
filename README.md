# scrapper-ironhack-v2
New version (a bit hacky) to scrap Ironhack Course Website 

Example of how to scrap Ironhack website - Only for student purposes

Obtain token from POST call at Ironhack's website after login 
(tip: use console of chrome, label Network and search "token") 

Create your own temario.json getting url
https://lms-api.ironhack.tech/YOURVERSION/courses/course-YOURVERSION:YOURCOURSE 
(im sure you will find the right way to get this JSON)

Put your temario.json inside the root folder, change "INSERT_BEARER_TOKEN" with your token (do not put Bearer word, i will do for you) and call python3 app.py

Ready! Bot is downloading all website with wait of 5 seconds between lessons (do not change it, DDOS is bad for kittys)
