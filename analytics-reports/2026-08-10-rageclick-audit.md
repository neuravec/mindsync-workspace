# Audyt rage-clickow ($rageclick) - B8

Data: 2026-08-10
Autor: ui-ux-designer (konsultant, read-only)
Zrodlo danych: PostHog (`scripts/posthog_query.py`, HogQL, 14 dni wstecz od 2026-08-10)

## Metodologia

33 zdarzenia `$rageclick` w oknie 14 dni rozbite po: `$lib`, `$screen_name` (na samym evencie), najblizszym poprzedzajacym/nastepujacym evencie `$screen` per `distinct_id`, wspolrzednych dotyku (`$touch_x`/`$touch_y`) wzgledem `$screen_width`/`$screen_height`, oraz kontekscie zdarzen w tej samej sesji (session replay jest maskowany, wiec lokalizacja + kontekst zdarzen to jedyne dostepne sygnaly - zgodnie z zalozeniem zadania).

## Ustalenia ogolne

- Wszystkie 33 zdarzenia pochodza z `$lib = 'posthog-flutter'` (aplikacja mobilna, iOS we wszystkich przypadkach). Zero rage-clickow z web (`$lib='web'`) w tym oknie. Wlasciciel problemu: **flutter-mobile**, nie strona www.
- Wlasciwosc `$screen_name` na samym evencie `$rageclick` zawsze zwraca literalny string `"Flutter"` - to luka w instrumentacji SDK (PostHog Flutter autocapture nie taguje aktywnego ekranu na rage-clicku), nie realna nazwa ekranu. Dlatego lokalizacje trzeba bylo ustalic przez korelacje z najblizszym zdarzeniem `$screen` w tej samej sesji, a nie z property na samym evencie.
- Rozklad: 5 uzytkownikow, 8 dni-sesji, w tym:
  - `Ho0vY6fZJ7ZQmZis6YYNQxV7Hs13`: 23/33 (69.7%, ~70% zgodnie z opisem zadania) - **3 oddzielne dni** (07-29, 07-30, 08-07). To nie jest jednorazowy incydent - ten sam typ frustracji wraca u tego samego uzytkownika przez ponad tydzien.
  - `kHUk7zMWXtRVxLot4u13wKF4z1d2`: 5/33, jeden dzien (07-30)
  - `5J8Wq6xh9rV4P9LItfzwi5nFGA33`: 3/33, dwa dni (08-03, 08-08)
  - `f5457AOhe7Y4TvcUSrpuvcPj8Kh2`: 1/33 (08-03)
  - `Zyr8D8qERjWWYrMdq0P0kUdCyu12`: 1/33 (08-07)

## Ekran i element: Settings (ekran ustawien), przycisk "wstecz"

Dla dominujacego uzytkownika (`Ho0vY6f...`), w sesji 08-07 (13 z 23 rage-clickow), skorelowanie kazdego `$rageclick` z najblizszym `$screen`:

- Wiekszosc rage-clickow z tej sesji poprzedzona jest zdarzeniem `$screen` = `settings`, a bezposrednio po rage-clicku pojawia sie `$screen` = `mainPage` (w dwoch przypadkach odstep to odpowiednio 3.8s przed / 1.3s po oraz 1.9s przed / 6ms po - praktycznie jednoczesnie z przejsciem ekranu).
- Wspolrzedne dotyku dla 8 z 13 rage-clickow w tej sesji skupiaja sie bardzo ciasno w lewym gornym rogu ekranu: `touch_x` 19-107, `touch_y` 49-197, przy szerokosci ekranu 414px. Przyklady: (31, 49), (34, 97), (45, 131), (68.5, 135), (23.5, 94), (19, 68), (21.5, 76.5), (97.5, 169).
- Ten sam wzorzec (lewy gorny rog + sasiedztwo ekranu "settings") powtarza sie w sesjach z 07-29 i 07-30 u tego samego uzytkownika, np. touch (27.5, 88.5) tuz po `$screen settings`, touch (365.5, 70.5) i (364.0, 372.5) rowniez w sesjach z aktywnym ekranem settings.

Ten obszar (x: ~20-68, y: ~77-137 licząc SafeArea + padding) odpowiada dokladnie pozycji przycisku "wstecz" na ekranie Ustawien:

```
lib/screens/settings/widgets/settings_header.dart:16-21
IconButton(
  onPressed: () => context.pop(),
  icon: const Icon(Icons.arrow_back, color: MsColors.deepOcean, size: 22),
  padding: const EdgeInsets.all(12),
  constraints: const BoxConstraints(minWidth: 48, minHeight: 48),
),
```

