# mtscreen
[LANGUAGE - PL]
Program anazluje przesłany screen z MetaTrader (template znajduje się w folderze mt4-template) pod kątem rodzaju świec (BULL/BEAR). Wynik zapisywany jest do pliku candle.csv, gdzie zapistwane są informacje takie jak:
  - rodzaj bieżącej świecy,
  - rodzaj poprzedniej świecy,
  - trend (1 jeśli kolejne 3 świece są tego samego rodzaju, 0 jeśli 3 kolejne świece nie są tego samego rodzaju).
  
Plik candle.csv jest następnie do Jupyter i na podstawie Decision Tree próbuje przewidzieć kolejną świecę.
