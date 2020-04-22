# SmartDataCollector

L'application est facile à utiliser. Il suffit de spécifier les critéres convoités comme
l’indique la figure suivante :

![alt text](https://imgur.com/RxXkVfD.png)

Aprés avoir saisie les profils recherchés , l’application commence le ’Scraping’ à l’aide de Selenium WebScraper. 
La première étape consiste à lister les profils LinkedIn vérifiant ces critéres
(Le nombre des profils affichés est réglable par l’application).


![alt text](https://imgur.com/oJMnk5W.png)

La deuxième étape consiste à collecter les données des profils sélectionnés (Name , Job , Entreprise , Skills ..) 
et les organiser dans un fichier de type CSV.

En une troisème phase ,et pour chaque profils trouvé , l’application essaye de collecter ses posts facebook et ses tweets ( à l’aide de tweepy et API Twitter ) et les combiner avec les données LinkedIn.

Finalement , l’application affiche le résultat sous forme de Json.

![alt text](https://imgur.com/EyBPCee.png)