`SettingsHeader` jest renderowany wewnatrz `SettingsBody`, ktore z kolei jest owiniete w `SafeArea` + `Padding(EdgeInsets.symmetric(horizontal: 20, vertical: 30))` (`lib/screens/settings/settings_body.dart:132-140`) - stad przycisk wstecz siedzi w oknie x ~20-68, y ~(safeAreaTop+30) do +78, czyli dokladnie tam, gdzie skupiaja sie wspolrzedne rage-clickow.

## Root cause: ekran Settings nie ma zadnego wyjscia podczas ladowania

`lib/screens/settings/settings_screen.dart:60-84`:

```dart
builder: (BuildContext context, SettingsState state) {
  return switch (state) {
    SettingsLoadingState() => const Center(child: CircularProgressIndicator()),
    SettingsNoDataState() => const NoDataView(),
    SettingsLoadedState(...) => SettingsBody(...),
    SettingsErrorState(:final error) => ErrorView(error: error),
  };
},
```

`SettingsHeader` (a wiec i przycisk wstecz) istnieje wylacznie wewnatrz `SettingsBody`, czyli tylko w stanie `SettingsLoadedState`. W stanie `SettingsLoadingState` caly ekran to goly `Center(CircularProgressIndicator())` - **bez AppBar, bez przycisku wstecz, bez jakiejkolwiek mozliwosci wyjscia**. Trasa `settingsRoute` w `ms_routes.dart:353-363` to zwykly `GoRoute` bez ShellRoute z wlasnym stalym paskiem gory, wiec nic nie "podklada" przycisku wstecz pod spodem.

`SettingsCubit.init()` (`lib/screens/settings/cubit/settings_cubit.dart:237+`) wykonuje sekwencyjne odczyty z SharedPreferences, a nastepnie `Future.wait` na kilku wywolaniach sieciowych rownoczesnie (profil/preferencje uzytkownika, symptomy, sprawdzenie uprawnien powiadomien systemowych). Przy gorszym polaczeniu lub przy zimnym starcie to realnie zauwazalny czas bez feedbacku.

**Mechanizm rage-clicku**: uzytkownik otwiera Ustawienia (z menu bocznego, `drawer_menu.dart:104-113`), widzi spinner na srodku ekranu bez zadnego naglowka, i - z przyzwyczajenia do konwencji "wstecz w lewym gornym rogu" - zaczyna tapac w ten rejon ekranu, mimo ze nic tam jeszcze nie ma. Gdy `SettingsBody` w koncu sie zamontuje i prawdziwy przycisk wstecz pojawi sie dokladnie w tym miejscu, jeden z powtarzanych tapniec trafia w niego i ekran natychmiast wraca do `mainPage` - stad sekwencja `settings -> (seria tapniec w tym samym miejscu w krotkim oknie czasowym, wykryta jako $rageclick) -> mainPage` widoczna w danych.

Dla porownania: `ErrorView` (`lib/widgets/error_view.dart`) ma przycisk "Przejdz do glownej strony" (`Navigator.maybePop`), wiec stan bledu ma wyjscie. `NoDataView` (`lib/widgets/no_data_view.dart`) tak jak stan ladowania - rowniez nie ma zadnej mozliwosci wyjscia, ale w tym audycie nie mamy dowodow rage-clickow akurat w tym stanie; wymieniam to jako pokrewny, mniejszy problem tej samej klasy.

## Werdykt

**Bug UI, nie wolne dzialanie i nie przypadek jednej osoby bez znaczenia.** Element wyglada tak, jakby mial tam byc przycisk wstecz (uzytkownik trafia we wlasciwe miejsce po zaladowaniu), ale przez chwile go tam nie ma - klasyczny brak stanu posredniego / brak trwalego elementu nawigacji. Doswiadczenie powtarza sie u tego samego uzytkownika w 3 oddzielnych dniach, co wskazuje na realna, odtwarzalna frustracje, nie szum.

Severity: **High** (nie Critical - nie blokuje funkcji na stale, spinner w koncu znika i akcja sie wykonuje, ale to bezposrednie zrodlo frustracji na ekranie, ktory kazdy uzytkownik odwiedza regularnie, i narusza podstawowa zasade projektowa dla aplikacji mental health: "predictable flows" oraz "brak niespodziewanych zmian nawigacji").

## Spec naprawy dla flutter-mobile

### Ekran: Settings - stan ladowania

**Plik**: `lib/screens/settings/settings_screen.dart`

