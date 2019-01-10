#!/bin/bash

#génère la ligne du tableau après le traitement complet de la page web, pour le cas où la fonction getencoding a fonctionné
function tab_line() {
	echo -e '''		<tr>
		<td>'''$i'''</td>
		<td>'''$code_sortie'''</td>
		<td><a href="'''$ligne'''" target="_blank">'''$ligne'''</a></td>
		<td><a href="../PAGES-ASPIREES/'''$itab'''_'''$i'''.html" target="_blank">'''$itab'''_'''$i'''.html</a></td>
		<td>'''$ENCODAGE'''</td>''';
		if [[ "$ENCODAGE" == "UTF-8" ]]
		then
			echo -e '''<td>-</td>''';
			echo -e '''<td><a target="_blank" href="../DUMP-TEXT/'''$itab'''_'''$i'''.txt">'''$itab'''_'''$i'''</a></td>''';
		else
			echo -e '''<td><a target="_blank" href="../DUMP-TEXT/'''$itab'''_'''$i'''.txt">'''$itab'''_'''$i'''</a></td>''';
			echo -e '''<td><a target="_blank" href="../DUMP-TEXTCONV/'''$itab'''_'''$i'''.txt">'''$itab'''_'''$i'''</a></td>''';
		fi
		echo -e '''	<td><a target="_blank" href="../INDEX/'''$itab'''_'''$i'''.txt">'''$itab'''_'''$i'''</a></td>
			<td><a target="_blank" href="../BIGRAMS/'''$itab'''_'''$i'''.txt">'''$itab'''_'''$i'''</a></td>
			<td><a target="_blank" href="../CONTEXTES/'''$itab'''_'''$i'''.txt">'''$itab'''_'''$i'''</a></td>
			<td><a target="_blank" href="../CONTEXTESMINI/'''$itab'''_'''$i'''.html">'''$itab'''_'''$i'''</a></td>
			<td>'''$nbmotif'''</td>''';
	echo -e '''</tr>
	''';
}

#génère la ligne de tableau après le traitement complet de la page
#dans le cas où on a dû passer par la commande file pour récupérer l'encodage
function tab_line_file() {
	echo -e '''		<tr>
		<td>'''$i'''</td>
		<td>'''$code_sortie'''</td>
		<td><a href="'''$ligne'''" target="_blank">'''$ligne'''</a></td>
		<td><a href="../PAGES-ASPIREES/'''$itab'''_'''$i'''.html" target="_blank">'''$itab'''_'''$i'''.html</a></td>
		<td>'''$ENCODAGEFILE'''</td>''';
		if [[ "$ENCODAGEFILE" == "UTF-8" ]]
		then
			echo -e '''<td>-</td>''';
			echo -e '''<td><a target="_blank" href="../DUMP-TEXT/'''$itab'''_'''$i'''.txt">'''$itab'''_'''$i'''</a></td>''';
		else
			echo -e '''<td><a target="_blank" href="../DUMP-TEXT/'''$itab'''_'''$i'''.txt">'''$itab'''_'''$i'''</a></td>''';
			echo -e '''<td><a target="_blank" href="../DUMP-TEXTCONV/'''$itab'''_'''$i'''.txt">'''$itab'''_'''$i'''</a></td>''';
		fi
		echo -e '''	<td><a target="_blank" href="../INDEX/'''$itab'''_'''$i'''.txt">'''$itab'''_'''$i'''</a></td>
			<td><a target="_blank" href="../BIGRAMS/'''$itab'''_'''$i'''.txt">'''$itab'''_'''$i'''</a></td>
			<td><a target="_blank" href="../CONTEXTES/'''$itab'''_'''$i'''.txt">'''$itab'''_'''$i'''</a></td>
			<td><a target="_blank" href="../CONTEXTESMINI/'''$itab'''_'''$i'''.html">'''$itab'''_'''$i'''</a></td>
			<td>'''$nbmotif'''</td>''';
	echo -e '''</tr>
	''';
}

