# Annotationrichtlinien für Historische Regesten

## Allgemeine Prinzipien

### 1. Ziel und Umfang der Annotation:

Die Annotation von Regesten dient der strukturierten Erfassung relevanter Entitäten zur besseren Analyse und maschinellen Verarbeitung.  
Annotiert werden all jene Begriffe bzw. Konzepte, für die sich ein Forschungsinteresse in der wissenschaftlichen Literatur nachweisen lässt. Neben der Forschungsliteratur berücksichtigen wir ebenfalls die Ergebnisse einer von uns in der historischen Forschungsgemeinschaft durchgeführten Umfrage zu früheren, aktuellen und geplanten Forschungsvorhaben mit Bezug zum Repertorium Germanicum.   
Nicht getaggte Inhalte können dennoch durch KI-gestützte Verfahren erfasst werden. Annotiert werden ausschließlich Begriffe, die explizit im Regesttext vorkommen – Begriffe, die nur implizit mitgedacht werden müssen, z.B. (prov.) de eccl., bleiben unberücksichtigt.  
Abkürzungspunkte und Endpunkte nach der Quellenangabe, sind Teil der Annotation und werden entsprechend mit ausgezeichnet.      

### 2. Kategorien:

Die Annotation erfolgt derzeit anhand einer Vielzahl von **basalen Kategorien**, also kleinster logisch abgrenzbarer Einheiten im Regesttext. Diese basalen Kategorien bilden die Grundlage der Auszeichnung.
Behelfsmäßig sind diese Basiskategorien in vier übergeordnete Kategorien gruppiert: Person, Vita, Event und Varia. Diese dienen der besseren Übersichtlichkeit und Navigation innerhalb der Guidelines.
Perspektivisch werden diese übergeordneten Kategorien durch andere/weitere **semantische Kategorien** ersetzt bzw. ergänzt. Semantische Kategorien entstehen aus der Kombination mehrerer basaler Kategorien. Ein und dieselbe basale Einheit kann dabei mehreren semantischen Kategorien zugeordnet werden. Die semantischen Kategorien befinden sich aktuell im Aufbau und werden schrittweise in die Guidelines integriert.

### 3. Darstellung im Guidelines-Dokument:

Der Fettdruck kennzeichnet, welche Wörter mit dem Kategorielabel getaggt werden sollen und welche nicht.    

## Strukturierung der Labels und Beispiele

Jede Kategorie (Person, Vita, Event, Varia) enthält eine Liste von Labels (Unterkategorien). Für jedes Label werden "Standardbeispiele" (Standard Examples) und "Sonstige Beispiele" (Other Examples) aufgeführt. Jedes Beispiel umfasst den Kontext und das zu annotierende Textfragment, wobei das Fragment in doppelten Sternchen (`**`) eingeschlossen ist. Die erwartete Annotation wird im Format `[Type: Value]` angegeben. Bei Beispielen, die mehrere Annotationen ergeben, werden alle aufgeführt.

### Kategorie: Person

Bei der Annotation von Personen unterscheiden wir vier Unterkategorien:

#### Label: Vorname

##### Standard Examples:

* Text: **Henricus** de Bocholdia    
  Annotation: [Type: Vorname, Value: "Henricus"]
* Text: **Floora** relicta Magni Bootes armig.  
  Annotation: [Type: Vorname, Value: "Floora"] 

#### Label: Namenszusatz

##### Standard Examples:

* Text: Nachname/Beiname: Achacius **Berolczhaimer**  
  Annotation: [Type: Namenszusatz, Value: "Berolczhaimer"]
* Text: lokale Herkunft / Adelsprädikat: Henricus **de Bocholdia**  
  Annotation: [Type: Namenszusatz, Value: "de Bocholdia"]  
* Text: Alternative Namensformen: Bertholdus **Schomaker al. dictus Dives** 
  Annotation: [Type: Namenszusatz, Value: "Schomaker al. dictus Dives"]
* Text: Alternative Namensformen: Bertholdus **Denen (Deynen) de Wildunghen**  
  Annotation: [Type: Namenszusatz, Value: "Denen (Deynen) de Wildunghen"]
* Text: Alternative Namensformen: Fridericum **Baecht iuniorem**  
  Annotation: [Type: Namenszusatz, Value: "Baecht iuniorem"]
* Text: Alternative Namensformen: **Florentin. nunc.**  
  Annotation: [Type: Namenszusatz, Value: "Florentin. nunc."]

##### Other Examples:
* Text: castrum **das Newhaus nunc.** 
  Annotation: [Type: Namenszusatz, Value: "das Newhaus nunc."]

##### Hinweis 
Namenszusätze können sowohl für
Explizit nicht als Namenszusatz gelten kirchliche Ämter (Albertus **el. Ratisp.** /Angelus **abb. mon. in Runa**), weltliche Ämter (Antonius **dux Brabantie**), Identifikation über eine andere Person (Alexander **nob. viri Semonithi ducis Masouie** natus).

#### Label: PersonImplizit

##### Standard Examples:

* Text: cum **30 pers.** de confess. elig.  
  Annotation: [Type: PersonImplizit, Value: "30 pers."]

#### Label: Papst

##### Beschreibung:
Die Namen der Päpste kommen auch dekliniert vor, z.B. "Bonifatio VIII" statt "Bonifatius VIII"; ebenso: "pape" statt "papa". Achtung: Nicht als Papst getaggt werden Patrozinien, die ohne die Ordinalzahl (z.B. VIII) oder den Zusatz "papa" vorkommen, z.B.: Bonifatii in dem Kontext "eccl. s. Bonifatii Halberstad.".

##### Standard Examples:

* Text: **Bonifatius IX.**  
  Annotation: [Type: Papst, Value: "Bonifatius IX."]
* Text: **papa**  
  Annotation: [Type: Papst, Value: "papa"]
  * **Häufigkeit:** 480x in den Bänden 1-9, pape: 5307x in den Bänden 1-9.
* Text: **Bonifatio VIII papa**  
  Annotation: [Type: Papst, Value: "Bonifatio VIII papa"]  

### Kategorie: Vita

#### Label: Verwandtschaft

##### Beschreibung:
In den Regesten wird für viele Personen eine Verwandtschaftbeziehung angegeben. Die unter den Examples gelisteten Beispiele können auch dekliniert vorkommen. Die deklinierten Formen sollen ebenfalls das Label "Verwandtschaft" erhalten, z.B. uxoris statt uxor.

##### Standard Examples:

* Text: Albertus de Smolsco presb. Wladislav. dioc. **nepos** aep. Gneznen.  
  Annotation: [Type: Verwandtschaft, Value: "nepos"]
  * **Häufigkeit:** 403x in den Bänden 1-9
* Text: **ux.**  
  Annotation: [Type: Verwandtschaft, Value: "ux."]
  * **Häufigkeit:** 1878x in den Bänden 1-2 und 5-9
* Text: **genitor**  
  Annotation: [Type: Verwandtschaft, Value: "genitor"]

##### Other Examples:

* Text: **uxor**  
  Annotation: [Type: Verwandtschaft, Value: "uxor"]
  * **Häufigkeit:** 936x in den Bänden 1-5 und 9
* Text: **filius**  
  Annotation: [Type: Verwandtschaft, Value: "filius"]
* Text: **filia**  
  Annotation: [Type: Verwandtschaft, Value: "filia"]
* Text: **pater**  
  Annotation: [Type: Verwandtschaft, Value: "pater"]
* Text: **frater**  
  Annotation: [Type: Verwandtschaft, Value: "frater"]
* Text: **relicta**  
  Annotation: [Type: Verwandtschaft, Value: "relicta"]
* Text: (unknown) **natus** (unknown)
  Annotation: [Type: Verwandtschaft, Value: "natus"]
  * **Hinweis:** (unknown) steht hier als Platzhalter für den Namen des Vaters, z.B. "Bernhardus natus Johannis Berlin", wobei Johannes Berlin der Vater von Bernhardus ist. Oder: "Alexander nob. viri Semonithi ducis Masouie natus", wobei Semonithus der Vater des Alexander ist.
* Text: **consanguineus**  
  Annotation: [Type: Verwandtschaft, Value: "consanguineus"]

#### Label: Familiar

##### Standard Examples:

* Text: **fam.** Antonii ep. Portuen. card.  
  Annotation: [Type: Familiar, Value: "fam."]
* Text: **acolit.** pape  
  Annotation: [Type: Familiar, Value: "acolit."]

##### Other Examples:

* Text: **parafrenarius** pape  
  Annotation: [Type: Familiar, Value: "parafrenarius pape"]
* Text: **(unknown)** pape
  Annotation: [Type: Familiar, Value: "(unknown)"]
  * **Hinweis:** Neben den oben genannten Beispielen "acolit. pape" und "parafrenarius pape" kann es noch weitere Ämter geben, die im direkten Umfeld des Papstes ausgeübt werden. Diese kirchlichen Ämter, die im Regest durch die direkte Nähe zum Wort "pape" gekennzeichnet sind, werden hier durch den Platzhalter (unknown) bezeichnet. Dieser Platzhalter soll ebenfalls das Label "Familiar" bekommen. Wieder entfernt aus der Kategorie "Familiar" haben wir Fälle wie "cap. ap. sed." oder "script. litt. ap.", da es sich bei ihnen zwar um Bedienstete der Kurie,  nicht aber zwangsläufig um Familiare handelt.

#### Label: SozialerStand

##### Standard Examples:

* Text: **de nob. gen.**  
  Annotation: [Type: SozialerStand, Value: "de nob. gen."]
* Text: **nob. viri xxx**  
  Annotation: [Type: SozialerStand, Value: "nob. viri xxx"]
* Text: **de bar.**  
  Annotation: [Type: SozialerStand, Value: "de bar."]

##### Other Examples:

* Text: **baron. gen.**  
  Annotation: [Type: SozialerStand, Value: "baron. gen."]
* Text: **de com. gen.**  
  Annotation: [Type: SozialerStand, Value: "de com. gen."]
* Text: **de mil.**  
  Annotation: [Type: SozialerStand, Value: "de mil."]
