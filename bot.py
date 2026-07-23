import discord
from discord.ext import commands, tasks
import random
import json
import os
import threading
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- SERVER WEB PER KEEP-ALIVE SU RENDER ---
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot Online!")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()


def run_http_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    server.serve_forever()


threading.Thread(target=run_http_server, daemon=True).start()

# --- CONFIGURAZIONE DISCORD ---
TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = 1529463418745258145
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# -------------------------------------------------------------
# DATABASE COMPLETO CON 360 MISSIONI SETTIMANALI (60 PER RUOLO)
# -------------------------------------------------------------
MISSIONI_SETTIMANALI = {
    "🌾 Farmer": [
        "**Scorta Alimentare**: Raccogli e deposita 10 stack (640 pezzi) di cibo cotto nel magazzino comune.",
        "**Piccolo Allevamento**: Fai riprodurre gli animali della base fino ad avere 15 mucche, 15 pecore e 15 maiali.",
        "**La Pasticceria**: Cuoci e consegna 8 Torte e 32 Torte di Zucca per il gruppo.",
        "**Apicoltore di Quartiere**: Crea un giardino con 3 alveari e raccogli 16 blocchi di miele.",
        "**Serra Automatizzata**: Costruisci o espandi una farm automatica di canna da zucchero o bambù.",
        "**Varietà Agricola**: Raccogli 3 stack di grano, carote, patate e barbabietole.",
        "**La Riserva di Lana**: Raccogli 1 stack (64 pezzi) di lana per ciascuno dei 16 colori disponibili.",
        "**La Fungaia**: Costruisci una stanza buia per la coltivazione manuale o automatica di funghi.",
        "**Pesca di Comunità**: Pescate 1 stack di pesce cotto e recupera 3 libri incantati dalla pesca.",
        "**Il Frutteto**: Pianta un frutteto dedicato e raccogli 32 mele d'oro (o normali) per il magazzino.",
        "**Cultura delle Angurie**: Raccogli e stocca 10 stack di fette di anguria e 5 stack di zucche.",
        "**Raccolta Bacche**: Crea una piantagione protetta e raccogli 5 stack di bacche dolci e luminose.",
        "**Tesori del Mare**: Colleziona 3 stack di alghe essiccate e 1 stack di cetrioli di mare.",
        "**Zuppe della Casa**: Prepara e conserva in una cassa 32 Stufati Sospetti con effetti positivi.",
        "**Grande Infornata**: Cuoci 10 stack complessivi di patate e carne di maiale.",
        "**Maneggio Reale**: Alleva e addestra 5 cavalli con velocità e salto elevati per il server.",
        "**Oasi degli Axolotl**: Trova, allevare e porta alla base 4 axolotl di colori diversi.",
        "**Carovana di Cammelli**: Trova e porta alla base una coppia di cammelli per i viaggi di gruppo.",
        "**Gli Sniffer**: Fai schiudere 2 uova di Sniffer e crea un campo per la raccolta dei loro fiori.",
        "**I Nuovi Armadilli**: Alleva 6 armadilli e raccogli 32 scaglie per le armature dei lupi.",
        "**Pannocchie e Bambù**: Raccogli 10 stack di bambù e crea 5 stack di blocchi di bambù lavorato.",
        "**Allevamento Conigli**: Crea un recinto di conigli e raccogli 32 pelli di coniglio e 8 zampe.",
        "**Stagno delle Rane**: Colleziona e porta alla base rane di tutti e 3 i biomi (caldo, freddo, temperato).",
        "**I Blocchi di Fieno**: Trasforma il grano in 5 stack di blocchi di fieno per decorare la stalla.",
        "**I Llama da Carico**: Alleva 6 llama e equipaggiali con casse e tappeti colorati.",
        "**Gatti della Città**: Addomestica 5 gatti stray dai villaggi per proteggere la base dai creeper.",
        "**La Squadra di Lupi**: Addomestica 6 lupi ed equipaggiali tutti con armature in scaglie d'armadillo.",
        "**La Voliera**: Trova e porta alla base 3 pappagalli di colori differenti.",
        "**I Piccoli Allay**: Trova e porta alla base 2 Allay per aiutarti nella raccolta delle colture.",
        "**Cactus e Tinto**: Raccogli 10 stack di cactus e fondili per ottenere tintura verde.",
        "**Ninfee e Decorazioni**: Raccogli 5 stack di ninfee dai biomi di palude per i laghetti comunitarie.",
        "**Imperatore del Miele**: Accumula 5 stack di favi e 5 stack di blocchi di miele.",
        "**L'Inchiostro del Mare**: Raccogli 5 stack di sacche d'inchiostro standard e 2 stack di inchiostro lucente.",
        "**Panetteria di Bordo**: Sforna 10 stack di pane fresco da lasciare nelle casse di benvenuto.",
        "**Pasto da Coniglio**: Cuoci 5 stack di carne di coniglio e conserva le risorse.",
        "**Pescagione Pregiata**: Pesca e cucina 5 stack di salmone e 5 stack di merluzzo.",
        "**Cavalcatura con Sella**: Alleva 5 maiali ed equipaggiali con selle e canne con carota.",
        "**I Giardini di Muschio**: Raccogli 10 stack di blocchi di muschio per il reparto builder.",
        "**Azalee in Fiore**: Coltiva e raccogli 5 stack di azalee fiorite e foglie di azalea.",
        "**I Fiori delle Spore**: Esplora le caverne rigogliose e raccogli 10 Fiori delle Spore per le decorazioni.",
        "**Legno di Mangrovia**: Pianta una palude artificiale e raccogli 10 stack di radici di mangrovia.",
        "**Riserva di Bacche Luminose**: Raccogli 5 stack di bacche luminose pendenti per le caverne comunitarie.",
        "**L'Orto Botanico**: Pianta un campo con tutti i tipi di fiori piccoli e grandi presenti nel gioco.",
        "**Cassa Alimentare**: Riempi un'intera cassa doppia con cibi di qualsiasi tipo pronti all'uso.",
        "**I Funghi Luminosi**: Raccogli 5 stack di funghi del Nether (rossi e blu) per il magazzino.",
        "**I Campi a Terrazza**: Progetta una struttura agricola a 3 livelli con acqua fluente canalizzata.",
        "**Fattoria Automatica a Uova**: Crea una struttura con tramogge che raccolga automaticamente 10 stack di uova.",
        "**Scorta per i Cani**: Cuoci e deposita 5 stack di cotolette di maiale e bistecche per i lupi del server.",
        "**Le Zucche Intagliate**: Intaglia e posiziona con torce 1 stack di zucche di Halloween attorno alla base.",
        "**I Fiori del Nether**: Raccogli 3 stack di radici del Nether e funghi enormi da piantare in superficie.",
        "**Coltivazione di Cacao**: Pianta 32 alberi della giungla con cacao e raccogli 5 stack di chicchi.",
        "**Compostaggio di Masse**: Crea 10 compostiera e produci 3 stack di farina d'ossa per il gruppo.",
        "**Il Tè di Kelp**: Cuoci 10 stack di alghe nelle fornaci per creare blocchi di alghe essiccate.",
        "**Collezione di Semi**: Raccogli 5 stack di semi di grano, zucca, anguria e barbabietola.",
        "**Fattoria delle Bacche Nere**: Raccogli 5 stack di bacche dolci usando le volpi per la raccolta automatica.",
        "**La Riserva di Pelle**: Raccogli 5 stack di pelle per la produzione di libri dell'incantatore.",
        "**Il Mercato del Cibo**: Costruisci 3 banchi di vendita trasparenti con cibo esposto in cornici.",
        "**Sospensione Acquatica**: Crea una coltura idroponica artificiale al coperto con luce di pietraluce.",
        "**Conserva di Miele**: Riempi 1 cassa singola solo con ampolle di miele per le pozioni curative.",
        "**Grande Raccolto Estivo**: Svuota e ripianta contemporaneamente 4 campi di grandi dimensioni."
    ],
    "🏗️ Builder": [
        "**Punto di Ristoro**: Costruisci una taverna o locanda decorata nei pressi dello spawn.",
        "**Torre di Guardia**: Progetta una torre d'avvistamento illuminata sul punto più alto del villaggio.",
        "**Ingresso Nether**: Decora l'interno e l'esterno del portale del Nether principale con un tema antico.",
        "**La Fontana Centrale**: Costruisci una fontana decorata con panchine per la piazza del villaggio.",
        "**Stalla Comunitaria**: Costruisci un fienile decorato per ospitare i cavalli di tutti i giocatori.",
        "**Mulino a Vento**: Costruisci un mulino a vento scenografico vicino ai campi coltivati.",
        "**Faro Costiero**: Costruisci un faro illuminato su una costa vicino alla base.",
        "**Rete Stradale**: Collega le strutture principali con sentieri in pietra, lampioni e vegetazione.",
        "**Molo di Pesca**: Costruisci un piccolo molo con capanno in legno e barchette ormeggiate.",
        "**Cimitero del Server**: Crea un cimitero scenografico con lapidi dedicate alle morti dei giocatori.",
        "**Ponte Decorato**: Progetta un ponte in pietra e legno che attraversi un fiume o un burrone.",
        "**Casa sull'Albero**: Costruisci un'abitazione nascosta tra le chiome di un grande albero della giungla.",
        "**Serra di Vetro**: Progetta una serra cupolata in vetro e mattoni per la zona del Farmer.",
        "**Fucina del Fabbro**: Costruisci una bottega da fabbro con incudini, fornaci e dettagli di lava.",
        "**La Biblioteca**: Crea un edificio dedicato agli incantesimi con scaffali e vetrate colorate.",
        "**Stanza degli Incantesimi**: Arreda e illumina la stanza del tavolo per incantesimi della base.",
        "**Facciata Magazzino**: Abbellisci l'entrata del magazzino centrale rendendola imponente.",
        "**Albero Personalizzato**: Progetta e costruisci un grande albero artificiale con foglie e recinti.",
        "**Statua della Base**: Costruisci una statua in pietra o rame che rappresenti la mascot del server.",
        "**Torre dell'Orologio**: Crea una torre alta con quadrante decorativo al centro del villaggio.",
        "**Rimessa per Barche**: Costruisci una struttura coperta sull'acqua per riporre le imbarcazioni.",
        "**Posto di Guardia**: Progetta un piccolo avamposto difensivo lungo le mura esterne.",
        "**Banco del Mercato**: Costruisci 3 bancarelle in legno con tende colorate per gli scambi.",
        "**Panetteria del Paese**: Crea un piccolo negozio decorato con forni e vetrine per il pane.",
        "**Apoteca Alchemica**: Costruisci una bottega di pozioni con alambicchi e altopiani vegetali.",
        "**Casa del Sindaco**: Progetta una casa padronale decorata da usare come punto di ritrovo.",
        "**Anfiteatro**: Costruisci una piccola gradinata in pietra per le riunioni di gruppo.",
        "**Pozzo dei Desideri**: Crea un pozzo decorato con recinzioni, secchi e dettagli di muschio.",
        "**Gazebo da Giardino**: Costruisci una struttura aperta in legno intagliato circondata da fiori.",
        "**Hub del Nether**: Progetta una stanza sicura in pietra nera attorno al portale del Nether.",
        "**Sala del Portale End**: Decora la stanza del Portale dell'End donandole un tema cosmico.",
        "**Mura di Cinta**: Costruisci un segmento di mura difensive alto 5 blocchi lungo un confine.",
        "**Stazione dei Treni**: Progetta un piccolo fabbricato per la partenza dei carrelli da miniera.",
        "**Giardino Botanico**: Crea un'area recintata con camminamenti in ghiaia e vegetazione rara.",
        "**Fattoria a Terrazze**: Progetta i muri di contenimento in pietra per i campi del Farmer.",
        "**Cascata Artificiale**: Crea un punto d'acqua scenografico su una parete di roccia con vegetazione.",
        "**Ingresso Miniera**: Decora la discesa sotterranea del Miner con travi in legno e lanterne.",
        "**Laghetto da Pesca**: Scava e abbellisci un laghetto naturale con canneti e ninfee.",
        "**Poligono Tiro con l'Arco**: Costruisci una struttura con bersagli a distanze crescenti.",
        "**La Caserma**: Costruisci un edificio con brandine e armadietti per il ruolo PvP'er.",
        "**Banca e Caveau**: Crea un piccolo edificio rinforzato in ferro per conservare i beni rari.",
        "**Stanza delle Mappe**: Progetta una sala con tavolo centrale e parete per le mappe geografiche.",
        "**Stanza dei Trofei**: Costruisci un corridoio con piedistalli per esporre le teste dei mob e i dischi.",
        "**Museo della Storia**: Crea una galleria dove esporre i primi oggetti usati nel server.",
        "**Bar sulla Spiaggia**: Costruisci un chiosco in legno di palma e paglia vicino al mare.",
        "**Padiglione degli Scambi**: Progetta un'area con banconi per effettuare scambi tra giocatori.",
        "**Gru Decorativa**: Costruisci una gru in legno ed impalcature presso il molo o il cimitero.",
        "**Mulino ad Acqua**: Crea una ruota di legno adiacente a un fiume con edificio di lavorazione.",
        "**Arena PvP**: Costruisci un piccolo ring circondato da staccionate per i duelli amichevoli.",
        "**Piccolo Teatro**: Progetta un palco in legno con sipario in lana rossa e sedute.",
        "**Faro Subacqueo**: Costruisci una cupola illuminata sotto il livello del mare con prismather.",
        "**Rovine Decorative**: Crea una struttura in rovina ricoperta di rampicanti per dare atmosfera.",
        "**Labirinto di Siepi**: Pianta e pota un piccolo labirinto in foglie vicino alla base.",
        "**Osservatorio**: Costruisci una cupola in vetro sulla montagna per l'osservazione delle stelle.",
        "**Ponte Levatoio**: Progetta la facciata di un castello con un ponte in legno sollevato.",
        "**Porta Monumentale**: Costruisci un arco d'ingresso imponente all'inizio del sentiero principale.",
        "**Capanna del Cacciatore**: Crea un rifugio in tronchi e pelli situato nel bosco.",
        "**Bagni Pubblici**: Costruisci una struttura con vasche d'acqua calda, vapore e recinzioni.",
        "**Torre del Faro Magico**: Crea una torre con cristalli di ametista e blocchi illuminati in cima.",
        "**Rifugio di Montagna**: Progetta uno chalet in legno e pietra arroccato sulla neve."
    ],
    "⛏️ Miner": [
        "**Caccia ai Diamanti**: Estrai e consegna 24 diamanti grezzi o lavorati per la cassa comune.",
        "**Stazione di Discesa**: Scava uno scalone ben illuminato e sicuro dalla superficie fino a Y = -58.",
        "**Scorta di Ferro**: Raccogli e fondi 5 stack (320 pezzi) di lingotti di ferro.",
        "**Spedizione Netherite**: Esplora il Nether e recupera 8 unità di Debris Antico.",
        "**La Caverna d'Estrazione**: Scava e organizza una grande stanza sotterranea (20x20) per l'hub.",
        "**Scorta di Rame e Lapis**: Raccogli e consegna 5 stack di rame fuso e 3 stack di lapislazzuli.",
        "**Galleria con Binari**: Costruisci una linea mineraria con binari lunga 300 blocchi a Y = -58.",
        "**Bonifica Speleologica**: Illumina completamente ed elimina i mob da una vasta caverna.",
        "**I Materiali Edili**: Raccogli 10 stack complessivi di Slate profonda, Granito, Diorite e Andesite.",
        "**L'Oro del Nether**: Esplora i livelli inferiori del Nether e porta 3 stack di lingotti d'oro.",
        "**Carbone per le Fornaci**: Estrai e deposita 10 stack di carbone grezzo nel magazzino.",
        "**Quarzo da Costruzione**: Raccogli e fondi 5 stack di quarzo del Nether per il Builder.",
        "**Geode di Ametista**: Individua una geode e raccogli 2 stack di schegge di ametista.",
        "**Fornitura di Ossidiana**: Scava in sicurezza e stocca 1 stack (64 pezzi) di ossidiana.",
        "**La Deepslate Lavorata**: Trasforma la pietra profonda estratta in 10 stack di mattoni lavorati.",
        "**Blocchi di Ferro**: Compatta i lingotti estratti fino a formare 1 stack di blocchi di ferro.",
        "**Blocchi di Rame Grezzo**: Raccogli 2 stack di blocchi di rame grezzo nelle caverne.",
        "**Riserva di Lapislazzuli**: Raccogli 1 stack di blocchi di lapislazzuli per l'incantatore.",
        "**Lingotti d'Oro**: Fondi e conserva 3 stack di lingotti d'oro presi dalle miniere naturali.",
        "**Blocchi di Diamante**: Raccogli abbastanza diamanti da formare 8 blocchi di diamante compatti.",
        "**Netherite Lavorata**: Unisci la netherite all'oro per fabbricare 4 lingotti di Netherite.",
        "**Scorta di Tufo**: Raccogli 10 stack di tufo per i progetti di costruzione moderni.",
        "**Pietra Calcite**: Trova una geode ed estrai 5 stack di calcite bianca.",
        "**Pietra Nera del Nether**: Raccogli 10 stack di pietranera (blackstone) nelle fortezze o bastioni.",
        "**Basalto Industriale**: Raccogli 10 stack di basalto naturale per le decorazioni del Nether.",
        "**Terracotta Naturale**: Esplora le caverne nei biomi caldi e raccogli 5 stack di terracotta.",
        "**Sabbia delle Anime**: Estrai 5 stack di sabbia delle anime per le coltivazioni di verruche.",
        "**Blocchi di Magma**: Raccogli 5 stack di blocchi di magma dai laghi sotterranei o dal Nether.",
        "**Spina di Pesce**: Scava 5 gallerie parallele lunghe 100 blocchi ciascuna al livello Y = -58.",
        "**Drenaggio Lava**: Svuota completamente un lago di lava sotterraneo usando la pietra.",
        "**Messa in Sicurezza**: Metti illuminazione e staccionate in 3 caverne verticali pericolose.",
        "**Hub Sotterraneo**: Scava una sala circolare con raggio di 10 blocchi al livello della bedrock.",
        "**Scorta di Selce**: Metti nelle casse del PvP'er 5 stack di selce per la fabbricazione di frecce.",
        "**Polvere di Pietrarossa**: Estrai e stocca 10 stack di polvere di pietrarossa per il Redstoner.",
        "**Cobblestone di Riserva**: Riempi 1 cassa doppia unicamente con blocchi di pietrisco.",
        "**Scavo del Mini-Chunk**: Scava un'area di 8x8 dal livello del mare fino alla bedrock.",
        "**Diorite Levigata**: Trasforma la diorite grezza estratta in 5 stack di diorite levigata.",
        "**Granito Levigato**: Trasforma il granito grezzo estratto in 5 stack di granito levigato.",
        "**Andesite Levigata**: Trasforma l'andesite grezza estratta in 5 stack di andesite levigata.",
        "**Mineshaft Abbandonata**: Trova una miniera abbandonata, bonificala e raccogli 3 stack di binari.",
        "**Blocchi di Quarzo**: Converti il quarzo estratto in 2 stack di blocchi di quarzo lisci.",
        "**Glowstone del Nether**: Raccogli 5 stack di pietraluce intatta dalle volte del Nether.",
        "**Netherrack Massiccia**: Raccogli 15 stack di roccia del Nether per le fornaci ad alta velocità.",
        "**Magazzino dei Grezzi**: Crea una stanza sotterranea per lo stoccaggio dei blocchi non lavorati.",
        "**Disattivazione Spawner**: Trova uno spawner sotterraneo, illuminalo e scava l'area attorno.",
        "**Estrazione di Argilla**: Scava nei fiumi e raccogli 5 stack di blocchi di argilla.",
        "**Sabbia delle Caverne**: Raccogli 10 stack di sabbia dai biomi sotterranei o desertici.",
        "**Ghiaia per Sentieri**: Raccogli 10 stack di ghiaia per i progetti stradali del Builder.",
        "**Mattoni di Deepslate**: Converti la pietra profonda in 10 stack di mattoni incisi.",
        "**Mattoni del Nether**: Cuoci la netherrack per produrre 5 stack di mattoni del Nether.",
        "**Area Slime**: Trova un chunk di slime sotterraneo, scava l'area e segnala le coordinate.",
        "**Pulizia della Bedrock**: Appiattisci un'area di 20x20 blocchi direttamente sulla bedrock.",
        "**Fornaci Industriali**: Costruisci una batteria di 12 fornaci ben organized nella miniera.",
        "**Pietra Levigata**: Cuoci il pietrisco per produrre 10 stack di pietra liscia standard.",
        "**Gocciolatoi e Stalattiti**: Raccogli 5 stack di blocchi di speleotema e stalattiti.",
        "**Vetro per la Base**: Cuoci la sabbia estratta per produrre 10 stack di vetro trasparente.",
        "**Pietra Nera Levigata**: Trasforma la pietra nera in 5 stack di mattoni di pietra nera lucidati.",
        "**Serbatoio d'Acqua**: Crea un serbatoio sotterraneo con acqua infinita per le spedizioni.",
        "**Scorta di Torce**: Prepara e lascia nell'hub di miniera 10 stack di torce pronte all'uso.",
        "**I Cristalli d'Ametista**: Raccogli 16 blocchi di ametista intatti usando un piccone con Tocco di Seta."
    ],
    "🧭 Explorer": [
        "**Cartografo Locale**: Completa una mappa da parete 2x2 dei dintorni della base.",
        "**Mondo Animale**: Trova e porta alla base 2 esemplari di un animale raro.",
        "**Cacciatore di Strutture**: Trova 2 strutture diverse e svuotane i bauli del bottino.",
        "**Botanico**: Raccogli e pianta vicino alla base 1 esemplare di ogni albero del gioco.",
        "**Tesoro Sommerso**: Trova una mappa del tesoro nascosto ed dissotterra il baule.",
        "**I Biomi Rari**: Individua e segna le coordinate di un bioma raro (Giungla o Mesa).",
        "**Liberazione Allay**: Ripulisci un Avamposto ed libera gli Allay portandoli a casa.",
        "**Archeologo**: Trova un sito archeologico, usa la spazzola e porta 3 frammenti di vaso.",
        "**Ricerca dello Sniffer**: Trova ed fai schiudere 1 Uovo di Sniffer dalle rovine marine.",
        "**Esplorazione Abissale**: Esplora una Magione o un Monumento e scatta uno screenshot.",
        "**La Parete Mappe**: Crea una mappa gigante 3x3 a livello di ingrandimento intermedio.",
        "**Città Antica**: Trova un'Ancient City nel Deep Dark e segna le coordinate sicure.",
        "**Fortezza del Nether**: Individua una Fortezza del Nether e traccia un percorso sicuro.",
        "**Bastione dei Piglin**: Trova un Bastione e svuota la cassa del tesoro centrale.",
        "**Città dell'End**: Trova una Città dell'End dotata di nave volante e recupera le Elitri.",
        "**Isola dei Funghi**: Trova il raro bioma Mushroom Island e porta a casa una Mooshroom.",
        "**I Ciliegi in Fiore**: Trova un bioma Cherry Grove e raccogli sapling e fiori.",
        "**I Calanchi (Badlands)**: Esplora il bioma della Mesa e raccogli 5 stack di terracotta colorata.",
        "**La Palude di Mangrovie**: Esplora una palude di mangrovie e raccogli campioni di propaganda.",
        "**Cattura Axolotl**: Trova un axolotl blu o rosa e portalo sano e salvo alla base.",
        "**I Cammelli del Deserto**: Trova un villaggio nel deserto e scorta un cammello a casa.",
        "**Armadilli delle Savane**: Trova il bioma della savana e porta a casa 2 armadilli.",
        "**Rane della Palude**: Cerca e cattura 2 rane verdi nel bioma della palude fredda.",
        "**Finiture per Armature**: Trova 3 modelli di finiture (armor trims) differenti nelle strutture.",
        "**I Dischi Musicali**: Recupera 3 dischi musicali rari dai bauli delle strutture.",
        "**Guscio di Nautilo**: Ottieni 3 gusci di nautilo dalla pesca o dagli annegati.",
        "**Il Cuore del Mare**: Riscatta il Cuore del Mare dal baule di un tesoro sepolto.",
        "**Teste di Drago**: Esplora le navi dell'End e stacca la testa di drago dalla prua.",
        "**Le Spunze Marine**: Prosciuga una stanza del Monumento e raccogli 32 spugne bagnate.",
        "**I Corni di Capra**: Fai urtare una capra contro la roccia per raccogliere 2 corni da guerra.",
        "**Il Panda Gigante**: Trova una giungla e scorta un panda fino alla base di gruppo.",
        "**L'Orso Polare**: Viaggia nei biomi congelati ed individua una famiglia di orsi polari.",
        "**L'Ocelot della Giungla**: Addomestica ed accompagna a casa un ocelot della giungla.",
        "**I Pappagalli**: Trova una giungla e porta a casa 2 pappagalli posati sulle spalle.",
        "**Cartografia dell'End**: Crea una mappa dettagliata dell'isola centrale dell'End.",
        "**Mappa del Nether**: Crea una mappa con tracciato dei portali all'interno del Nether.",
        "**Il Guardiano Warden**: Trova un sensore Sculk, attivalo e scatta una foto al Warden prima di fuggire.",
        "**L'Elder Guardian**: Sconfiggi 1 Elder Guardian nel monumento e recupera la spugna.",
        "**I Relitti Sommersi**: Trova ed esplora 3 relitti di navi affondate sotto l'oceano.",
        "**Piramidi del Deserto**: Trova 2 piramidi del deserto ed disattiva le trappole a TNT.",
        "**Templi della Giungla**: Risolvi il puzzle a leve di 2 templi della giungla e prendi il bottino.",
        "**Avamposti dei Saccheggiatori**: Trova 2 avamposti e ruba lo stendardo del Capitano.",
        "**I Fiori Rari**: Raccogli 1 esemplare di Orchidea Blu, Allium e Margherita dei Campi.",
        "**I Sapling del Mondo**: Colleziona 1 alberello per ognuno degli 8 tipi di alberi esistenti.",
        "**Foto nei Biomi**: Scatta uno screenshot del tuo personaggio in 10 biomi differenti.",
        "**Sabbia Sospetta**: Spazzola 10 blocchi di sabbia sospetta nelle rovine del deserto.",
        "**Ghiaia Sospetta**: Spazzola 10 blocchi di ghiaia sospetta nelle rovine oceaniche.",
        "**Fiori di Chorus**: Raccogli 1 stack di fiori di Chorus dalle isole esterne dell'End.",
        "**Portali Diroccati**: Trova 3 portali del Nether diroccati e svuotane le casse d'oro.",
        "**Rovine Oceaniche**: Esplora un villaggio sommerso ed elimina gli annegati all'interno.",
        "**I Picchi di Ghiaccio**: Trova il bioma Ice Spikes e raccogli 2 stack di ghiaccio compatto.",
        "**Caverne Rigogliose**: Esplora una Lush Cave e raccogli muschio, azalee e bacche.",
        "**Caverne di Stalattiti**: Trova una Dripstone Cave e mappa l'estensione della caverna.",
        "**L'Isola Solitaria**: Trova un'isola nell'oceano distante almeno 1000 blocchi dallo spawn.",
        "**I Geyser del Nether**: Esplora il bioma del Delta di Basalto e segna i punti di interesse.",
        "**La Foresta Rossa**: Esplora la Crimson Forest e recupera 2 stack di steli cremisi.",
        "**La Foresta Blu**: Esplora la Warped Forest e raccogli 2 stack di steli distorti.",
        "**La Valle delle Anime**: Trova la Soul Sand Valley e raccogli 2 stack di blocchi d'ossa.",
        "**Ricerca delle Maschere**: Recupera una testa di Zombie, Scheletro o Creeper dai bauli.",
        "**Esplorazione Polare**: Trova un iceberg gigante ed erigi un piccolo faro di segnalazione."
    ],
    "⚙️ Redstoner": [
        "**Smistamento Base**: Costruisci uno smistamento automatico per 6 materiali principali.",
        "**Porta Segreta**: Realizza un passaggio segreto a pistoni 2x2 per accedere a una zona riservata.",
        "**Magazzino Smaltimento**: Crea un cestino della spazzatura a lava/cactus automatizzato.",
        "**Illuminazione Automatica**: Crea un circuito con sensore solare che accenda le luci di notte.",
        "**Farm di Pollo**: Costruisci una farm automatica di pollo cotto ed uova compatto.",
        "**Ascensore Ad Acqua**: Crea un sistema di risalita e discesa rapida con blocchi di sabbia delle anime e magma.",
        "**Campanello della Base**: Costruisci un circuito con Noteblock che suoni una melodia all'ingresso.",
        "**Farm di Zucche e Angurie**: Costruisci un circuito automatico con Observer e pistoni.",
        "**Faro con Luci Alternate**: Progetta un circuito che faccia alternare le luci del faro di base.",
        "**Mercato Automatico**: Crea un sistema di scambio in cui inserire un oggetto per riceverne un altro.",
        "**Smistamento Avanzato**: Espandi lo smistamento automatico portandolo a 12 oggetti differenti.",
        "**Porta 3x3 a Pistoni**: Costruisci una porta circolare 3x3 a pistoni completamente scomparsa.",
        "**Farm di Canna da Zucchero**: Progetta una farm ad alta velocità a pistoni ed Observer a 2 piani.",
        "**Farm di Bambù**: Crea una colonna automatica per la raccolta continua di bambù.",
        "**Smistatore di Dischi**: Crea un sistema a tramogge che separi i dischi musicali dagli altri oggetti.",
        "**Farm di Ferro Compattata**: Costruisci una farm di ferro con villici e zombie per il Miner.",
        "**Farm di Lana Automatica**: Progetta una farm con distributori e cesoie per le pecore colorate.",
        "**Farm di Miele Automatica**: Crea un sistema con comparatori per raccogliere ampolle di miele.",
        "**Allevamento Villici**: Crea una struttura automatizzata per fare riprodurre i villici con le lettiere.",
        "**Poligono con Punteggio**: Progetta un bersaglio con Noteblock e lampade che mostrino la precisione.",
        "**Loop Musicale**: Crea un circuito a ripetizione che suoni un brano famoso con i Noteblock.",
        "**Timer ad Imbuti**: Costruisci un orologio di redstone ad imbuti regolabile per le farm.",
        "**Trappola a Trabocchetto**: Crea una botola a pistoni azionata da una pedana per la sicurezza.",
        "**Generatore di Basalto**: Costruisci una macchina che generi basalto usando ghiaccio blu e lava.",
        "**Generatore di Cobblestone**: Crea una farm automatica di pietra con pistoni di spinta.",
        "**Farm di Ghiaccio**: Crea un sistema ad acqua che congeli i blocchi e li spinga per il piccone.",
        "**Contatore di Entità**: Crea un circuito che numeri i carrelli o i giocatori che attraversano un varco.",
        "**Stazione a Pulsante**: Progetta una stazione ferroviaria dove il carrello arriva a chiamata.",
        "**Porta Dietro il Quadro**: Crea un passaggio segreto che si apre lanciando un oggetto contro un quadro.",
        "**Ponte Levatoio a Pistoni**: Costruisci un ponte che si alza nascondendo la lava sottostante.",
        "**Allarme Intrusione**: Crea un circuito con fili d'inciampo che attivi campanelli di avviso.",
        "**Farm di Alghe Automatica**: Progetta un sistema a pistoni subacqueo per la raccolta di alghe.",
        "**Farm di Cactus Automatica**: Crea una struttura a griglia per raccogliere cactus appena crescono.",
        "**Distributore di Cibo**: Crea un pulsante in mensa che eroghi un cibo casuale da una cassa.",
        "**Vestizione Rapida**: Costruisci una pedana con 4 distributori per indossare l'armatura al volo.",
        "**Illuminazione a Sequenza**: Crea una linea di lampade di redstone che si accendono in successione.",
        "**Scarico Carrelli Automatico**: Crea una stazione che svuoti i carrelli con tramoggia e li rimandi indietro.",
        "**Montacarichi a Pistoni**: Costruisci un ascensore a pistoni spingitori per salire di 10 blocchi.",
        "**Spegnimento Portale**: Crea un circuito con distributori di secchi d'acqua per spegnere il portale.",
        "**Riaccensione Portale**: Crea un circuito con carica di fuoco per riaccendere il portale a pulsante.",
        "**Farm di Funghi**: Progetta un sistema ad acqua azionato da una leva per raccogliere funghi.",
        "**Cassaforte a Noteblock**: Crea una porta che si apra solo suonando una sequenza di 3 note precise.",
        "**Porta con Codice**: Progetta un sistema con 4 leve che richieda la combinazione esatta.",
        "**Indicatore di Livello**: Crea un indicatore a lampade di redstone collegato a una cassa tramite comparatore.",
        "**Circuito Anti-AFK**: Costruisci una piscina d'acqua ad anello con correnti per i giocatori in pausa.",
        "**Distributore Pozioni**: Crea un banco alchemico con 4 pulsanti per erogare ingredienti precisi.",
        "**Farm di Fiori**: Progetta un sistema con distributore di farina d'ossa e pistoni spingitori.",
        "**Trinciatrice Legna**: Crea una parete di spinta a pistoni per accumulare i tronchi piazzati.",
        "**Farm di Neve**: Costruisci una cabina con un pupazzo di neve e un sistema di spinta a pistone.",
        "**Porta 4x4 Imponente**: Progetta un portone 4x4 a pistoni per l'ingresso delle mura comunitarie.",
        "**Ponte Retrattile**: Crea un passaggio in pietra che si ritrae completamente sotto la lava.",
        "**Trappola a Caduta**: Crea una fossa azionata da pistoni per difendere l'ingresso principale.",
        "**Ascensore Slimeblock**: Costruisci un sistema di lancio verso l'alto usando blocchi di slime e pistoni.",
        "**Lanciatore di Barche**: Crea un circuito che rilasci una barca sul canale d'acqua a comando.",
        "**Indicatore Notte/Giorno**: Costruisci due lampade (Sole e Luna) che mostrino la fase della giornata.",
        "**Farm di Muschio**: Crea un sistema automatizzato con farina d'ossa ed acqua per raccogliere muschio.",
        "**Cestino con Suono**: Crea uno smaltitore che suoni una nota di noteblock quando distrugge un oggetto.",
        "**Semaforo per Binari**: Crea uno scambio ferroviario visivo con lampade rosse e verdi.",
        "**Farm di Glow Berries**: Progetta un sistema ad Observer per raccogliere le bacche pendenti.",
        "**Griglia di Sicurezza**: Costruisci una serie di barre di ferro che scendono dal soffitto a leva."
    ],
    "⚔️ PvP'er / Soldato": [
        "**Scorta per i Beacon**: Raccogli 16 Verghe di Blaze e 3 Teste di Wither Scheletro.",
        "**Difesa del Villaggio**: Trova un capitano, avvia e vinci 1 Incursione salvando i villici.",
        "**Pulizia Notturna**: Sconfiggi 80 mob ostili e stocca le loro risorse nel magazzino.",
        "**Arsenale di Base**: Forgia e incanta al massimo 2 spade in diamante per l'armeria.",
        "**Caccia ai Ghast**: Pattuglia il Nether ed elimina 10 Ghast recuperando le lacrime.",
        "**Muro di Difesa**: Costruisci una trincea o palizzata lungo i confini della base.",
        "**Poligono di Tiro**: Costruisci un bersaglio e fornisci 5 stack di frecce all'armeria.",
        "**Igiene degli Scheletri**: Pattuglia di notte e raccogli 5 stack di ossa e polvere da sparo.",
        "**Cacciatore di Warden**: Esplora l'Ancient City, affronta o eludi lo Warden e torna alla base.",
        "**Fortezza del Nether**: Costruisci una roccaforte attorno al portale dal lato del Nether.",
        "**Archi d'Elite**: Forgia e incanta 2 archi con Potenza IV e Impatto II per l'armeria.",
        "**Elmi Protettivi**: Prepara 2 elmi in diamante con Protezione IV e Respirazione III.",
        "**Corazze da Guerra**: Fabbrica 2 corazze in diamante con Protezione IV per la squadra.",
        "**Schinieri Rinforzati**: Crea 2 paia di schinieri in diamante incantati per la truppa.",
        "**Stivali da Esplorazione**: Prepara 2 paia di stivali in diamante con Atterraggio Morbido IV.",
        "**Eroe Plurimo**: Partecipa e vinci 2 Incursioni (Raid) a livello di difficoltà normale/difficile.",
        "**Caccia ai Creeper**: Elimina 20 Creeper prima che esplodano e raccogli la polvere da sparo.",
        "**Pulizia dei Cieli**: Sconfiggi 20 Phantom durante le notti insomne e raccogli le membrane.",
        "**Membrane di Phantom**: Deposita 10 membrane di Phantom nell'armeria per riparare le elitri.",
        "**I Magma Cube**: Elimina 15 Magma Cube nel Nether e raccogli 3 stack di creme di magma.",
        "**Caccia agli Enderman**: Pattuglia di notte ed elimina 20 Enderman raccogliendo le perle.",
        "**Perle di Ender**: Accumula 32 perle di Ender nella cassa delle emergenze dell'armeria.",
        "**Guardiano Abissale**: Sconfiggi 1 Elder Guardian nel Monumento dell'Oceano.",
        "**I Gusci di Nautilo**: Ottieni 5 gusci di nautilo eliminando gli annegati con conchiglia.",
        "**Tridente da Combattimento**: Recupera un tridente dagli annegati e incantalo con Lealtà III.",
        "**Frecce Spettrali**: Unisci la polvere di pietraluce alle frecce per creare 3 stack di frecce spettrali.",
        "**Pozioni di Guarigione**: Prepara 1 stack (16 bottiglie) di Pozioni di Guarigione Istantanea II.",
        "**Pozioni di Forza**: Prepara 1 stack di Pozioni di Forza II per le battaglie del server.",
        "**Pozioni di Velocità**: Cucinare 1 stack di Pozioni di Velocità II da lasciare nell'armeria.",
        "**Gli Husk del Deserto**: Sconfiggi 40 Husk nei biomi desertici e ripulisci l'area.",
        "**Gli Stray dei Ghiacci**: Sconfiggi 40 Stray nei biomi congelati e raccogli le frecce lente.",
        "**Annegati Pericolosi**: Sconfiggi 10 annegati armati di tridente senza morire.",
        "**Assalto all'Avamposto**: Ripulisci interamente un Avamposto dei Saccheggiatori.",
        "**Armatura in Netherite**: Trasforma 1 set di armatura in diamante in Netherite incantata.",
        "**Scontro con il Wither**: Evoca e sconfiggi il Wither nel Nether per ottenere la Stella del Nether.",
        "**Stella del Nether**: Deposita 1 Stella del Nether nella cassa forte per il futuro Beacon.",
        "**Torretta d'Avvistamento**: Costruisci una torretta difensiva elevata con riserva di frecce.",
        "**Turno di Guardia**: Pattuglia il perimetro della base per 3 notti consecutive eliminando i mob.",
        "**Scorta al Farmer**: Accompagna il Farmer durante una spedizione di caccia o esplorazione.",
        "**Scorta al Miner**: Proteggi il Miner durante lo scavo di una caverna complessa.",
        "**Rastrelliera Armature**: Costruisci un'armeria decorata con 8 rastrelliere e armature di ferro.",
        "**Scudi con Stendardo**: Fabbrica 5 scudi incantati e personalizzati con lo stendardo del server.",
        "**Fornitura TNT**: Fabbrica e deposita 32 blocchi di dinamite (TNT) per le demolizioni.",
        "**Trincea Anti-Mob**: Scava una trincea profonda 3 blocchi ricoperta di ragnatele attorno alla base.",
        "**I Ravager**: Sconfiggi 3 Ravager (i tori dei saccheggiatori) durante i Raid.",
        "**Stendardi della Vittoria**: Raccogli ed esponi nell'armeria 5 stendardi dei capitani saccheggiatori.",
        "**Poligono Mobile**: Costruisci un percorso di tiro con bersagli azionati a redstone.",
        "**Mele d'Oro da Guerra**: Prepara e conserva 16 mele d'oro per le spedizioni ad alto rischio.",
        "**Asse da Guerra**: Forgia 2 asce in diamante incantate con Affilatezza V e Infrangibilità III.",
        "**Trappola per Ostili**: Costruisci un punto di neutralizzazione sicuro per i mob notturni.",
        "**Gli Shulker dell'End**: Ripulisci una Città dell'End e raccogli 16 gusci di Shulker.",
        "**Scatole di Shulker**: Fabbrica 4 casse di Shulker per i trasporti tattici del gruppo.",
        "**Bonifica Notturna**: Ripulisci completamente da solo un bioma intero durante la notte.",
        "**Protezione Villici**: Costruisci una recinzione rinforzata attorno al villaggio principale.",
        "**Cassa Munizioni**: Riempi 1 cassa singola unicamente con frecce e Fuochi d'Artificio per balestre.",
        "**Raid al Bastione**: Ripulisci la zona centrale di un Bastione dai Piglin Brute.",
        "**Balestre Multi-Tiro**: Forgia 2 balestre incantate con Tiro Multiplo e Ricarica Rapida.",
        "**Fumo da Copertura**: Fabbrica 1 stack di bombe fumogene (usando pozioni d'invisibilità o cecità).",
        "**Manutenzione Armeria**: Ripara e reincanta tutte le armi danneggiate rimaste nelle casse comunitarie.",
        "**Campione del Server**: Sconfiggi 100 mob ostili totali registrando le risorse nello stoccaggio."
    ]
}