#génère la ligne de tableau pour le cas où l'url est pourri
function tab_linevide() {
	echo -e '''		<tr>
		<td>'''$i'''</td>
		<td>'''$code_sortie'''</td>
		<td><a href="'''$ligne'''" target="_blank">'''$ligne'''</a></td>
		<td>-</td>
		<td>'''-'''</td>
		<td>-</td>
		<td>-</td>
		<td>-</td>
		<td>-</td>
		<td>-</td>
		<td>-</td>
		<td>-</td>
	</tr>
	''';
}

#récupère l'encodage de la page html via l'en-tête de la page
function getencoding() {
	egrep -i "<meta +charset" $1 | egrep -o "charset *= *[^>]+" | cut -f2 -d"=" | egrep -o "(\w|\-)+" | uniq |tr "[a-z]" "[A-Z]"
}

#dans le cas où la page récupérée était en utf-8
#écrit dans deux fichiers txt, l'un contient tous les dump des pages entre balises; l'autre contient tous les contextes entre balises
function concat() {
	echo -e '''<fichier id="'''$itab'''_'''$i'''">\n''' >> ./DUMP-TEXT/dumpconcat.txt;
	echo -e '''<fichier id="'''$itab'''_'''$i'''">\n''' >> ./DUMP-TEXT/dumpconcat$itab.txt;
	cat ./DUMP-TEXT/$itab\_$i.txt >> ./DUMP-TEXT/dumpconcat.txt;
	cat ./DUMP-TEXT/$itab\_$i.txt >> ./DUMP-TEXT/dumpconcat$itab.txt;
	echo -e '''\n</fichier>\n\n''' >> ./DUMP-TEXT/dumpconcat.txt;
	echo -e '''\n</fichier>\n\n''' >> ./DUMP-TEXT/dumpconcat$itab.txt;
	echo -e '''<fichier id="'''$itab'''_'''$i'''">\n''' >> ./CONTEXTES/contextesconcat.txt;
	echo -e '''<fichier id="'''$itab'''_'''$i'''">\n''' >> ./CONTEXTES/contextesconcat$itab.txt;
	cat ./CONTEXTES/$itab\_$i.txt >> ./CONTEXTES/contextesconcat.txt;
	cat ./CONTEXTES/$itab\_$i.txt >> ./CONTEXTES/contextesconcat$itab.txt;
	echo -e '''\n</fichier>\n\n''' >> ./CONTEXTES/contextesconcat.txt;
	echo -e '''\n</fichier>\n\n''' >> ./CONTEXTES/contextesconcat$itab.txt;
}

#dans le cas où la page récupérée n'était pas en utf-8
#écrit dans deux fichiers txt, l'un contient tous les dump des pages entre balises; l'autre contient tous les contextes entre balises
function concatconv() {
	echo -e '''<fichier id="'''$itab'''_'''$i'''">\n''' >> ./DUMP-TEXT/dumpconcat.txt;
	echo -e '''<fichier id="'''$itab'''_'''$i'''">\n''' >> ./DUMP-TEXT/dumpconcat$itab.txt;
	cat ./DUMP-TEXTCONV/$itab\_$i.txt >> ./DUMP-TEXT/dumpconcat.txt;
	cat ./DUMP-TEXTCONV/$itab\_$i.txt >> ./DUMP-TEXT/dumpconcat$itab.txt;
	echo -e '''\n</fichier>\n\n''' >> ./DUMP-TEXT/dumpconcat.txt;
	echo -e '''\n</fichier>\n\n''' >> ./DUMP-TEXT/dumpconcat$itab.txt;
	echo -e '''<fichier id="'''$itab'''_'''$i'''">\n''' >> ./CONTEXTES/contextesconcat.txt;
	echo -e '''<fichier id="'''$itab'''_'''$i'''">\n''' >> ./CONTEXTES/contextesconcat$itab.txt;
	cat ./CONTEXTES/$itab\_$i.txt >> ./CONTEXTES/contextesconcat.txt;
	cat ./CONTEXTES/$itab\_$i.txt >> ./CONTEXTES/contextesconcat$itab.txt;
	echo -e '''\n</fichier>\n\n''' >> ./CONTEXTES/contextesconcat.txt;
	echo -e '''\n</fichier>\n\n''' >> ./CONTEXTES/contextesconcat$itab.txt;
}