* Text: **milit. gen.**  
  Annotation: [Type: SozialerStand, Value: "milit. gen."]  
* Text: **de ducum et com. gen.**  
  Annotation: [Type: SozialerStand, Value: "de ducum et com. gen."]
* Text: **de comit. gen.**  
  Annotation: [Type: SozialerStand, Value: "de comit. gen."]
* Text: **de ducum et comit. gen.**  
  Annotation: [Type: SozialerStand, Value: "de ducum et comit. gen."]
* Text: **de ducum et marchionum gen.**  
  Annotation: [Type: SozialerStand, Value: "de ducum et marchionum gen."]
* Text: **de ducis** natus  
  Annotation: [Type: SozialerStand, Value: "de ducis"]
* Text: **nob.**  
  Annotation: [Type: SozialerStand, Value: "nob."]
* Text: **mul.**  
  Annotation: [Type: SozialerStand, Value: "mulier"]
* Text: **mulier**  
  Annotation: [Type: SozialerStand, Value: "mulier"]
* Text: **armig.**  
  Annotation: [Type: SozialerStand, Value: "armig."]
* Text: **mil.**  
  Annotation: [Type: SozialerStand, Value: "mil."]
* Text: **civ.**  
  Annotation: [Type: SozialerStand, Value: "civ."]
* Text: **civis**  
  Annotation: [Type: SozialerStand, Value: "civis"]
* Text: **domic.**  
  Annotation: [Type: SozialerStand, Value: "domic."]
  * **Hinweis:** s. Notiz unten.   
* Text: **de milit. gen.**  
  Annotation: [Type: SozialerStand, Value: "de milit. gen."]
* Text: **opid.**  
  Annotation: [Type: SozialerStand, Value: "opid."]
* Text: **bar.**  
  Annotation: [Type: SozialerStand, Value: "bar."]
  * **Hinweis:** Wenn kein Herrschaftsgebiet genannt wird; vgl. WeltlichesAmt.
* Text: **com.**  
  Annotation: [Type: SozialerStand, Value: "com."]
  * **Hinweis:** Wenn kein Herrschaftsgebiet genannt wird; vgl. WeltlichesAmt.
* Text: **comes**  
  Annotation: [Type: SozialerStand, Value: "comes"]
  * **Hinweis:** Wenn kein Herrschaftsgebiet genannt wird; vgl. WeltlichesAmt.
* Text: **dux**  
  Annotation: [Type: SozialerStand, Value: "dux"]
  * **Hinweis:** Wenn kein Herrschaftsgebiet genannt wird; vgl. WeltlichesAmt.
* Text: **mercator**  
  Annotation: [Type: SozialerStand, Value: "mercator"]
* Text: **incola**  
  Annotation: [Type: SozialerStand, Value: "incola"] 

#### Label: KirchlicherStand

##### Beschreibung:
Der kirchliche Stand ergibt sich aus dem Empfang der niederen Weihen (Lektor, Akoluth, Subdiakon etc.) und der höheren Weihen (Diakonat, Presbyterat, Episkopat); er schlägt sich auch in der generellen Unterscheidung zwischen Laien und Klerikern nieder (laic. = Laie; cler. = Kleriker).

##### Standard Examples:

* Text: **presb.**  
  Annotation: [Type: KirchlicherStand, Value: "presb."]
  * **Hinweis:** vgl. KirchlichesAmt
* Text: **laic.**  
  Annotation: [Type: KirchlicherStand, Value: "laic."]
* Text: **in minore ord. constit.**  
  Annotation: [Type: KirchlicherStand, Value: "in minore ord. constit."]

##### Other Examples:

* Text: **cler.**  
  Annotation: [Type: KirchlicherStand, Value: "cler."]
* Text: **acol.**  
  Annotation: [Type: KirchlicherStand, Value: "acol."]
* Text: **lect.**  
  Annotation: [Type: KirchlicherStand, Value: "lect."]
  * **Hinweis:** selten, eher: KirchlichesAmt, s. Notizen unten.
* Text: **subdiac.**  
  Annotation: [Type: KirchlicherStand, Value: "subdiac."]
* Text: **diac.**  
  Annotation: [Type: KirchlicherStand, Value: "diac."]
  * **Hinweis:** vgl. KirchlichesAmt

#### Label: KirchlichesAmt

##### Beschreibung
Eine Position, die an eine Institution –Kirche, Kloster etc. – gebunden ist und mit Einnahmen verbunden ist. Durch die Implikation einer festen Stelle mit Einnahmen unterscheiden sich die hier in den Beispielen erfassten kirchlichen Ämter (z.B. presb. card. = Kardinalpriester mit einer Titelkirche) von den unter dem Label KirchlichesAmt gesammelten kirchlichen Weihen (z.B. presb. = Priester, i.e. Person, die die Priesterweihe empfangen hat). Es wird sowohl der Amtsträger (decanus) als auch das Amt (decanatus) getaggt.

##### Standard Examples:

* Text: **can. et preb.**  
  Annotation: [Type: KirchlichesAmt, Value: "can. et preb."]
  * **Hinweis:** s. Notizen unten.
* Text: **ep.**  
  Annotation: [Type: KirchlichesAmt, Value: "ep."]

##### Other Examples:

* Text: **patr.**  
  Annotation: [Type: KirchlichesAmt, Value: "patr."]
* Text: **aep.**  
  Annotation: [Type: KirchlichesAmt, Value: "aep."]
* Text: **epp.**  
  Annotation: [Type: KirchlichesAmt, Value: "epp."]
* Text: **episc.**  
  Annotation: [Type: KirchlichesAmt, Value: "episc."]
* Text: **antistes**  
  Annotation: [Type: KirchlichesAmt, Value: "antistes"]
* Text: **el.**  
  Annotation: [Type: KirchlichesAmt, Value: "el."]
* Text: **ordin.**  
  Annotation: [Type: KirchlichesAmt, Value: "ordin."]
* Text: **decan.**  
  Annotation: [Type: KirchlichesAmt, Value: "decan."]
* Text: **dec.**  
  Annotation: [Type: KirchlichesAmt, Value: "dec."]  
* Text: **archidiac.**  
  Annotation: [Type: KirchlichesAmt, Value: "archidiac."]
* Text: **vic.**  
  Annotation: [Type: KirchlichesAmt, Value: "vic."]
* Text: **abb.**  
  Annotation: [Type: KirchlichesAmt, Value: "abb."]
* Text: **abbat.**  
  Annotation: [Type: KirchlichesAmt, Value: "abbat."]
* Text: **cant.**  
  Annotation: [Type: KirchlichesAmt, Value: "cant."]
* Text: **cust.**  
  Annotation: [Type: KirchlichesAmt, Value: "cust."]
* Text: **custod.**  
  Annotation: [Type: KirchlichesAmt, Value: "custod."]
  * **Hinweis:** Ganz selten auch Laien.
* Text: **prepos.**  
  Annotation: [Type: KirchlichesAmt, Value: "prepos."]
* Text: **prep.**  
  Annotation: [Type: KirchlichesAmt, Value: "prep."]
* Text: **scolast.**  
  Annotation: [Type: KirchlichesAmt, Value: "scolast."]
* Text: **rect.**  
  Annotation: [Type: KirchlichesAmt, Value: "rect."]
* Text: **lect.**  
  Annotation: [Type: KirchlichesAmt, Value: "lect."]
  * **Hinweis:** Lektor im Kloster, selten: KirchlicherStand, s. Notizen unten.
* Text: **thesaur.**  
  Annotation: [Type: KirchlichesAmt, Value: "thesaur."]
* Text: **monach.**  
  Annotation: [Type: KirchlichesAmt, Value: "monach."]
* Text: **monialis**  
  Annotation: [Type: KirchlichesAmt, Value: "monialis."]
* Text: **dign.**  
  Annotation: [Type: KirchlichesAmt, Value: "dign."]
  * **Hinweis:** = Höhere Ämter in einem Kapitel: Propst, Dekan, Scholaster.
* Text: **can.**  
  Annotation: [Type: KirchlichesAmt, Value: "can."]
* Text: **preb.**  
  Annotation: [Type: KirchlichesAmt, Value: "preb."]
* Text: **can. sub expect. preb.**  
  Annotation: [Type: KirchlichesAmt, Value: "can. sub expect. preb."]
* Text: **can. et preb. ac supplem.**  
  Annotation: [Type: KirchlichesAmt, Value: "can. et preb. ac supplem."]
* Text: **canonicatus seu prebenda**  
  Annotation: [Type: KirchlichesAmt, Value: "canonicatus seu prebenda"]
* Text: **card.**  
  Annotation: [Type: KirchlichesAmt, Value: "card."]
* Text: **presb. card.**  
  Annotation: [Type: KirchlichesAmt, Value: "presb. card."]
  * **Hinweis:** Vgl. KirchlicherStand
* Text: **diac. card.**  
  Annotation: [Type: KirchlichesAmt, Value: "diac. card."]
  * **Hinweis:** Vgl. KirchlicherStand
* Text: **ep. card.**  
  Annotation: [Type: KirchlichesAmt, Value: "ep. card."]
  * **Hinweis:** Vgl. KirchlicherStand
* Text: **vic. generalis**  
  Annotation: [Type: KirchlichesAmt, Value: "vic. generalis"]
* Text: **mag. gen.**  
  Annotation:[Type: KirchlichesAmt, Value: "mag. gen."]
* Text: **precept.**  
  Annotation:[Type: KirchlichesAmt, Value: "precept."]
* Text: **capellan.**  
  Annotation:[Type: KirchlichesAmt, Value: "capellan."]
* Text: **cap.**  
  Annotation:[Type: KirchlichesAmt, Value: "cap."]       

#### Label: WeltlichesAmt

##### Beschreibung:
Eine Position, die an eine Institution, z.B. Königreich, gebunden ist und mit Einnahmen verbunden ist.

##### Standard Examples:

* Text: **imp.**  
  Annotation: [Type: WeltlichesAmt, Value: "imp."]
* Text: **rex**  
  Annotation: [Type: WeltlichesAmt, Value: "rex"]

##### Other Examples:

