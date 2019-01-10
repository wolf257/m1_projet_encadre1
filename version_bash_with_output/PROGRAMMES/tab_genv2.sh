#!/bin/bash
#bash tab_gen.sh dossier_url fichier_html "motif"
#Génère un tableau dans une page html pour visualiser le résultat d'une chaîne de traitement
#aspiration d'une page web à partir d'un fichier text
#dump de la page
#conversion en utf-8 si besoin
#segmentation du texte si japonais
#création d'un index des mots avec le nombre d'occurences
#même chose que précédemment mais avec des bigrammes
#création d'un fichier txt contenant toutes les lignes contenant le motif
#traitement par minigrep
#donne le nombre d'occurences du motif
#création d'un corpus en concatenant tous les fichiers dump avec balisage

echo "Dossier d'URLs : $1 " ;
echo "Tableau : $2" ;
echo "Motif : $3" ;
echo "------------------------------------------------";
echo "------------------------------------------------";

source ./PROGRAMMES/fonctions.sh;

echo -e '''<!DOCTYPE html>
<meta charset="UTF-8">

<html>

<head>
	<link rel="stylesheet" type="text/css" href="tableau.css">
	<title>Tableau urls</title>
</head>

<body>

	''' > $2;

itab=1;

for fichier in $(ls $1)
	do
		i=1;
		if [[ "$fichier" == "urls_en.txt" ]]
			then
				langue="Anglais"
			elif [[ "$fichier" == "urls_fr.txt" ]]
				then
					langue="Français"
			elif [[ "$fichier" == "urls_jp.txt" ]]
				then
					langue="Japonais"
		fi
		echo -e '''<p></p>
		<h2>Langue n°'''$itab''' : '''$langue'''</h2>
		<table class="bordered">
			<tr>
				<th>n°</th>
				<th>Code Sortie</th>
				<th>URL</th>
				<th>Page aspirée</th>
				<th>Encodage</th>
				<th>DUMP initial</th>
				<th>DUMP UTF-8</th>
				<th>Index des mots</th>
				<th>Bigrammes</th>
				<th>Contexte UTF-8</th>
				<th>Contexte UTF-8 HTML</th>
				<th>Fréquence du motif</th>
			</tr>
	''' >> $2;

		for ligne in $(cat $1/$fichier)
		 	do
				code_sortie=$(curl -s -L -o tmp.txt -w "%{http_code}" $ligne | tail -1) ;
				echo $itab - $i;
				echo $ligne;
				if [[ $code_sortie == 200 ]]
					then
						curl -sL -o ./PAGES-ASPIREES/$itab\_$i.html $ligne;
						ENCODAGE=$(getencoding ./PAGES-ASPIREES/$itab\_$i.html);
						if [[ "$ENCODAGE" == "BINARY" ]]
						 then
							ENCODAGE="UTF-8";
						fi
						echo $ENCODAGE;
						if [[ "$ENCODAGE" == "UTF-8" ]]
							then
								echo "Youpiiiii \o/"
								#on dump la page
								lynx -dump -nolist $ligne > ./DUMP-TEXT/$itab\_$i.txt;
								#si la page est en japonais, on segmente le texte
								tokenizer;
								#on fait l'index des mots
								indexmots < ./DUMP-TEXT/$itab\_$i.txt > INDEX/$itab\_$i.txt;
								#on fait les bigrams
								bigrams;
								#on fait une liste simple de toutes les lignes contenant le motif
								egrep -i $3 ./DUMP-TEXT/$itab\_$i.txt > ./CONTEXTES/$itab\_$i.txt ;
								#on prépare un corpus en rassemblant tous les fichiers dump dans un seul fichier avec des balises
								concat;
								#on compte les occurences du motif
								nbmotif=$(egrep -coi $3 ./DUMP-TEXT/$itab\_$i.txt);
								#on lance minigrep
								minigrep;
								#on génère le code html correspondant à une ligne dans le tableau
								tab_line >> $2;
						else
								echo -e "Pas de l'UTF-8?" ;
								if [[ "$ENCODAGE" == "" ]]
									then
										echo "ENCODAGE est vide";
										ENCODAGEFILE=$(file -i ./PAGES-ASPIREES/$itab\_$i.html | cut -d"=" -f2 | tr "[a-z]" "[A-Z]");
										if [[ "$ENCODAGEFILE" == "UTF-8" ]]
											then
												echo "ENCODAGEFILE = UTF-8";
												lynx -dump -nolist $ligne > ./DUMP-TEXT/$itab\_$i.txt;
												tokenizer;
												indexmots < ./DUMP-TEXT/$itab\_$i.txt > INDEX/$itab\_$i.txt;
												bigrams;
												egrep -i $3 ./DUMP-TEXT/$itab\_$i.txt > ./CONTEXTES/$itab\_$i.txt ;
												concat;
												nbmotif=$(egrep -coi $3 ./DUMP-TEXT/$itab\_$i.txt);
												minigrep;
												tab_line_file >> $2;
										else
											echo "ENCODAGEFILE pas de l'utf-8";
											lynx -dump -nolist --assume-charset=$ENCODAGEFILE --display-charset=$ENCODAGEFILE $ligne > ./DUMP-TEXT/$itab\_$i.txt;
											iconv -f $ENCODAGEFILE -t "UTF-8" < ./DUMP-TEXT/$itab\_$i.txt > ./DUMP-TEXTCONV/$itab\_$i.txt;
											tokenizerconv;
											indexmots < ./DUMP-TEXT/$itab\_$i.txt > INDEX/$itab\_$i.txt;
											bigramsconv;
											egrep -i $3 ./DUMP-TEXTCONV/$itab\_$i.txt > ./CONTEXTES/$itab\_$i.txt ;
											concatconv;
											nbmotif=$(egrep -coi $3 ./DUMP-TEXT/$itab\_$i.txt);
											minigrepconv;
											tab_line_file >> $2;
										fi
								else
									echo "ENCODAGE pas utf-8 mais pas vide"
									code=$(iconv -l | egrep -i $ENCODAGE);
									if [[ "$code" != "" ]];
										then
											echo "encodage valide donc conversion";
											lynx -dump -nolist --assume-charset=$ENCODAGE --display-charset=$ENCODAGE $ligne > ./DUMP-TEXT/$itab\_$i.txt;
											iconv -f $ENCODAGE -t "UTF-8" < ./DUMP-TEXT/$itab\_$i.txt > ./DUMP-TEXTCONV/$itab\_$i.txt;
											tokenizerconv;
											indexmots < ./DUMP-TEXT/$itab\_$i.txt > INDEX/$itab\_$i.txt;
											bigramsconv;
											egrep -i $3 ./DUMP-TEXTCONV/$itab\_$i.txt > ./CONTEXTES/$itab\_$i.txt ;
											concatconv;
											nbmotif=$(egrep -coi $3 ./DUMP-TEXT/$itab\_$i.txt);
											minigrepconv;
											tab_line >> $2;
									else
										echo "encodage non valide, passage à encodagefile"
										ENCODAGEFILE=$(file -i ./PAGES-ASPIREES/$itab\_$i.html | cut -d"=" -f2 | tr "[a-z]" "[A-Z]");
										if [[ "$ENCODAGEFILE" == "UTF-8" ]]
											then
												echo "encodagefile = utf-8";
												lynx -dump -nolist $ligne > ./DUMP-TEXT/$itab\_$i.txt;
												tokenizer;
												indexmots < ./DUMP-TEXT/$itab\_$i.txt > INDEX/$itab\_$i.txt;
												bigrams;
												egrep -i $3 ./DUMP-TEXT/$itab\_$i.txt > ./CONTEXTES/$itab\_$i.txt ;
												concat;
												nbmotif=$(egrep -coi $3 ./DUMP-TEXT/$itab\_$i.txt);
												minigrep;
												tab_line_file >> $2;
										else
											echo "ENCODAGEFILE pas de l'utf-8";
											lynx -dump -nolist --assume-charset=$ENCODAGEFILE --display-charset=$ENCODAGEFILE $ligne > ./DUMP-TEXT/$itab\_$i.txt;
											iconv -f $ENCODAGEFILE -t "UTF-8" < ./DUMP-TEXT/$itab\_$i.txt > ./DUMP-TEXTCONV/$itab\_$i.txt;
											tokenizerconv;
											indexmots < ./DUMP-TEXT/$itab\_$i.txt > INDEX/$itab\_$i.txt;
											bigramsconv;
											egrep -i $3 ./DUMP-TEXTCONV/$itab\_$i.txt > ./CONTEXTES/$itab\_$i.txt ;
											concatconv;
											nbmotif=$(egrep -coi $3 ./DUMP-TEXT/$itab\_$i.txt);
											minigrepconv;
											tab_line_file >> $2;
										fi
									fi
								fi
						fi

				else # URL "pourrie"
							echo "URL pourri désolée ¯\_(ツ)_/¯"
							tab_linevide >> $2
						fi
				let i++;
				rm tmp.txt;
				echo "-------------------------------------------------------------";
			done
		echo -e "</table>" >> $2;
		let itab++;
	done
echo -e '''</body>
</html>''' >> $2

#extraction et comptages pour mettre en évidence les formes passsives et actives
bash ./PROGRAMMES/grep.sh