# -------------------------------------------------------------
# DATABASE MISSIONI MENSILE (1 SOLA ESTRATTA A CASO AL MESE)
# -------------------------------------------------------------
MISSIONI_MENSILE_LISTA = [
    "🐉 **Il Cacciatore di Draghi:** Sconfiggete l'Ender Dragon 3 volte.",
    "⛏️ **Lo Scavatore Folle:** Raccogliete 10.000 blocchi di Pietra o Ardesia Profonda.",
    "💎 **Febbre del Diamante:** Trovate e minate 100 minerali di Diamante grezzo.",
    "🌾 **L'Agricoltore Supremo:** Raccogliete 5.000 unità di Grano, Carote o Patate.",
    "🧟 **Difensore del Reame:** Uccidete 500 mob ostili (Zombie, Scheletri, Creeper).",
    "🗺️ **L'Esploratore:** Trovate e saccheggiate un'Antica Città (Ancient City), sconfiggete il Warden e razziate una Trial Chamber.",
    "🤝 **Il Mercante:** Completate 100 scambi con i Villager.",
    "🔥 **Maestro del Nether:** Ottenete 50 frammenti di Netherite.",
    "🎣 **Pesca Miracolosa:** Pescate 200 oggetti (Pesci, Libri, Tesori).",
    "🐄 **L'Allevatore:** Fate riprodurre 150 animali nella tua farm.",
    "🏰 **L'Architetto:** Costruite una struttura usando almeno 3.000 blocchi.",
    "✨ **Il Collezionista:** Craftate un Faro (Beacon) e portalo al livello massimo.",
    "🐸 **Amico degli Animali:** Catturate 5 Axolotl di colori diversi.",
    "💀 **Cacciatore di Teste:** Ottenete 3 Cuori di Wither."
]

