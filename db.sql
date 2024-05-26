CREATE TABLE IF NOT EXISTS TCarteFedelta (
    CartaFedeltaID INTEGER PRIMARY KEY AUTOINCREMENT,
    Titolare TEXT NOT NULL,
    SaldoPunti INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS TMovimenti (
    MovimentoID INTEGER PRIMARY KEY AUTOINCREMENT,
    CartaFedeltaID INTEGER NOT NULL,
    DataMovimento DATA NOT NULL,
    TipoMovimento INTEGER NOT NULL,
    PremioID INTEGER,
    Punti INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS TPremi (
    PremioID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nome TEXT NOT NULL,
    PuntiMinimi INTEGER NOT NULL DEFAULT 0
)