* Text: **bar.**  
  Annotation: [Type: WeltlichesAmt, Value: "bar."]
  * **Hinweis:** Wenn ein Herrschaftsgebiet genannt wird, ansonsten: SozialerStand.
* Text: **dux**  
  Annotation: [Type: WeltlichesAmt, Value: "dux."]
  * **Hinweis:** Wenn ein Herrschaftsgebiet genannt wird, ansonsten: SozialerStand.
* Text: **com.**  
  Annotation: [Type: WeltlichesAmt, Value: "com."]
  * **Hinweis:** Wenn ein Herrschaftsgebiet genannt wird, ansonsten: SozialerStand.
* Text: **comes**  
  Annotation: [Type: WeltlichesAmt, Value: "comes"]
  * **Hinweis:** Wenn ein Herrschaftsgebiet genannt wird, ansonsten: SozialerStand.
* Text: **patron.**  
  Annotation: [Type: WeltlichesAmt, Value: "patron."]
* Text: **imperator**    
  Annotation: [Type: WeltlichesAmt, Value: "imperator"]
* Text: **rex elect.**    
  Annotation: [Type: WeltlichesAmt, Value: "rex elect."]
* Text: **proconsul**    
  Annotation: [Type: WeltlichesAmt, Value: "proconsul"]
* Text: **consul**    
  Annotation: [Type: WeltlichesAmt, Value: "consul"]
* Text: **burggravius**    
  Annotation: [Type: WeltlichesAmt, Value: "burggravius"]  
 
#### Label: Verwaltungsamt

##### Beschreibung:
Eine Position, die an eine Institution, z.B. apostolische Kammer, gebunden ist und mit Einnahmen verbunden ist. Es wird sowohl der Amtsträger (subcollector) als auch das Amt (officium subcollectorie) getaggt.

##### Standard Examples:

* Text: **abbr.**  
  Annotation: [Type: Verwaltungsamt, Value: "abbr."]
* Text: **administr.**  
  Annotation: [Type: Verwaltungsamt, Value: "administr."]
* Text: **aud.**  
  Annotation: [Type: Verwaltungsamt, Value: "aud."]

##### Other Examples:

* Text: **cancell.**  
  Annotation: [Type: Verwaltungsamt, Value: "cancell."]
* Text: **collect.**  
  Annotation: [Type: Verwaltungsamt, Value: "collect."]
* Text: **consilarius**  
  Annotation: [Type: Verwaltungsamt, Value: "consilarius"]
* Text: **cubic.**  
  Annotation: [Type: Verwaltungsamt, Value: "cubic."]
* Text: **cursor**  
  Annotation: [Type: Verwaltungsamt, Value: "cursor"]
* Text: **not.**  
  Annotation: [Type: Verwaltungsamt, Value: "not."]
* Text: **nunt.**  
  Annotation: [Type: Verwaltungsamt, Value: "nunt."]
* Text: **offic.**  
  Annotation: [Type: Verwaltungsamt, Value: "offic."]
* Text: **procur.**  
  Annotation: [Type: Verwaltungsamt, Value: "procur."] 
* Text: **proc.**  
  Annotation: [Type: Verwaltungsamt, Value: "proc."]
* Text: **proc.** ap. sed.  
  Annotation: [Type: Verwaltungsamt, Value: "proc."]
* Text: **prothonot.**  
  Annotation: [Type: Verwaltungsamt, Value: "prothonot."]
* Text: **refer.**  
  Annotation: [Type: Verwaltungsamt, Value: "refer."]
* Text: **script.**  
  Annotation: [Type: Verwaltungsamt, Value: "script."]
* Text: **script. litt. ap.**  
  Annotation: [Type: Verwaltungsamt, Value: "script. litt. ap."]
* Text: **scult.**  
  Annotation: [Type: Verwaltungsamt, Value: "scult."]
* Text: **secret.**  
  Annotation: [Type: Verwaltungsamt, Value: "secret."]
* Text: **secr.**  
  Annotation: [Type: Verwaltungsamt, Value: "secr."]
* Text: **subcollector**  
  Annotation: [Type: Verwaltungsamt, Value: "subcollector"]  
* Text: **tab.**  
  Annotation: [Type: Verwaltungsamt, Value: "tab."]
* Text: **iud.**  
  Annotation: [Type: Verwaltungsamt, Value: "iud."]
* Text: **iudex**  
  Annotation: [Type: Verwaltungsamt, Value: "iudex"] 

#### Label: Bildung

##### Standard Examples:

* Text: **licent.**  
  Annotation: [Type: Bildung, Value: "licent."]
* Text: **scol.**  
  Annotation: [Type: Bildung, Value: "scol."]
* Text: **bac. in decr.**  
  Annotation: [Type: Bildung, Value: "bac. in decr."]

##### Other Examples:

* Text: **studens**  
  Annotation: [Type: Bildung, Value: "studens"]
* Text: **lic.**   
  Annotation: [Type: Bildung, Value: "lic."]
  * **Hinweis:** Nur selten steht lic. für das Lizenziat, i.d.R. nur in Verbindung mit einem Namen. Häufiger steht es für die päpstliche Lizenz und wird dann als Event getaggt.
* Text: **lic. in decr.**    
  Annotation: [Type: Bildung, Value: "lic. in decr."]
* Text: **lic. in leg.**  
  Annotation: [Type: Bildung, Value: "lic. in leg."]
* Text: **lic. in iure can.**  
  Annotation: [Type: Bildung, Value: "lic. in iure can."]
* Text: **mag.**  
  Annotation: [Type: Bildung, Value: "mag."]
* Text: **mag. in art.**  
  Annotation: [Type: Bildung, Value: "mag. in art."]
* Text: **decr. doct.**  
  Annotation: [Type: Bildung, Value: "decr. doct."]
* Text: **aud. gen.**  
  Annotation: [Type: Bildung, Value: "aud. gen."]

* **Hinweis:** Und entsprechende Permutationen (mag. in art. / art. mag. …, utriusque iuris, theol. … Bitte ergänzen).

#### Label: VitaZusatz

##### Beschreibung:
Weitere Informationen zur Person, z.B. in Form von längeren Relativsätzen.

##### Standard Examples:

* Text: **adh.**  
  Annotation: [Type: VitaZusatz, Value: "adh."] 
* Text: **qui per multos annos cur. secutus est absque consolatione benef. et ratione alicuius proc. Magnis expensis oppressus est**  
  Annotation: [Type: VitaZusatz, Value: "qui per multos annos cur. secutus est absque consolatione benef. et ratione alicuius proc. Magnis expensis oppressus est"]

#### Label: Orden

##### Beschreibung: 
Religiöse Ordensgemeinschaften

##### Standard Examples:

* Text: **o. s. Ant.**  
  Annotation: [Type: Orden, Value: "o. s. Ant."]
* Text: **o. s. Aug.**  
  Annotation: [Type: Orden, Value: "o. s. Aug."]
* Text: **o. s. Ben.**  
  Annotation: [Type: Orden, Value: "o. s. Ben."]

##### Other Examples:

* Text: **o. cist.**  
  Annotation: [Type: Orden, Value: "o. cist."]
* Text: **o. fr. herem. s. Aug.**  
  Annotation: [Type: Orden, Value: "o. fr. herem. s. Aug."]
* Text: **o. s. Ant.**  
  Annotation: [Type: Orden, Value: "o. s. Ant."]
* Text: **o. s. Clare**  
  Annotation: [Type: Orden, Value: "o. s. Clare"]
* Text: **o. Carm.**  
  Annotation: [Type: Orden, Value: "o. Carm."]
* Text: **o. Cartus.**  
  Annotation: [Type: Orden, Value: "o. Cartus."]
* Text: **o. Clun.**  
  Annotation: [Type: Orden, Value: "o. Clun."]
* Text: **o. fr. min.**  
  Annotation: [Type: Orden, Value: "o. fr. min."]
* Text: **o. pred.**  
  Annotation: [Type: Orden, Value: "o. pred."]
* Text: **o. Prem.**  
  Annotation: [Type: Orden, Value: "o. Prem."]

* **Hinweis:** Und deren Variationen (z.B. o. Cist.; Cist. ord.). Bitte ergänzen!

### Kategorie: Event

* **Hinweis:** Die Kategorie Event zerfällt in die zwei Unterkategorien "Gnadenerweise/Indulta/Gratiae" und “EventNichtPapst”. Die Unterkategorie "Gnadenerweise" umfasst alle Labels von "Abolitio" bis einschließlich "UndefinierteGnade" und bezieht sich auf Handlungen, die vom Papst ausgehen (i.e. Gnaden, die vom Papst gewährt werden). Die Labels der Unterkategorie "EventNichtPapst" beziehen sich auf Handlungen des Petenten oder einer anderen Person, die im Regest auftritt. Zu einem späteren Zeitpunkt, wenn wir mehr Daten ausgewertet haben, könnte es sinnvoll sein, die Labels der Unterkategorie "Gnadenerweise/Indulta/Gratiae" nach kirchenrechtlichen (oder anderen) Kriterien zu gruppieren und ggf. weiter zu unterteilen (z.B. disp. de def. nat.; disp. de def. et. ...).

### Event: Gnadenerweise/Indult/Gratiae

#### Label: Abolitio

##### Beschreibung:
Tilgung, z.B. von Inhabilität

##### Standard Examples:

* Text: **m. abol. inhabil.**  
  Annotation: [Type: Abolitio, Value: "m. abol. inhabil."]
* Text: **abol. inhabil.**  
  Annotation: [Type: Abolitio, Value: "abol. inhabil."]
* Text: **abol. macule infamie**  
  Annotation: [Type: Abolitio, Value: "abol. macule infamie."]

#### Label: AbolitioZusatz

##### Beschreibung:
Kennzeichnung des Gnadeninhalts. Der gesamte Gnadeninhalt wird mit dem Label AbolitioZusatz getaggt, nicht aber die Gnade abol. selbst.

##### Standard Examples:

