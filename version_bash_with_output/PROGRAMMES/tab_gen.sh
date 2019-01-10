#!/bin/bash
#bash tab_gen.sh dossier_url fichier_html
#Génère un tableau dans une page html à partir d'un fichier d'urls

function tab_line() {
	echo -e '''		<tr>
		<td>'''$i'''</td>
		<td>'''$code_sortie'''</td>
		<td><a href="'''$ligne'''" target="_blank">'''$ligne'''</a></td>
		<td><a href="../PAGES-ASPIREES/'''$itab'''_'''$i'''.html" target="_blank">'''$itab'''_'''$i'''.html</a></td>
		<td>'''$ENCODAGE'''</td>
		<td><a target="_blank" href="../DUMP-TEXT/'''$itab'''_'''$i'''.txt">DUMP  n°'''$i'''</a></td>
	</tr>
	''';
}

function tab_line_file() {
	echo -e '''		<tr>
	<td>'''$i'''</td>
	<td>'''$code_sortie'''</td>
	<td><a href="'''$ligne'''" target="_blank">'''$ligne'''</a></td>
	<td><a href="../PAGES-ASPIREES/'''$itab'''_'''$i'''.html" target="_blank">'''$itab'''_'''$i'''.html</a></td>
	<td>'''$ENCODAGEFILE'''</td>
	<td><a target="_blank" href="../DUMP-TEXT/'''$itab'''_'''$i'''.txt">DUMP  n°'''$i'''</a></td>
		</tr>
	''';
}

echo -e '''<!DOCTYPE html>
<meta charset="UTF-8">

<html>

<head>
	<title>Tableau urls</title>
</head>

<body>

	''' > $2;

itab=1;

for fichier in $(ls $1)
	do
		i=1;
		echo -e '''<table border="2">
			<caption> Table n°'''$itab'''</caption>
			<tr>
				<th>n°</th>
				<th>Code Sortie</th>
				<th>URL</th>
				<th>Page aspirée</th>
				<th>Encodage</th>
				<th>DUMP initial</th>
			</tr>
	''' >> $2;

		for ligne in $(cat $1/$fichier)
		 	do
				code_sortie=$(curl -s -L -o tmp.txt -w "%{http_code}" $ligne | tail -1) ;
				if [[ $code_sortie == 200 ]]
					then
						curl -sL -o ./PAGES-ASPIREES/$itab\_$i.html $ligne;
						ENCODAGE=$(egrep -i "<meta +charset" ./PAGES-ASPIREES/$itab\_$i.html | egrep -o "charset *= *[^>]+" | cut -f2 -d"=" | egrep -o "(\w|\-)+" | uniq |tr "[a-z]" "[A-Z]") ;
						echo $itab - $i;
						echo $ligne;
						# echo -e "$itab::$i::$code_sortie::$ENCODAGE::$ligne";
						if [[ "$ENCODAGE" == "UTF-8" ]]
							then
								echo "Youpiiiii"
								lynx -dump -nolist $ligne > ./DUMP-TEXT/$itab\_$i.txt;
								tab_line >> $2;
						else
								echo -e "Pas de l'UTF-8?" ;
								if [[ "$ENCODAGE" == "" ]]
									then
										ENCODAGEFILE=$(file -i ./PAGES-ASPIREES/$itab\_$i.html | cut -d"=" -f2 | tr "[a-z]" "[A-Z]");
										if [[ "$ENCODAGEFILE" == "UTF-8" ]]
											then
												tab_line_file >> $2;
										else
											lynx -dump -nolist --assume-charset=$ENCODAGEFILE --display-charset=$ENCODAGEFILE $ligne > ./DUMP-TEXT/$itab\_$i.txt;
											iconv -f $ENCODAGEFILE -t "UTF-8" < ./DUMP-TEXT/$itab\_$i.txt > ./DUMP-TEXT/$itab\_$i.txt;
											tab_line_file >> $2;
										fi
								else
									code=$(iconv -l | egrep -i $ENCODAGE);
									if [[ "$code" != "" ]];
										then
											lynx -dump -nolist --assume-charset=$ENCODAGE --display-charset=$ENCODAGE $ligne > ./DUMP-TEXT/$itab\_$i.txt;
											iconv -f $ENCODAGE -t "UTF-8" < ./DUMP-TEXT/$itab\_$i.txt > ./DUMP-TEXTCONV/$itab\_$i.txt;
											tab_line >> $2;
									else
										ENCODAGEFILE=$(file -i ./PAGES-ASPIREES/$itab\_$i.html | cut -d"=" -f2 | tr "[a-z]" "[A-Z]");
										tab_line_file >> $2;
										if [[ "$ENCODAGEFILE" == "UTF-8" ]]
											then
												tab_line_file >> $2;
										fi
									fi
								fi
						fi

				else # URL "pourrie"
							echo '''<tr><td>$i</td><td>'''$code_sortie'''</td><td><a target="_blank" href="'''$ligne'''">'''$ligne'''</a></td><td>-</td><td>-</td><td>-</td></tr>''' >> $2 ;
						fi
				let i++;
				echo "-------------------------------------------------------------"
			done
		echo -e "</table>" >> $2;
		let itab++;
	done

echo -e '''</body>
</html>''' >> $2;
