# Filigrana_Bot
Bot per convertire e filigranare file di vario tipo

# Funzionamento
L'utente manda il file che desidera convertire e il bot una volta ricevuto estrae le impostazioni dell'utente per poter eseguire il processo di conversione e filigrana, la conversione avviene in ogni caso, la filigrana solo se il flag è messo su on, inoltre il bot filigrana con la primaria o la secondaria a seconda dello stato del flag "logo".
La filigrana ha l'opacità standard se non specificata dal comando predisposto.
::::::::::::::
Per usare due tipi di filigrana è necessario creare due filigrane dimensione A4 sia orizontali che verticali.
Per il sistema di opacità è necessario creare per ogni livello di opacità un pdf contenente la filigrana desiderata con quel livello di opacità, in questo modo il bot potrà usare i file pdf per far scegliere all'utente il livello di opacità.

# Comandi Disponibili
1. /filigrana : Permette all'utente di settare un flag on/off per filigranare o no il file.
2. /logo : Permette all'utente di settare uno switch on/off per filigranare o no con una filigrana secondaria.
3. /opacity {valore} : Permette all'utente di impostare un valore di opacità per la filigrana compreso tra 5 e 30.
4. /help : Mostra un messaggio che riassume il funzionamento del bot all'utente.

# Implementazione
Per la realizzazione sono state utilizzate le librerie: telepot, os, pdfrw, unicodedata.
Viene inoltre utilizzato un software di sistema chiamato unoconv per la conversione dei file in pdf.

# Telepot
Una Libreria per Python che permette di gestire attraverso se stessa un bot di telegram fornendo delle funzioni che si appoggiano alle API di telegram stesso.
E' stata utilizzata per la gestione dei messaggi che un utente e il bot scambiano.

# Os
Una libreria che serve per lanciare comandi di sistema, è stata utilizzata per rinominare i file e convertirli.

# Pdfrw
Una libreria per la manipolazione dei pdf, è stata utilizzata per importare le classi PdfReader, PdfWriter, PageMerge per convertire il file, regolare la dimensione della filigrana e apporla.

# Unicodedata
Una libreria per la gestione delle stringhe, usata per ovviare al problema degli accento


# Installazione e Utilizzo
Per poter eseguire lo script sarà necessario installare le opportune librerie indicate sopra.
Per usufruire del bot è necessario inserire il percorso in cui esso potrà salvare i propri file di configurazione, inserire il TOKEN del bot che si può facilmente ottenere tramite il BotFather (Nick: @BotFather).
Fatti i dovuti cambiamenti basterà eseguire lo script python e il bot è pronto.
Per rendere il bot sempre attivo senza dover avere una sessione aperta sul pc remoto si può trasformare lo script in un servizio linux mediante la seguente guida: https://github.com/torfsen/python-systemd-tutorial