* Text: m. abol. inhabil., **quia sacr. ord. una die per Matheum ep. olim Placentin. indebite recepit, n. o. proc. per mag. Angelum de Balionibus aud. gen. cam. ap. instructo** 4 mart. 1412 L 158 130.  
  Annotation: [Type: AbolitioZusatz, Value: "quia sacr. ord. una die per Matheum ep. olim Placentin. indebite recepit, n. o. proc. per mag. Angelum de Balionibus aud. gen. cam. ap. instructo"]


#### Label: Absolutio

##### Beschreibung:
Absolution

##### Standard Examples:

* Text: **absol.**  
  Annotation: [Type: Absolutio, Value: "absol."]
* Text: **m. absol.**  
  Annotation: [Type: Absolutio, Value: "m. absol."]
* Text: **m. absol.** a sent. excom.  
  Annotation: [Type: Absolutio, Value: "m. absol."]

##### Other Examples:

* Text: **absol.** a matrim. C. gentili et quasi pagano contracto  
  Annotation: [Type: Absolutio, Value: "absol."]
* Text: **absol.**, quod olim …  
  Annotation: [Type: Absolutio, Value: "absol."]

#### Label: AbsolutioZusatz

##### Beschreibung:
Kennzeichnung des Gnadeninhalts der Absolution. Der gesamte Gnadeninhalt wird mit dem Label AbsolutioZusatz getaggt, nicht aber die Gnade absol. oder m. absol. selbst.

##### Standard Examples:

* Text: m. absol. **a sent. excom.**  
  Annotation: [Type: AbsolutioZusatz, Value: "a sent. excom."]
* Text: absol. **a matrim. C. gentili et quasi pagano contracto**  
  Annotation: [Type: AbsolutioZusatz, Value: "a matrim. C. gentili et quasi pagano contracto"]
* Text: absol., **quod olim …**  
  Annotation: [Type: AbsolutioZusatz, Value: "quod olim …"]

#### Label: Aggravatio

##### Beschreibung:
Verstärkung einer Strafe

##### Standard Examples:

* Text: **m. aggrav. sent.**  
  Annotation: [Type: Aggravatio, Value: "m. aggrav. sent."]
* Text: **m. aggrav. excom. sent.**  
  Annotation: [Type: Aggravatio, Value: "m. aggrav. excom. sent."]
* Text: **m. aggravandi sent.**  
  Annotation: [Type: Aggravatio, Value: "m. aggravandi sent."]

#### Label: Cassatio

##### Beschreibung:
Ungültigkeitserklärung

##### Standard Examples:

* Text: **cass.**  
  Annotation: [Type: Cassatio, Value: "cass."]
* Text: **m. cass.** litt.  
  Annotation: [Type: Cassatio, Value: "m. cass."]
* Text: **cass.** pensionis  
  Annotation: [Type: Cassatio, Value: "cass."]

#### Label: CassatioZusatz

#### Beschreibung:
Kennzeichnung des Gnadeninhalts der Cassatio. Der gesamte Gnadeninhalt wird mit dem Label CassatioZusatz getaggt, nicht aber die Gnade cass. selbst.

##### Standard Examples:

* Text: m. cass. **litt.**  
  Annotation: [Type: CassatioZusatz, Value: "litt."]
* Text: de cass. **pensionis**  
  Annotation: [Type: CassatioZusatz, Value: "pensionis."]

#### Label: Commissio

##### Beschreibung:
Auftrag zur weiteren Bearbeitung eines Falles

##### Standard Examples:

* Text: **committ.**  
  Annotation: [Type: Commissio, Value: "committ."]

#### Label: Concessio

##### Beschreibung:
Verleihung / Erlaubnis = Lizenz (?)

##### Standard Examples:

* Text: **conc. transgr.**  
  Annotation: [Type: Concessio, Value: "conc. transgr."]
  * **Hinweis:** vgl. Licentia -> lic. transgr.

#### Label: Confirmatio

##### Beschreibung:
Bestätigung

##### Standard Examples:

* Text: **conf.**  
  Annotation: [Type: Confirmatio, Value: "conf."]

#### Label: ConfirmatioZusatz

##### Beschreibung:
Kennzeichnung des Gnadeninhalts. Der gesamte Gnadeninhalt wird mit dem Label ConfirmatioZusatz getaggt, nicht aber die Gnade conf. selbst.

##### Standard Examples:

* Text: conf. **emptionem pratorum ac al. bonorum in villa Diczisow Constant. dioc. ac donationem iuris patron. super par. eccl. in dicta villa ex possess. Eberhardi Burgermaister incole dicti op. factam** 22 oct. 1411 L 157 113.  
  Annotation: [Type: ConfirmatioZusatz, Value: "emptionem pratorum ac al. bonorum in villa Diczisow Constant. dioc. ac donationem iuris patron. super par. eccl. in dicta villa ex possess. Eberhardi Burgermaister incole dicti op. factam"]

#### Label: Declaratio

##### Beschreibung:
Erklärung

##### Standard Examples:

* Text: **decl.**  
  Annotation: [Type: Declaratio, Value: "decl."]

#### Label: Derogatio

##### Beschreibung: 
Klauseln, die andere Regelungen / Tatsachen außer Kraft setzen; vgl. das Label NonObstantien.

##### Standard Examples:

* Text: de **derog.**  
  Annotation: [Type: Derogatio, Value: "derog."]
* Text: c. **derog.**  
  Annotation: [Type: Derogatio, Value: "derog."]

#### Label: DerogatioZusatz

##### Beschreibung:
Kennzeichnung des Gnadeninhalts der Derogatio. Der gesamte Gnadeninhalt wird mit dem Label DerogatioZusatz getaggt, nicht aber die Gnade derog. selbst.

##### Standard Examples:

* Text: c. derog. **statut. d. eccl. quod nullus nisi can. actu prebend. et capitul. inibi dign. assequi val.** 6. decb. 1437 S 342 193v.
  Annotation: [Type: DerogatioZusatz, Value: "statut. d. eccl. quod nullus nisi can. actu prebend. et capitul. inibi dign. assequi val."]

##### Other Examples:

* Text: de derog. **antelationum quibusdam aliis prerog. curialium habentibus in concil. Basil. existentibus conc. ratione gr. expect. sue** s.d. 24. apr. 31 20. decb. 1436 S 329 239rs.
  Annotation: [Type: DerogatioZusatz, Value: "antelationum quibusdam aliis prerog. curialium habentibus in concil. Basil. existentibus conc. ratione gr. expect. sue"]
* Text: c. derog. **statutis eccl. s. Petri de optando** 18. aug. 1463 S 566 89r, L 582 63v-65r.
  Annotation: [Type: DerogatioZusatz, Value: "statutis eccl. s. Petri de optando"]

#### Label: Dispensatio

##### Beschreibung:
Befreiung, Außerkraftsetzung kirchlicher Gesetze

##### Standard Examples:

* Text: **disp.**  
  Annotation: [Type: Dispensatio, Value: "disp."]

##### Other Examples:

* Text: **disp.** sup. def. nat.  
  Annotation: [Type: Dispensatio, Value: "disp."]
* Text: **disp.** super def. etat. et super prom. ad sacr. ord.  
  Annotation: [Type: Dispensatio, Value: "disp."]
* Text: de **disp.** ut d. Theordericus d. prepos. unac. alio benef. recip. valeat    
  Annotation: [Type: Dispensatio, Value: "disp."]

#### Label: DispensatioZusatz

##### Beschreibung:
Kennzeichnung des Gnadeninhalts. Der gesamte Gnadeninhalt wird mit dem Label DispensatioZusatz getaggt, nicht aber die Gnade disp. selbst.

##### Standard Examples:

* Text: disp. **sup. def. nat.**  
  Annotation: [Type: DispensatioZusatz, Value: "sup. def. nat."]
* Text: disp. **super def. etat. et super prom. ad sacr. ord.**  
  Annotation: [Type: DispensatioZusatz, Value: "super def. etat. et super prom. ad sacr. ord."]
* Text: de disp. **ut d. Theordericus d. prepos. unac. alio benef. recip. valeat**   
  Annotation: [Type: DispensatioZusatz, Value: "ut d. Theordericus d. prepos. unac. alio benef. recip. valeat"]

#### Label: Erectio

##### Beschreibung:
Erlaubnis zur Errichtung einer neuen kirchlichen Institution oder der Erhebung einer Kaplanei/Vikarie zur Pfarrkirche bzw. Pfarrkirche zur Kollegiatkirche etc.

##### Standard Examples:

* Text: **m. erig.**  
  Annotation: [Type: Erectio, Value: "m. erig."]
* Text: **erig.**  
  Annotation: [Type: Erectio, Value: "erig."]
* Text: **m. instit.**  
  Annotation: [Type: Erectio, Value: "m. instit."]

##### Other Examples:

* Text: **erigere**  
  Annotation: [Type: Erectio, Value: "erigere"]
* Text: de **erectione**  
  Annotation: [Type: Erectio, Value: "erectione"]
* Text: **instit.**  
  Annotation: [Type: Erectio, Value: "instit."]
* Text: de **institutione**  
  Annotation: [Type: Erectio, Value: "institutione."]

#### Label: Exemptio

##### Beschreibung:
Befreiung, Ausnahmestellung

##### Standard Examples:

* Text: **exemt.** de iurisdictione ordin.  
  Annotation: [Type: Exemptio, Value: "exemt."]
* Text: **exempt.** de iurisdictione ordin.  
  Annotation: [Type: Exemptio, Value: "exempt."]
* Text: **exemptione** de iurisdictione ordin.  
  Annotation: [Type: Exemptio, Value: "exemptione"] 

##### Other Examples:

* Text: **exemtione** de iurisdictione ordin.  
  Annotation: [Type: Exemptio, Value: "exemtione"]

#### Label: Facultas

##### Beschreibung:
Erlaubnis. Vgl. Lizenz und Concessio (?)

##### Standard Examples:

* Text: **facult.** resign.  
  Annotation: [Type: Facultas, Value: "facult."]

##### Other Examples:

* Text: **facult.** absol. eos, qui…  
  Annotation: [Type: Facultas, Value: "facult."]
* Text: **facult.** absol. 100 person.  
  Annotation: [Type: Facultas, Value: "facult."]
