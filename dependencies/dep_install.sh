
#!/bin/bash


# A lancer avec source dep_install.sh
# Si vous avez déjà un env virtuel, il ne sera pas réinstallé
# Si vous voulez réinstaller l'env virtuel, supprimez le dossier centrale_p

if [ -d $PWD/centrale_p ]; then
	echo "centrale_p already exists"
else
	sudo pip install python3.11-dev python3.11-venv
	python3.11 -m venv $PWD/centrale_p
	pip3.11 install pandas \
				numpy \
				scikit-learn \
				openpyxl \
				plotlib \
				matplotlib \
				jupyter
	# mettez les librairie que vous voulez installer les potos
	source $PWD/centrale_p/bin/activate
	ipython kernel install --user --name=centrale_p
	exit 0
fi
source $PWD/centrale_p/bin/activate
pip install pandas \
				openpyxl \
				numpy \
				scikit-learn \
				plotly \
				matplotlib \
				jupyter


# Pour activer l'env virtuel : source centrale_p/bin/activate
# Pour désactiver l'env virtuel : deactivate
# Si pas sur linux : normalement ca marche sans sudo si python est déjà installé
# retirer 3.11 si vous avez une ancienne version de python
