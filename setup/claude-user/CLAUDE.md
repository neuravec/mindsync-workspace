# Globalne zasady (wszystkie projekty)

## Typografia generowanego tekstu

- **Zakaz długiego myślnika em-dash (U+2014)** we WSZYSTKIM generowanym tekście: ebooki, artykuły, copy stron, maile, posty, dokumenty, komunikaty UI, README. To najbardziej charakterystyczny sygnał tekstu AI.
- **Zakaz obejmuje również półpauzę (U+2013) użytą jako wtrącenie, pauza albo separator zdania.** Podmiana em-dasha na półpauzę niczego nie naprawia, tylko zamienia jeden sygnał AI na drugi.
- **Zamiast tego przebuduj zdanie.** Przecinek, dwukropek, nawias, albo kropka i dwa osobne zdania. Wtrącenie w środku zdania idzie w przecinki lub nawias, definicja po myślniku idzie w dwukropek.
- **Zakres liczbowy** zapisuj zwykłym łącznikiem, bez spacji: "7-10 m²", "strony 20-30".
- **Dozwolony jest wyłącznie zwykły łącznik (U+002D)** w wyrazach złożonych i zakresach. Nic dłuższego.
- **Sprawdzenie mechaniczne przed oddaniem tekstu:** przeszukaj wynik pod kątem obu znaków (U+2014 i U+2013). Trafienie znaczy, że tekst nie jest gotowy. Przepisz te zdania, nie podmieniaj znaku na inny. Nie stosuj find&replace jednego myślnika na drugi, bo to omija regułę zamiast ją spełniać.
- Źródło prawdy dla tej reguły i przykładów zastosowania: sekcja §8 "Dashes as the universal connector" w skillu `humanizer` (`.claude/skills/humanizer/SKILL.md`).