* Text: **facult.** absol. in casibus, in quibus …  
  Annotation: [Type: Facultas, Value: "facult."]  
* Text: **facult.** reconciliandi  
  Annotation: [Type: Facultas, Value: "facult."]
* Text: alternativa **facult.** disponendi  
  Annotation: [Type: Facultas, Value: "facult."]

#### Label: FacultasZusatz

##### Beschreibung:
Kennzeichnung des Gnadeninhalts. Der gesamte Gnadeninhalt wird mit dem Label FacultasZusatz getaggt, nicht aber die Gnade facult. selbst.

##### Standard Examples:

* Text: facult. **resign.**  
  Annotation: [Type: FacultasZusatz, Value: "resign."]
* Text: facult. **absol. eos, qui (unknown)**  
  Annotation: [Type: FacultasZusatz, Value: "absol. eos, qui (unknown)"]
  * **Hinweis:** (unknown) steht für den Rest des Relativsatzes.
* Text: facult. **absol. 100 person.**  
  Annotation: [Type: FacultasZusatz, Value: "absol. 100 person."]

##### Other Examples:

* Text: facult. **absol. in casibus, in quibus (unknown)**  
  Annotation: [Type: FacultasZusatz, Value: "absol. in casibus, in quibus (unknown)"]
  * **Hinweis:** (unknown) steht für den Rest des Relativsatzes.
* Text: facult. **reconciliandi**  
  Annotation: [Type: FacultasZusatz, Value: "reconciliandi"]
* Text: **alternativa** facult. **disponendi**  
  Annotation: 
  - [Type: FacultasZusatz, Value: "alternativa"]
  - [Type: FacultasZusatz, Value: "disponendi"]

#### Label: Habilitatio

##### Beschreibung:
Wiederherstellung der Befähigung zur Ausübung einer Rechtshandlung

##### Standard Examples:

* Text: **habil.**  
  Annotation: [Type: Habilitatio, Value: "habil."]
* Text: **rehab.**  
  Annotation: [Type: Habilitatio, Value: "rehab."]

##### Other Examples: 

* Text: **rehabilitatio**  
  Annotation: [Type: Habilitatio, Value: "rehabilitatio"]
* Text: **habilitatio**  
  Annotation: [Type: Habilitatio, Value: "habilitatio"]

#### Label: Indulgentia

##### Beschreibung:
Indulgenz, Ablass

##### Standard Examples:

* Text: **indulg.**  
  Annotation: [Type: Indulgentia, Value: "indulg."]

#### Label: Incorporatio

##### Beschreibung:
Einverleibung einer kirchlichen Institution durch eine andere

##### Standard Examples:

* Text: **inkorp.**  
  Annotation: [Type: Incorporatio, Value: "inkorp."]
* Text: **unio**  
  Annotation: [Type: Incorporatio, Value: "unio"]

#### Label: Introductio

##### Beschreibung:
Einführung in die Besitztümer einer Pfründe

##### Standard Examples:

* Text: **m. introduc. in possess.**  
  Annotation: [Type: Introductio, Value: "m. introduc. in possess."]
* Text: **in possessionem** bonorum eorum eccl. **introducat**  
  Annotation: 
  - [Type: Introductio, Value: "in possessionem"]
  - [Type: Introductio, Value: "introducat"]

#### Label: LitteraConservatoriaBonorum

##### Beschreibung:
Schutzbrief

##### Standard Examples:

* Text: de **conserv.**  
  Annotation: [Type: LitteraConservatoriaBonorum, Value: "conserv."]

#### Label: LitteraPassus

##### Beschreibung:
Reiseerlaubnis und Schutzbrief

##### Standard Examples:

* Text: **litt. passus**  
  Annotation: [Type: LitteraPassus, Value: "litt. passus"]
* Text: **littera passus**  
  Annotation: [Type: LitteraPassus, Value: "littera passus"]

#### Label: Licentia

##### Beschreibung:
Sondererlaubnis

##### Standard Examples:

* Text: **lic.**  
  Annotation: [Type: Licentia, Value: "lic."]
* Text: **m. lic.**  
  Annotation: [Type: Licentia, Value: "m. lic."]

##### Other Examples:

* Text: **lic.** de ante diem  
  Annotation: [Type: Licentia, Value: "lic."]
* Text: **lic.** armuciis de vario et griseo utendi  
  Annotation: [Type: Licentia, Value: "lic."]
* Text: **lic.** visitandi Sepulcrum Dominicum  
  Annotation: [Type: Licentia, Value: "lic."]
* Text: **lic.** ratione par. eccl. s. Martini, … in casu quod rect. unius ex d. eccl. fuerit excom., per alios presb. sibi sacramenta ministrari faciendi  
  Annotation: [Type: Licentia, Value: "lic."]

#### Label: LicentiaZusatz

##### Beschreibung:
Kennzeichnung des Gnadeninhalts. Der gesamte Gnadeninhalt wird mit dem Label LicentiaZusatz getaggt, nicht aber die Gnade lic. selbst.

##### Standard Examples:

* Text: lic. **de ante diem**  
  Annotation: [Type: LicentiaZusatz, Value: "de ante diem"]
* Text: lic. **armuciis de vario et griseo utendi**  
  Annotation: [Type: LicentiaZusatz, Value: "armuciis de vario et griseo utendi"]
* Text: lic. **visitandi Sepulcrum Dominicum**  
  Annotation: [Type: LicentiaZusatz, Value: "visitandi Sepulcrum Dominicum"]

##### Other Examples:

* Text: lic. **ratione par. eccl. s. Martini, … in casu quod rect. unius ex d. eccl. fuerit excom., per alios presb. sibi sacramenta ministrari faciendi**  
  Annotation: [Type: LicentiaZusatz, Value: "ratione par. eccl. s. Martini, … in casu quod rect. unius ex d. eccl. fuerit excom., per alios presb. sibi sacramenta ministrari faciendi"]

#### Label: Monitorium

##### Beschreibung:
Ermahnung durch den Papst

##### Standard Examples:

* Text: **monitorium penale**  
  Annotation: [Type: Monitorium, Value: "monitorium penale"]

#### Label: Moratorium

##### Beschreibung:
Zahlungsaufschub

##### Standard Examples:

* Text: de **moratorio**  
  Annotation: [Type: Moratorium, Value: "moratorio"]
* Text: **moratorium**  
  Annotation: [Type: Moratorium, Value: "moratorium"]

##### Hinweis
Hauptsächlich in RG 10 (?)

#### Label: Pensio

##### Beschreibung:
Verleihung und Modifizierung von Pensionsleistunen

##### Standard Examples:

* Text: de **reductione pensionis**  
  Annotation: [Type: Pensio, Value: "reductione pensionis."]
* Text: de **transl. pensionis**  
  Annotation: [Type: Pensio, Value: "transl. pensionis."]

#### Label: Prerogativa

##### Beschreibung:
Vorrecht, Prärogative

##### Standard Examples:

* Text: **prerog.** ad instrar pape fam.  
  Annotation: [Type: Prerogativa, Value: "prerog."]
* Text: **antelatio**  
  Annotation: [Type: Prerogativa, Value: "antelatio"]

##### Other Examples:

* Text: **prerog.** pape fam. in absentia  
  Annotation: [Type: Prerogativa, Value: "prerog."]

#### Label: Prorogatio

##### Beschreibung:
Fristverlängerung

##### Standard Examples:

* Text: **prorog.**  
  Annotation: [Type: Prorogatio, Value: "prorog."]

##### Other Examples: 

* Text: cum **prorog.** term. solut. ad 1 an. propter incertitudinem taxe  
  Annotation: [Type: Prorogatio, Value: "prorog."]

#### Label: ProrogatioZusatz

##### Beschreibung:
Kennzeichnung des Gnadeninhalts. Der gesamte Gnadeninhalt wird mit dem Label ProrogatioZusatz getaggt, nicht aber die Gnade prorog. selbst.

##### Standard Examples:

* Text: cum prorog. **term. solut. ad 1 an. propter incertitudinem taxe**  
  Annotation: [Type: ProrogatioZusatz, Value: "term. solut. ad 1 an. propter incertitudinem taxe"]

#### Label: Provisio

##### Beschreibung:
Bestimmungen zur Verleihung eines Benefizes

##### Standard Examples:

* Text: **prov.**  
  Annotation: [Type: Provisio, Value: "prov."]
* Text: **m. prov.**  
  Annotation: [Type: Provisio, Value: "m. prov."]
* Text: **nova prov.**  
  Annotation: [Type: Provisio, Value: "nova prov."]

##### Other Examples:

* Text: **prov. si neutri**  
  Annotation: [Type: Provisio, Value: "prov. si neutri"]
* Text: **prov. si nulli**  
  Annotation: [Type: Provisio, Value: "prov. si nulli"]
* Text: **surrog.** ad iur.  
  Annotation: [Type: Provisio, Value: "surrog."]
* Text: **gr. expect.**  
  Annotation: [Type: Provisio, Value: "gr. expect."]

#### Label: Reformatio

##### Beschreibung:
Abänderung, Nachbesserung einer päpstlichen Gnade (?)

##### Standard Examples:

* Text: **ref.**  
  Annotation: [Type: Reformatio, Value: "ref."]
* Text: **reformatio**  
  Annotation: [Type: Reformatio, Value: "reformatio"]

#### Label: Revalidatio

##### Beschreibung:
Erklärung der Gültigkeit einer verfallenen Gnade

##### Standard Examples:

* Text: **reval.**  
  Annotation: [Type: Revalidatio, Value: "reval."]

#### Label: SalvusConductus

##### Beschreibung:
Sicherheitsbrief für flüchtige Personen

##### Standard Examples:

* Text: **salv. cond.**  
  Annotation: [Type: SalvusConductus, Value: "salv. cond."]
* Text: **salvus conductus**  
  Annotation: [Type: SalvusConductus, Value: "salvus conductus"]
* Text: **salc. cond.**  
  Annotation: [Type: SalvusConductus, Value: "salc. cond."]
  * **Hinweis:** Achtung: im Digitalisat von Band 3 falsch eingelesen als salc. statt salv.