**Problem**: w galezi `SettingsLoadingState()` (linia 62) renderowany jest goly `Center(CircularProgressIndicator())` bez zadnego elementu nawigacyjnego.

**Fix**: dodac trwaly naglowek z przyciskiem wstecz widoczny we WSZYSTKICH stanach ekranu (loading, no-data, error, loaded), nie tylko w `SettingsBody`. Rekomendowane podejscie:

1. Wyciagnac `SettingsHeader` (lub jego odpowiednik z przyciskiem wstecz) poza `switch` na poziomie `SettingsScreen.build()`, tak aby byl renderowany raz, na stale, niezaleznie od stanu:

```dart
return BlocProvider<SettingsCubit>.value(
  value: _cubit,
  child: MsAppScaffold( // lub Scaffold + SafeArea
    body: Column(
      children: [
        const SettingsHeader(), // zawsze widoczny, natychmiast klikalny
        Expanded(
          child: BlocConsumer<SettingsCubit, SettingsState>(
            builder: (context, state) => switch (state) {
              SettingsLoadingState() => const Center(child: CircularProgressIndicator()),
              SettingsNoDataState() => const NoDataView(),
              SettingsLoadedState(...) => SettingsBody(...), // bez wlasnego naglowka - juz jest wyzej
              SettingsErrorState(:final error) => ErrorView(error: error),
            },
          ),
        ),
      ],
    ),
  ),
);
```

2. Usunac `const SettingsHeader()` z wnetrza `SettingsBody` (`lib/screens/settings/settings_body.dart:140`), zeby nie renderowac go podwojnie po zaladowaniu.

3. Jesli wyciagniecie na gore wymaga wiekszego refaktoru (np. `SettingsBody` zarzadza tez scrollem i sekcjami), minimalny wariant: dodac do galezi `SettingsLoadingState()` sam przycisk wstecz w tej samej pozycji co docelowy (`IconButton(onPressed: () => context.pop(), icon: Icons.arrow_back, ...)`, identyczne `padding`/`constraints` jak w `SettingsHeader`), zeby tap w tym miejscu dzialal natychmiast, zanim reszta tresci sie zaladuje.

4. Ten sam problem (brak wyjscia) dotyczy `NoDataView` w `SettingsNoDataState()` - warto naprawic przy okazji tym samym mechanizmem (trwaly naglowek na gorze), a nie osobnym fixem w `NoDataView` (ktory jest uzywany w wielu miejscach i nie powinien sam zakladac istnienia `context.pop()`).

**Semantics/a11y**: przycisk wstecz juz ma 48x48 minimalny target (`constraints: BoxConstraints(minWidth: 48, minHeight: 48)`) - to jest OK, nie zmieniac. Upewnic sie, ze `IconButton` ma czytelny `tooltip`/semantic label dla czytnikow ekranu (obecnie polega tylko na domyslnym tooltipie Material - warto sprawdzic czy `S.of(context)` ma klucz na "wstecz"/"back" i dodac `tooltip:` jawnie).

**DONE_WHEN**: przycisk wstecz na ekranie Ustawien jest widoczny i klikalny natychmiast po wejsciu na ekran, niezaleznie od tego czy dane sie jeszcze laduja; `flutter test` dla `SettingsScreen` pokrywa wszystkie 4 stany (loading/no-data/loaded/error) i weryfikuje obecnosc przycisku wstecz w kazdym z nich.

## Obserwacje poboczne (nie ten sam bug, do wiadomosci)

- **Serie szybkich `tab_switched`** tuz przed niektorymi rage-clickami (np. sesja `5J8Wq...` z 08-08: cztery `tab_switched` w 3 sekundy, potem rage-click 2.4s pozniej) sugeruja niecierpliwe tapanie w dolny pasek nawigacji, prawdopodobnie dlatego ze `PageView.animateToPage` (300ms, `main_page_body.dart:244-248`) nie nadaza za tempem tapniec. Slabszy sygnal niz Settings (mniej spojny w danych), warto obserwowac, ale nie rekomenduje osobnej naprawy w tej chwili.
- **Okresowe `api_error` 404 na `/api/v1/debriefs/latest`** (co ~60s, prawdopodobnie polling w tle) wystapily w tle sesji z rage-clickami u `Zyr8D8...` i posrednio u innych, ale to znany, juz sklasyfikowany szum (404 = "brak danych jeszcze", nie realny blad) objety osobnym tematem (S1 z tej samej rundy audytu). Nie ma bezposredniego zwiazku czasowo-przestrzennego z lokalizacja dotyku rage-clickow, wiec traktuje to jako niepowiazane tlo, nie jako przyczyne.
