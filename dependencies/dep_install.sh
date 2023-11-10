
#!/bin/bash

if [ -d $PWD/centrale_p ]; then
	echo "centrale_p already exists"
	exit 1
else
	sudo pip3.11 install python3.11-dev python3.11-venv
	python3.11 -m venv $PWD/centrale_p
fi

source centrale_p/bin/activate
pip3.11 install pandas \
				numpy \
				scikit-learn \
				pyspark \
				matplotlib \
				jupyter
# mettez les librairie que vous voulez installer les potos
ipython kernel install --user --name=centrale_p

# Pour activer l'env virtuel : source centrale_p/bin/activate
# Pour désactiver l'env virtuel : deactivate
# Si pas sur linux : normalement ca marche sans sudo si python est déjà installé
# retirer 3.11 si vous avez une ancienne version de python