#### Label: UndefinierteGnade

##### Beschreibung:
Gnaden, die nicht explizit den Begriff der gewährten Gnade – Abolitio, Absolution, Dispens etc. – , sondern nur den Inhalt der Gnade [de alt. port.] oder den allgemeinen Terminus gratia angeben. Hier ist keine vollständige Liste möglich.

##### Standard Examples:

* Text: gratia de **alt. port.**  
  Annotation: [Type: UndefinierteGnade, Value: "alt. port."]
* Text: de **alt. port.**  
  Annotation: [Type: UndefinierteGnade, Value: "alt. port."]
* Text: gratia de **confess. elig.**  
  Annotation: [Type: UndefinierteGnade, Value: "confess. elig."]
* Text: de **confess. elig.**  
  Annotation: [Type: UndefinierteGnade, Value: "confess. elig."]

##### Other Examples:

* Text: de **rem. plen.**  
  Annotation: [Type: UndefinierteGnade, Value: "rem. plen."]
* Text: de **locis interdictis**  
  Annotation: [Type: UndefinierteGnade, Value: "locis interdictis"]
* Text: de **benef.**  
  Annotation: [Type: UndefinierteGnade, Value: "benef."]
* Text: de **prom. ad ord.**  
  Annotation: [Type: UndefinierteGnade, Value: "prom. ad ord."]
* Text: de **prom. ad ord. extra temp.**  
  Annotation: [Type: UndefinierteGnade, Value: "prom. ad ord. extra temp."]
* Text: de **n. prom.**  
  Annotation: [Type: UndefinierteGnade, Value: "n. prom."]
* Text: de **n. resid.**  
  Annotation: [Type: UndefinierteGnade, Value: "n. resid."]
* Text: de **fruct. percip.**  
  Annotation: [Type: UndefinierteGnade, Value: "fruct. percip."]
* Text: de **visitatione et reformatione**  
  Annotation: [Type: UndefinierteGnade, Value: "visitatione et reformatione"]

### Event: EventNichtPapst

#### Label: EventNichtPapst

##### Beschreibung:
Handlungen, die von einer anderen Person als dem Papst bzw. von nicht-Personen ausgehen. Hier ist keine vollständige Liste möglich.

##### Standard Examples:

* Text: **vac. p. o.**  
  Annotation: [Type: EventNichtPapst, Value: "vac. p. o."]
* Text: **vacat. p. o.**  
  Annotation: [Type: EventNichtPapst, Value: "vacat. p. o."]
  * **Hinweis:** Neben p.o., das als Abkürzung für per obitum am häufigsten vorkommt, gibt es in Band 1 und 3 des RG per ob. als Alternative und in Band 9 p.o. in curia.
* Text: **vac. p. prom.**  
  Annotation: [Type: EventNichtPapst, Value: "vac. p. prom."]

##### Other Examples:

* Text: **vac. p. n. prom.**  
  Annotation: [Type: EventNichtPapst, Value: "vac. p. n. prom."]
* Text: **vac. p. priv.**  
  Annotation: [Type: EventNichtPapst, Value: "vac. p. priv."]
* Text: **vac. p. devol.**  
  Annotation: [Type: EventNichtPapst, Value: "vac. p. devol."]
* Text: **vac. p. transgr.**  
  Annotation: [Type: EventNichtPapst, Value: "vac. p. transgr."]
* Text: **vac. p. resign.**  
  Annotation: [Type: EventNichtPapst, Value: "vac. p. resign."]
* Text: **vac. p. assec.**  
  Annotation: [Type: EventNichtPapst, Value: "vac. p. assec."]
* Text: **vac. p. ingress. relig.**  
  Annotation: [Type: EventNichtPapst, Value: "vac. p. ingress. relig."]
* Text: **vac. p. contract. matrim.**  
  Annotation: [Type: EventNichtPapst, Value: "vac. p. contract. matrim."]
* Text: **vac. ex eo quod** …  
  Annotation: [Type: EventNichtPapst, Value: "vac. ex eo quod"]
* Text: **prom.**  
  Annotation: [Type: EventNichtPapst, Value: "prom."]
* Text: **resign.**  
  Annotation: [Type: EventNichtPapst, Value: "resign."]
* Text: **litig.**  
  Annotation: [Type: EventNichtPapst, Value: "litig."]
* Text: **indebite assec. fuit**  
  Annotation: [Type: EventNichtPapst, Value: "indebite assec. fuit"]
* Text: **destin.**    
  Annotation: [Type: EventNichtPapst, Value: "destin."]
* Text: **solv.**    
  Annotation: [Type: EventNichtPapst, Value: "solv."]  
* Text: **iuram. fidel.**    
  Annotation: [Type: EventNichtPapst, Value: "iuram. fidel."]
* Text: **constit. iudices appellat.**    
  Annotation: [Type: EventNichtPapst, Value: "constit. iudices appellat."]    

* **Hinweis:** Achtung: Erstmal nur Groberfassung, z.B. de qua **litig.**

### Kategorie: Varia

#### Label: Verwaltungseinheit

##### Beschreibung:
Vor allem weltliche Verwaltungseinheiten, z.B. Herzogtümer.

##### Standard Examples:

* Text: **ducat.**  
  Annotation: [Type: Verwaltungseinheit, Value: "ducat."]
* Text: **baron.**  
  Annotation: [Type: Verwaltungseinheit, Value: "baron."]
* Text: **civit.**  
  Annotation: [Type: Verwaltungseinheit, Value: "civit."]

##### Other Examples:

* Text: **op.**  
  Annotation: [Type: Verwaltungseinheit, Value: "op."]
* Text: **op. imp.**  
  Annotation: [Type: Verwaltungseinheit, Value: "op. imp."]
* Text: **Slesia**  
  Annotation: [Type: Verwaltungseinheit, Value: "Slesia"]
* Text: **villa**  
  Annotation: [Type: Verwaltungseinheit, Value: "villa"]

#### Label: Diözese

##### Beschreibung:
Eine kirchliche Verwaltungseinheit.

##### Standard Examples:

* Text: **Traiect. dioc.**  
  Annotation: [Type: Diözese, Value: "Traiect. dioc."]
* Text: **dioc. Traiect.**  
  Annotation: [Type: Diözese, Value: "dioc. Traiect."]


##### Other Examples:

* Text: **Magunt. dioc.**  
  Annotation: [Type: Diözese, Value: "Magunt. dioc."]
* Text: **Colon. dioc.**  
  Annotation: [Type: Diözese, Value: "Colon. dioc."]

#### Label: Institution

##### Beschreibung:
Kirchen, Klöster, Universitäten, etc.

##### Standard Examples:

* Text: **eccl.**  
  Annotation: [Type: Institution, Value: "eccl."]
* Text: **par. eccl.**  
  Annotation: [Type: Institution, Value: "par. eccl."]
* Text: **mon.**  
  Annotation: [Type: Institution, Value: "mon."]

##### Other Examples:

* Text: **capit.**  
  Annotation: [Type: Institution, Value: "capit."]
* Text: **capit. eccl.**  
  Annotation: [Type: Institution, Value: "capit. eccl."]
* Text: **fil. eccl.**  
  Annotation: [Type: Institution, Value: "fil. eccl."]
* Text: **colleg. eccl.**  
  Annotation: [Type: Institution, Value: "colleg. eccl."]
* Text: **capel.**  
  Annotation: [Type: Institution, Value: "capel."]
* Text: **cathedr.**  
  Annotation: [Type: Institution, Value: "cathedr."]
* Text: **conv.**  
  Annotation: [Type: Institution, Value: "conv."]
* Text: **ord.**  
  Annotation: [Type: Institution, Value: "ord."]
* Text: **cam.**  
  Annotation: [Type: Institution, Value: "cam."]
* Text: **penit.**  
  Annotation: [Type: Institution, Value: "penit."]
* Text: **pen.**  
  Annotation: [Type: Institution, Value: "pen."]
* Text: **abbatia**  
  Annotation: [Type: Institution, Value: "abbatia"]
* Text: **hosp. paup.**  
  Annotation: [Type: Institution, Value: "hosp. paup."]
* Text: **conv.** mon.  
  Annotation: [Type: Institution, Value: "conv."]
* Text: **dom.**  
  Annotation: [Type: Institution, Value: "dom."]
  * **Hinweis:** Achtung: dom. nur als Institution taggen, wenn es für domus steht, nicht für dominus.
* Text: **domus**  
  Annotation: [Type: Institution, Value: "domus"]

#### Label: InstitutionZusatz

##### Beschreibung:
Information zur Beziehung einer kirchlichen Institution zur Kurie, insbesondere die direkte Unterstellung unter den Papst (Exemption). 

##### Standard Examples:

* Text: eccl. b. Marie castri Aldenburg. Rom. eccl. **immed. subiect.**  
  Annotation: [Type: Institution, Value: "immed. subiect."]

#### Label: Titelkirche

##### Beschreibung:
Kirchen, die Bischöfen, Priestern und Diakonen bei ihrer Kardinalsweihe zugeteilt werden. Ihre Anzahl ist finit. Man erkennt sie v.a. daran, dass in ihrer Nähe im Regest ein Kardinal genannt wird (ep. card., presb. card., diac. card.). In diesen Fällen wird ausnahmsweise darauf verzichtet, zusätzlich das Patrozinium oder den Ort als solche gesondert zu taggen.

##### Standard Examples:

* **Titelkirchen Kardinalbischöfe:**
  * Text: **Albanen.**  
    Annotation: [Type: Titelkirche, Value: "Albanen."]
  * Text: **Ostien. et Velletren.**  
    Annotation: [Type: Titelkirche, Value: "Ostien. et Velletren."]
  * Text: **Portuen. et s. Rufinae**  
    Annotation: [Type: Titelkirche, Value: "Portuen. et s. Rufinae"]
