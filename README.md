Guida all'utilizzo:

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
        un nuovo file denominato 'output.xml'. Per poterlo utilizzare devi procedere cosi':
            Apri il file 'tour.html' con un editor di testo e modificare la seguente stringa:
                embedpano({xml:"tour.xml", target:"pano", html5:"only", mobilescale:1.0, passQueryParameters:"startscene,startlookat"});
            in:
                embedpano({xml:"output.xml", target:"pano", html5:"only", mobilescale:1.0, passQueryParameters:"startscene,startlookat"});
