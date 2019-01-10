# dans fichier.

grep -Eno "(\w+ )?(\w+ )?(abused|raped)( \w+)?" ./CONTEXTES/contextesconcat1.txt |
cut -d: -f3 > ./CONTEXTES/extraction/en_1.txt

grep -Eno "(\w+ )?(\w+ )?(violée?|agressée?)( \w+)?" ./CONTEXTES/contextesconcat2.txt |
cut -d: -f3 > ./CONTEXTES/extraction/fr_1.txt

grep -Eno "([^ ]+ )?([^ ]+ )?(レイプ?|強姦?)( [^ ]+)?" ./CONTEXTES/contextesconcat3.txt | cut -d: -f2 > ./CONTEXTES/extraction/jp_1.txt

# un mot par ligne

grep -Eo "\w+" ./CONTEXTES/extraction/fr_1.txt > ./CONTEXTES/extraction/fr_2.txt

grep -Eo "\w+" ./CONTEXTES/extraction/en_1.txt > ./CONTEXTES/extraction/en_2.txt

grep -Eo "[^ ]+" ./CONTEXTES/extraction/jp_1.txt > ./CONTEXTES/extraction/jp_2.txt

# tagger

tree-tagger-french ./CONTEXTES/extraction/fr_2.txt > ./CONTEXTES/extraction/fr_3.txt

tree-tagger-english ./CONTEXTES/extraction/en_2.txt > ./CONTEXTES/extraction/en_3.txt

# classement

cut -f3 ./CONTEXTES/extraction/en_3.txt | sort | uniq -c | sort -r > ./CONTEXTES/extraction/en_4.txt

cut -f3 ./CONTEXTES/extraction/fr_3.txt | sort | uniq -c | sort -r > ./CONTEXTES/extraction/fr_4.txt

cut -f3 ./CONTEXTES/extraction/jp_2.txt | sort | uniq -c | sort -r > ./CONTEXTES/extraction/jp_3.txt