* **Titelkirchen Kardinalpriester:**
  * Text: **S. Anastasiae**  
    Annotation: [Type: Titelkirche, Value: "S. Anastasiae"]
  * Text: **Ss. XII Apostolorum**  
    Annotation: [Type: Titelkirche, Value: "Ss. XII Apostolorum"]
  * Text: **S. Balbinae**  
    Annotation: [Type: Titelkirche, Value: "S. Balbinae"]

##### Other Examples:

* **Titelkirchen Kardinalbischöfe:**
  * Text: **Praenestin.**  
    Annotation: [Type: Titelkirche, Value: "Praenestin."]
  * Text: **Sabinen.**  
    Annotation: [Type: Titelkirche, Value: "Sabinen."]
  * Text: **Tusculan.**  
    Annotation: [Type: Titelkirche, Value: "Tusculan."]
* **Titelkirchen Kardinalpriester:**
  * Text: **S. Caeciliae**  
    Annotation: [Type: Titelkirche, Value: "S. Caeciliae"]
  * Text: **S. Chrysogoni**  
    Annotation: [Type: Titelkirche, Value: "S. Chrysogoni"]
  * Text: **S. Clementis**  
    Annotation: [Type: Titelkirche, Value: "S. Clementis"]
  * Text: **Ss. IV Coronatorum**  
    Annotation: [Type: Titelkirche, Value: "Ss. IV Coronatorum"]
  * Text: **S. Crucis in Jerusalem**  
    Annotation: [Type: Titelkirche, Value: "S. Crucis in Jerusalem"]
  * Text: **S. Cyriaci**  
    Annotation: [Type: Titelkirche, Value: "S. Cyriaci"]
  * Text: **Ss. Joannis et Pauli**  
    Annotation: [Type: Titelkirche, Value: "Ss. Joannis et Pauli"]
  * Text: **S. Laurentii in Damaso**  
    Annotation: [Type: Titelkirche, Value: "S. Laurentii in Damaso"]
  * Text: **S. Laurentii in Lucina**  
    Annotation: [Type: Titelkirche, Value: "S. Laurentii in Lucina"]
  * Text: **S. Marcelli**  
    Annotation: [Type: Titelkirche, Value: "S. Marcelli"]
  * Text: **Ss. Marcellini et Petri**  
    Annotation: [Type: Titelkirche, Value: "Ss. Marcellini et Petri"]
  * Text: **S. Marci**  
    Annotation: [Type: Titelkirche, Value: "S. Marci"]
  * Text: **S. Mariae trans Tiberim**  
    Annotation: [Type: Titelkirche, Value: "S. Mariae trans Tiberim"]
  * Text: **S. Martini in montibus**  
    Annotation: [Type: Titelkirche, Value: "S. Martini in montibus"]
  * Text: **Ss. Nerei et Achillei**  
    Annotation: [Type: Titelkirche, Value: "Ss. Nerei et Achillei"]
  * Text: **S. Nicolai ad (inter) imagines**  
    Annotation: [Type: Titelkirche, Value: "S. Nicolai ad (inter) imagines"]
  * Text: **S. Petri ad vincula**  
    Annotation: [Type: Titelkirche, Value: "S. Petri ad vincula"]
  * Text: **S. Praxedis**  
    Annotation: [Type: Titelkirche, Value: "S. Praxedis"]
  * Text: **S. Priscae**  
    Annotation: [Type: Titelkirche, Value: "S. Priscae"]
  * Text: **S. Pudentianae**  
    Annotation: [Type: Titelkirche, Value: "S. Pudentianae"]
  * Text: **S. Sabinae**  
    Annotation: [Type: Titelkirche, Value: "S. Sabinae"]
  * Text: **Ss. Silvestri et Martini**  
    Annotation: [Type: Titelkirche, Value: "Ss. Silvestri et Martini"]
  * Text: **S. Sixti**  
    Annotation: [Type: Titelkirche, Value: "S. Sixti"]
  * Text: **S. Stephani in Coelio monte**  
    Annotation: [Type: Titelkirche, Value: "S. Stephani in Coelio monte"]
  * Text: **S. Susannae**  
    Annotation: [Type: Titelkirche, Value: "S. Susannae"]
  * Text: **S. Vitalis**  
    Annotation: [Type: Titelkirche, Value: "S. Vitalis"]
* **Titelkirchen Kardinaldiakone:**
  * Text: **S. Adriani**  
    Annotation: [Type: Titelkirche, Value: "S. Adriani"]
  * Text: **S. Agathae**  
    Annotation: [Type: Titelkirche, Value: "S. Agathae"]
  * Text: **S. Angeli in foro piscium**  
    Annotation: [Type: Titelkirche, Value: "S. Angeli in foro piscium"]
  * Text: **Ss. Cosmae et Damiani**  
    Annotation: [Type: Titelkirche, Value: "Ss. Cosmae et Damiani"]
  * Text: **S. Eustachii**  
    Annotation: [Type: Titelkirche, Value: "S. Eustachii"]
  * Text: **S. Georgii ad velum aureum**  
    Annotation: [Type: Titelkirche, Value: "S. Georgii ad velum aureum"]
  * Text: **S. Luciae in Orthea (Silice)**  
    Annotation: [Type: Titelkirche, Value: "S. Luciae in Orthea (Silice)"]
  * Text: **S. Luciae in Septemsoliis**  
    Annotation: [Type: Titelkirche, Value: "S. Luciae in Septemsoliis"]
  * Text: **S. Mariae in Aquiro**  
    Annotation: [Type: Titelkirche, Value: "S. Mariae in Aquiro"]
  * Text: **S. Mariae in Cosmedin**  
    Annotation: [Type: Titelkirche, Value: "S. Mariae in Cosmedin"]
  * Text: **S. Mariae novae**  
    Annotation: [Type: Titelkirche, Value: "S. Mariae novae"]
  * Text: **S. Mariae in Porticu**  
    Annotation: [Type: Titelkirche, Value: "S. Mariae in Porticu"]
  * Text: **S. Mariae in via lata**  
    Annotation: [Type: Titelkirche, Value: "S. Mariae in via lata"]
  * Text: **S. Nicolai in carcere Tulliano**  
    Annotation: [Type: Titelkirche, Value: "S. Nicolai in carcere Tulliano"]
  * Text: **Ss. Sergii et Bacchi**  
    Annotation: [Type: Titelkirche, Value: "Ss. Sergii et Bacchi"]
  * Text: **S. Theodori**  
    Annotation: [Type: Titelkirche, Value: "S. Theodori"]
  * Text: **Ss. Viti et Modesti**  
    Annotation: [Type: Titelkirche, Value: "Ss. Viti et Modesti"]

#### Label: Patrozinium

##### Beschreibung:
Namenspatrone von Kirchen oder Institutionen.

##### Standard Examples:

* Text: **s. Jacobi**  
  Annotation: [Type: Patrozinium, Value: "s. Jacobi"]
* Text: **b. Marie**  
  Annotation: [Type: Patrozinium, Value: "b. Marie"]
* Text: **s. Johannis bapt.**  
  Annotation: [Type: Patrozinium, Value: "s. Johannis bapt."]

#### Label: Objekt

##### Beschreibung:
unspezifizierte Objekte.

##### Standard Examples:

* Text: **alt.**  
  Annotation: [Type: Objekt, Value: "alt."]
* Text: **alt. port.**  
  Annotation: [Type: Objekt, Value: "alt. port."]
  * **Hinweis:** s. UndefinierteGnade

#### Label: Ort

##### Beschreibung:
Namen von Städten, Dörfern und Bergen (s. Notizen unten).

##### Standard Examples:

* Text: **Bodegrauen**  
  Annotation: [Type: Ort, Value: "Bodegrauen"]
* Text: Novifori **Magdeburg.**  
  Annotation: [Type: Ort, Value: "Magdeburg."]
* Text: in castro **Quernfort**  
  Annotation: [Type: Ort, Value: "Quernfort"]

##### Other Examples:
* Text: in **Rauhen** et in **Schlechthin Kulm** castris
  Annotation: [Type: Ort, Value: "Rauhen"]
  Annotation: [Type: Ort, Value: "Schlechthin Kulm"]

#### Label: OrtImplizit

##### Beschreibung:
Implizite Ortsangaben (s. Notizen unten).

##### Standard Examples:

* Text: apud. **cur.**  
  Annotation: [Type: OrtImplizit, Value: "cur."]
* Text: **ap. sed.**  
  Annotation: [Type: OrtImplizit, Value: "ap. sed."]
* Text: **Novifori** Magdeburg.  
  Annotation: [Type: OrtImplizit, Value: "Novifori"]

##### Other Examples:

* Text: in **castro** Quernfort  
  Annotation: [Type: OrtImplizit, Value: "castro"]

#### Label: Kollatur

##### Standard Examples:

* Text: ad **coll.** epp.  
  Annotation: [Type: Kollatur, Value: "coll."]
* Text: **mutatio coll.**  
  Annotation: [Type: Kollatur, Value: "mutatio coll."]

#### Label: Annaten

##### Beschreibung:
Zahlungen an den Papst für die Verleihung einer Pfründe.

##### Standard Examples:

* Text: **annat.**  
  Annotation: [Type: Annaten, Value: "annat."]
* Text: **annata**  
  Annotation: [Type: Annaten, Value: "annata"]

#### Label: Servitien

##### Beschreibung:
Zahlungen des Bischöfe und einiger Äbte an den Papst anlässlich ihrer Einsetzung.

##### Standard Examples:

* Text: **serv.**  
  Annotation: [Type: Servitien, Value: "serv."]
* Text: 5 min. **serv.**  
  Annotation: [Type: Servitien, Value: "serv."]
* Text: comm. **serv.**  
  Annotation: [Type: Servitien, Value: "serv."]

#### Label: Geldsumme

##### Beschreibung:
Geldbeträge in historischen Einheiten (Betrag und Währung).

##### Standard Examples:

* Text: **9 fl.**  
  Annotation: [Type: Geldsumme, Value: "9 fl."]

#### Label: Dauer

##### Beschreibung:
Dauer eines Dispens etc.

##### Standard Examples:

* Text: **3 an.**  
  Annotation: [Type: Dauer, Value: "3 an."]

#### Label: NonObstantien

