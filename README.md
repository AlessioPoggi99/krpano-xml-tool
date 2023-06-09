# krpano-xml-tool

Questo tool automatizza alcune modifiche applicabili al file xml ottenuto come output da krpano. Dopo avere selezionato la cartella del progetto krpano offre la possibilita' di:

    * scelta scena iniziale tramite il nome (es: R0010318)
    * inserimento di un logo con relativa scelta della posizione sullo schermo e relativa scala di ingrandimento
    * inserimento immagine di una pianta con relativa scelta della posizione sullo schermo e scala di ingrandimento 
      (la pianta ha la funzionalita' di ingrandirsi al click sulla stessa), inoltre:
        * inserimento hotspots sull'immagine della pianta
        * aggiunta radar su hotspot attivo che segue l'orientamento della visuale
        
N.B. Per aggiungere gli hotspot sulla pianta è necessario fornire al programma un file txt contenente la lista di ogni scena presente nel tour e relative coordinate X e Y dell'hotspot sull'immagine della pianta selezionata. Esempio file coordinate:
```txt
R0011068,580.2671,304.1169
R0011070,578.2679,251.4617
R0010327,349.3598,347.9781
R0011071,654.2438,341.1190
R0010324,418.6995,373.6220
R0011067,584.7013,369.5214
R0010316,465.0760,254.7118
R0010318,532.8588,252.2776
```


#### Guida all'installazione:
    
    1 - Installare python3
    2 - Aprire una finestra di terminale e navigare nella cartella della repository
    3 - Eseguire i seguenti comandi:
```sh

        python3 -m venv venv
        source venv/bin/activate
        pip3 install -r requirements.txt

```
    4 - Modificare il file 'venv/lib/site-packages/bs4/__init__.py', cercare la funzione 'new_tag' e sostituire
        il parametro 'name' in 'namee', sia nella lista dei parametri della funzione, sia nel return statment


#### Creazione eseguibile:

Per dispositivi UNIX:
```sh
pyinstaller --windowed --name="KrPano - XML tool" --icon="assets/icon.icns" --add-data="assets:assets" --onefile app.py
```
Per dispositivi WINDOWS:
```sh
pyinstaller --windowed --name="KrPano - XML tool" --icon="assets/icon.ico" --add-data="assets;assets" --onefile app.py
```


#### Guida all'utilizzo:

    1 - Selezionare una cartella contenente un progetto krpano
    2 - Dopo aver selezionato la cartella del progetto c'e' la possibilita' di scegliere
        cosa aggiungere al file xml originale, e' possibile aggiungere:
            1 - La scena iniziale
            2 - Un logo
            3 - Una mini mappa ingrandibile (pianta) sulla quale poter aggiungere:
                1 - Hotspot a partire da un file di coordinate formattato nel seguente modo:
                    es. NOME_SCENA,X_COORD,Y_COORD
                2 - Radar

    3 - Per molti elementi e' possibile anche scegliere una scala e la posizione sullo schermo
    4 - Premendo il tasto di generazione dell'xml il programma copierà nelle cartelle del tuo
        progetto krpano tutti i file necessari al funzionamento di questo tool, inoltre creera'
        un nuovo file denominato 'output.xml'. Infine modificherà il file 'tour.html' facendo si che vada a leggere direttamente il file 'output.xml'. N.B Se stai usando la v1.0.0 devi modificare manualmente il file 'tour.html' e sostituire la stringa tour.xml in output.xml
        
     
#### Screenshots:

![Alt text](./screenshoots/screen-macos.png?raw=true "Macos screenshot")

![Alt text](./screenshoots/screen-win.jpeg?raw=true "Windows screenshot")
