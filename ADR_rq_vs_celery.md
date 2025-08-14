# ADR: RQ vs Celery

RQ a été choisi pour sa simplicité d'usage et une empreinte légère dans ce projet monolithique. Celery offre plus de fonctionnalités mais nécessite une configuration plus lourde (broker, backend, workers). RQ basé sur Redis suffit pour nos besoins de tâches courtes (emails, miniatures, analytics). La mise en place est rapide et la courbe d'apprentissage réduite.