##### Beschreibung:
Klauseln, die andere Regelungen / Tatsachen außer Kraft setzen; vgl. die Label Derogatio und DerogatioZusatz.

##### Standard Examples:

* Text: **n. o.** can. et preb.
  Annotation: [Type: NonObstantien, Value: "n. o."]
  * **Häufigkeit** 4459x in den Bänden 1-9

##### Other Examples:

* Text: **n. o.** par. eccl.
  Annotation: [Type: NonObstantien, Value: "n. o."]
  * **Häufigkeit** 2665x in den Bänden 2-4 und 6-8
* Text: **n. o.** def. nat.  
  Annotation: [Type: NonObstantien, Value: "n. o."]
  * **Häufigkeit** 1044x in den Bänden 2-4 und 6-8
* Text: **n. o.** perp. vicar.  
  Annotation: [Type: NonObstantien, Value: "n. o."]
  * **Häufigkeit** 243x nur in den Bänden 7+8
* Text: **n. o.** perp. s. c. vicar.  
  Annotation: [Type: NonObstantien, Value: "n. o."]
  * **Häufigkeit** 122x, nur in den Bänden 7-8
* Text: **n. o.** statut.  
  Annotation: [Type: NonObstantien, Value: "n. o."]
  * **Häufigkeit** 13x, nur in Band 3

#### Label: Datum

##### Beschreibung:
exakte oder ungefähre Datumsangaben

##### Standard Examples:

* Text: **9 apr. 1410**  
  Annotation: [Type: Datum, Value: "9 apr. 1410"]

#### Label: Quelle

##### Beschreibung:
Verweise auf Dokumente oder Handschriften.

##### Standard Examples:

* Text: **L 138 254v**  
  Annotation: [Type: Quelle, Value: "L 138 254v."]

## Unklare Fälle und Richtlinien zur Entscheidung

### Domic.
Im Abkürzungsverzeichnis des RG steht für domic. nur domicella/domicellus (Ritterfräulein, Stiftsdame; Knappe, Junker [kurialer Ehrentitel]), auch wenn man domicellarius (Domherr) erwarten würde.

### Doppeldeutige Begriffe
Manche Begriffe können in mehreren Kategorien fallen. Beispiel: „alt.“ kann für ein Objekt (Altar), als auch für ein kirchliches Amt (ein Altarist, also ein Priester, der Gottesdienste an diesem Altar abhält und dafür ein Einkommen erhält) stehen. Wir haben uns dazu entschieden, alt. als Objekt zu taggen. 
An dieser Stelle sollen weitere ambige Fälle gesammelt werden und unsere Entscheidungen festgehalten werden:
  - alt. = Objekt
  - par. eccl. = Institution
  - archidiac. = KirchlichesAmt
  - vic. = KirchlichesAmt

### Fit mentio
Fit mentio wird nicht getaggt.

### Klammern

Alle Angaben in Klammern, die eine Alternative darstellen, werden in den Tag ihres Bezugsausdruckes miteinbezogen, inkl. Klammern:  
- Henricus **de Gerpstede (Gherbstede)** -> Namenszusatz: de Gerpstede (Gherbstede)
- **Erhardus (Gerardus)** -> Vorname: Erhardus (Gerardus)
- **24 oct. 13 (20 sept. 1413)** -> Datum: 24 oct. 13 (20 sept. 1413)
- **056 148 (ASO 2 11).** -> Quelle: 056 148 (ASO 2 11).  
Bei “frei stehenden” Angaben in Klammern werden die Klammern ignoriert.  
- (**33,33 fl.**) -> Geldsumme: 33,33 fl.
- (procur. mag. Bruno Boghel) -> Verwaltungsamt: procur.; Bildung: mag.; Vorname: Bruno; Namenszusatz: Boghel  

### Kombinationen aus mehreren Kategorien
Ein Eintrag, der mehrere Entitäten beschreibt, wird in entsprechende Einzelannotationen aufgeteilt.
  * Beispiel: Text: can. et preb. eccl. Sleswic.
    Annotation:
    - [Type: KirchlichesAmt, Value: "can. et preb."]
    - [Type: Institution, Value: "eccl."]
    - [Type: Diözese, Value: "Sleswic."]

### Lect.
Bei der Abkürzung "lect." gibt es (wenigstens für das RG 3) noch Klärungsbedarf, weil es selten für Lektor und häufiger für einen Vermerk zum Geschäftsgang (lectio) zu stehen scheint. Wenn lect. am Ende des Regests steht, dann wird es nicht ausgezeichnet.

### maior und minor prebenda / ecclesia
Bei Fällen wie „incorp. maioris preb. eccl.“, bei denen nicht immer gleich klar ist, ob sich das Adjektiv maior/minor auf die Präbende oder die Kirche bezieht, wird es grundsätzlich gemeinsam mit preb. mit dem Tag „KirchlichesAmt“ versehen (also nicht zu eccl. gezogen). 

### Ort vs. Diözese
- Steht nach der Angabe der Weihe (subdiac, diac., presb. , ep. etc.) der Name einer Stadt so muss diese als Diözese getaggt werden, weil Weihen auf Diözesen, nicht auf Städte erfolgen.
  - Beispiele: Henricus de Bocholdia al. d. Foet cler. Traiect.; ep. Vulterran. 
  - Achtung: Bei prepos. Plocen. wird Plocen. als Ort, nicht als Diözese, getaggt.
- Die Ortsbezeichnungen nach e.m. (extra muros = außerhalb der Mauern von) werden immer als Ort getaggt, z.B. e.m. Traiect.
- In Fällen wie “Prag. et Olumuc. dioc.” Ist davon auszugehen, dass das erste dioc. Weggefallen ist. Es werden also sowohl Prag. als auch Olumuc. als Diözesen getaggt.
- Wenn marchio (Markgraf) vor Brandenburg. steht, wird Brandenburg. als Verwaltungseinheit (nicht als Ort oder Diözese) getaggt.

### Präpositionen

Die Präposition *de* wird nur beim Label Namenszusatz und SozialerStand mitgetaggt: 
* Johannis **de Yselsteine** (de Yselsteine = Namenszusatz), Ghiselbertus de Lochorst **de nob. gen.** (de nob. gen. = SozialerStand)    
In allen anderen Fällen wird nur der relevante Hauptbegriff annotiert, nicht die Präposition:  
* **de eccl.** (eccl. = Institution), **de locis interdictis** (locis interdictis = UndefinierteGnade) etc.  

Entsprechendes gilt für weitere Präpositionen wie post ob. etc.

### Quellen
Für jede Quelle wird je ein Tag „Quelle“ vergeben, z.B. *C 1 4* (Quelle), *Ind. 323 127.* (Quelle)
Aber: *047 40 et 40v.* wird als eine Quelle getaggt.

### Thematische- / Topik-Tags
Wir haben uns aus zeitökonomischen Gründen dazu entschieden, keine thematischen Tags zu vergeben (z.B. „Geburtsdefekt“ für def. nat., „Interdikt“ für locis interdictis, „Ehe“ für matrim. usw.). Allerdings sollen die Nutzer/innen der fertigen Anwendung explizit darauf hingewiesen werden, dass sie bestimmte Themen, wie gewohnt, über die entsprechenden RG-Abkürzungen abrufen können. 
Beispielanfrage (falsch): Gib mir alle Ehefälle aus dem RG aus.
Beispielanfrage (richtig): Gib mir alle matrim. Fälle aus dem RG aus.

### Titelkirchen
Da die Namen derjenigen Kirchen, die Kardinalbischöfen, -priestern und -diakonen mit ihrer Ernennung zum Kardinal verliehen wurden, eine Mischform zwischen den Tags „Institution“, „Ort“ und „Patrozinium“ darstellen und ihre Anzahl zugleich finit ist, haben wir uns für einen eigenen Tag „Titelkirche“ entschieden. Man erkennt sie v.a. daran, dass in ihrer Nähe im Regest ein Kardinal genannt wird (ep. card., presb. card., diac. card.). In diesen Fällen wird ausnahmsweise darauf verzichtet, zusätzlich das Patrozinium oder den Ort als solche gesondert zu taggen. Beispiele: 
- presb. card. **tit. s. Laurentii in Damaso**
- diac. card. (tit.) **s. Georgii ad Velum Aureum**
- ep. **Portuen.** card.

### Ungünstige Trennung von zwei oder mehreren Wörtern
Manchmal kommt es vor, dass zwei Wörter, die eigentlich gemeinsam getaggt werden sollten (m. incorp.; ep. card.), durch andere Wörter getrennt werden (m. (Sigismundo Rom. Et Vng. rege) incorp.; ep. Portuen. card.). Behelfsmäßig haben wir jetzt beide Teile einzeln mit dem Tag Incorporatio bzw. KirchlichesAmt versehen - eine Lösung dafür muss noch gefunden werden, damit die Zuordnung eindeutig und konsistent ist (z.B. Pfeilverbindungen in Inception, die anzeigen, dass zwei Wörter zusammen unter ein Tag gehören).(?)

### Unklare oder vage Ortsangaben
Begriffe wie „apud cur.“ (an der Kurie), „Noviforum“ (Neumarkt) und „castrum“ (Burg) werden als "OrtImplizit" erfasst.

### Zusätze
Die Tags AbsolutioZusatz, CassatioZusatz, DispensatioZusatz, FacultasZusatz, LicentiaZusatz und ProrogatioZusatz dienen der Kennzeichnung des jeweiligen Gnadeninhalts im Regest (Bsp. s. jeweils oben). Wir verfahren so, dass der gesamte Gnadeninhalt, der oft bis zur Datumsangabe reicht, getaggt wird, nicht nur einzelne Wörter, da dieses Vorgehen sich bei mehreren Annotatoren als fehleranfälliger erwiesen hat. Beispiele: 
- LicentiaZusatz: lic. **retin. scolast., can. et par. eccl. ad 5 an.** 24 iul. 1409; nicht nur: **retin.** oder **retin. scolast.**
- ProrogatioZusatz: cum prorog. **term. solut. ad 1 an. propter incertitudinem taxe** 14 dec. 1409; nicht nur: **term.** oder **term. solut.**