#page en utf-8
#lance minigrep
function minigrep() {
	perl5.16.3.exe ./PROGRAMMES/minigrep/minigrepmultilingue.pl "UTF-8" ./DUMP-TEXT/$itab\_$i.txt ./PROGRAMMES/motif.txt;
	mv resultat-extraction.html ./CONTEXTESMINI;
	mv ./CONTEXTESMINI/resultat-extraction.html ./CONTEXTESMINI/$itab\_$i.html;
}

#page pas en utf-8
#lance minigrep
function minigrepconv() {
	perl5.16.3.exe ./PROGRAMMES/minigrep/minigrepmultilingue.pl "UTF-8" ./DUMP-TEXTCONV/$itab\_$i.txt ./PROGRAMMES/motif.txt;
	mv resultat-extraction.html ./CONTEXTESMINI;
	mv ./CONTEXTESMINI/resultat-extraction.html ./CONTEXTESMINI/$itab\_$i.html;
}

#crée un index des mots
function indexmots() {
	egrep -o "\w+" | sort | uniq -c | sort -r | less;
}

#crée un index de bigrammes à partir du dump d'une page utf-8
function bigrams() {
	egrep -o "\w+" ./DUMP-TEXT/$itab\_$i.txt > tmp1.txt;
	egrep -o "\w+" ./DUMP-TEXT/$itab\_$i.txt | tail -n+2 > tmp2.txt;
	paste tmp1.txt tmp2.txt | sort | uniq -c | sort -r | less > ./BIGRAMS/$itab\_$i.txt;
	rm tmp1.txt;
	rm tmp2.txt;
}

#crée un index de bigrammes à partir du dump d'une page qui n'était pas en utf-8
function bigramsconv() {
	egrep -o "\w+" ./DUMP-TEXTCONV/$itab\_$i.txt > tmp1.txt;
	egrep -o "\w+" ./DUMP-TEXTCONV/$itab\_$i.txt | tail -n+2 > tmp2.txt;
	paste tmp1.txt tmp2.txt | sort | uniq -c | sort -r | less > ./BIGRAMS/$itab\_$i.txt;
	rm tmp1.txt;
	rm tmp2.txt;
}

#lance le script python permettant de segmenter le texte des pages en japonais en utf-8
function tokenizer() {
	if [[ "$fichier" == "urls_jp.txt" ]] #on ne veut traiter que les urls japonais
		then
			cp ./DUMP-TEXT/$itab\_$i.txt ./DUMP-PRETOKEN/$itab\_$i.txt;
			python3 ./PROGRAMMES/tokenizer.py ./DUMP-PRETOKEN/$itab\_$i.txt ./DUMP-TEXT/$itab\_$i.txt;
	fi
}

#le tokenizer n'acceptant que les documents en UTF-8, il faut prévoir
#le cas où le fichier à utiliser est celui créé après conversion en UTF-8
function tokenizerconv() {
	if [[ "$fichier" == "urls_jp.txt" ]]
 		then
			cp ./DUMP-TEXTCONV/$itab\_$i.txt ./DUMP-PRETOKEN/$itab\_$i.txt;
 			python3 ./PROGRAMMES/tokenizer.py ./DUMP-PRETOKEN/$itab\_$i.txt ./DUMP-TEXTCONV/$itab\_$i.txt;
	fi
}