# --- GESTIONE MEMORIA ANTI-RIPETIZIONE ---
FILE_MEMORIA = "missioni_usate.json"

def carica_usate():
    if os.path.exists(FILE_MEMORIA):
        with open(FILE_MEMORIA, "r", encoding="utf-8") as f:
            return json.load(f)
    return {ruolo: [] for ruolo in MISSIONI_SETTIMANALI}

def salva_usate(usate):
    with open(FILE_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(usate, f, ensure_ascii=False, indent=4)

def estrai_missione(ruolo):
    usate = carica_usate()
    tutte = MISSIONI_SETTIMANALI[ruolo]
    
    if len(usate[ruolo]) >= len(tutte):
        usate[ruolo] = []
        
    disponibili = [m for m in tutte if m not in usate[ruolo]]
    scelta = random.choice(disponibili)
    
    usate[ruolo].append(scelta)
    salva_usate(usate)
    return scelta

# --- FUNZIONI DI GENERAZIONE EMBED ---

async def genera_e_invia_embed():
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print(f"❌ Errore: Canale con ID {CHANNEL_ID} non trovato.")
        return
        
    embed = discord.Embed(
        title="📜 MISSIONI SETTIMANALI PER RUOLO",
        description="Ecco le nuove sfide per i prossimi **7 giorni**! Per chi ce la fa... 50 SCUDI!!! Ma solo i migliori possono farlo\nNessuna ripetizione fino a completamento del catalogo.",
        color=discord.Color.gold()
    )
    
    for ruolo in MISSIONI_SETTIMANALI.keys():
        missione = estrai_missione(ruolo)
        embed.add_field(name=f"**Ruolo: {ruolo}**", value=missione, inline=False)
        
    embed.set_footer(text="Buona fortuna a tutti i giocatori!")
    await channel.send(embed=embed)
    print("✅ Messaggio delle missioni settimanali inviato con successo su Discord!")

async def genera_e_invia_mensili(target_channel=None):
    channel = target_channel or bot.get_channel(CHANNEL_ID)
    if not channel:
        print(f"❌ Errore: Canale non trovato.")
        return

    # Estrae UNA SOLA missione mensile casuale dalla lista
    sfida_mensile = random.choice(MISSIONI_MENSILE_LISTA)

    embed = discord.Embed(
        title="🏆 SFIDA MENSILE COMUNITARIA 🏆",
        description="Ecco la grande sfida per l'intero server per questo mese! **Lavorate insieme per completarla!** Se lo farete... **100 scudi a testa** come ricompensa",
        color=discord.Color.purple()
    )

    embed.add_field(name="La Missione del Mese:", value=sfida_mensile, inline=False)
    embed.set_footer(text="Avete un intero mese di tempo. Buona collaborazione!")

    await channel.send(embed=embed)
    print("✅ Messaggio della missione mensile inviato con successo su Discord!")

# --- TIMER AUTOMATICO GIORNALIERO (8:00 UTC = 10:00 Italiana) ---
ORARIO_INVIO = datetime.time(hour=8, minute=0, tzinfo=datetime.timezone.utc)

@tasks.loop(time=ORARIO_INVIO)
async def timer_automatico_giornaliero():
    oggi = datetime.datetime.now(datetime.timezone.utc)
    
    # 1. Se è Lunedì (0 = Lunedì), invia le missioni settimanali
    if oggi.weekday() == 0:
        print("📅 È Lunedì! Invio le missioni settimanali...")
        await genera_e_invia_embed()

    # 2. Se è il 1° giorno del mese, invia LA missione mensile
    if oggi.day == 1:
        print("📅 È il primo del mese! Invio la missione mensile...")
        await genera_e_invia_mensili()

# --- EVENTI E COMANDI DISCORD ---
@bot.event
async def on_ready():
    print(f'🤖 Bot connesso con successo come: {bot.user}')
    if not timer_automatico_giornaliero.is_running():
        timer_automatico_giornaliero.start()
        print("⏱️ Timer automatico per invio missioni avviato con successo!")

# Comando manuale per le settimanali
@bot.command(name="nuovemissioni")
async def cmd_nuove_missioni(ctx):
    await genera_e_invia_embed()

# Comando manuale per estrarre 1 missione mensile
@bot.command(name="missionimensili")
async def cmd_missioni_mensili(ctx):
    await genera_e_invia_mensili(target_channel=ctx.channel)

bot.run(TOKEN)
