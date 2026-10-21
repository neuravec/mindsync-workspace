## Security & GDPR Opinion — Anonimowy tryb próbny (Firebase `signInAnonymously` + `linkWithCredential`) — 2026-08-10

**Zlecenie**: `analytics-reports/2026-08-10-anonymous-users-analysis.md`, rekomendacja R3 „Wariant A". Cytat z tego raportu: *„BLOKER do rozstrzygnięcia PRZED implementacją: security-guardian musi wydać opinię. Pierwszy zapis to dane o zdrowiu psychicznym (art. 9 RODO), a dziś zgoda zbierana jest w legal gate po rejestracji. (…) Bez tej opinii wariantu A nie wolno zaczynać."*

**Status agenta**: read-only audytor. Nie edytowałem żadnego kodu — wszystkie ścieżki poniżej są odczytane w całości.

**Zastrzeżenie**: to jest wewnętrzna opinia bezpieczeństwa/inżynierska do decyzji operatora, **nie porada prawna**. Ostateczna ocena zgodności z RODO (w szczególności treść i redakcja checkboxa GDPR, podstawa prawna dla poszczególnych pól) wymaga sign-offu prawnika — pamięć projektu już oznacza treść `onboarding_gdprConsent` jako „⚠ prawnik" do weryfikacji niezależnie od tego dokumentu.

---

### Werdykt

**DOPUSZCZALNE POD WARUNKAMI — ale nie w kształcie opisanym w rekomendacji R3 Wariant A wprost.** Kluczowa zmiana względem propozycji growth-analyst: legal gate (albo jego okrojona wersja) musi zostać pokazany i zaakceptowany **przed pierwszym zapisem treści refleksyjnej/emocjonalnej**, a nie „po próbnym zapisie" ani nawet w obecnym miejscu (po pełnej rejestracji). To częściowo zjada zysk z wariantu — co growth-analyst już przewidział we własnym raporcie — ale jest to jedyna konfiguracja, która nie przetwarza danych art. 9 RODO bez podstawy prawnej.

Dodatkowo: implementacja wymaga jednej zmiany schematu backendu (pole `email` jest dziś obowiązkowe w kontrakcie tworzenia użytkownika — patrz sekcja 2) oraz nowego mechanizmu retencji dla nigdy-nie-skonwertowanych kont anonimowych (sekcja 3), zanim funkcja może wejść do produkcji.

**Nie blokuję trybu anonimowego jako takiego** — techniczna architektura Firebase `signInAnonymously` + `linkWithCredential` jest solidna i (poza dwoma wymienionymi lukami) dobrze pasuje do istniejącego modelu danych MindSync (Firebase UID jako PK, brak zmiany UID przy „upgrade" konta). Blokuję wyłącznie kolejność: zgoda musi poprzedzać treść, nie odwrotnie.

---

## 1. Dane art. 9 RODO od anonimowego użytkownika PRZED legal gate

**Odpowiedź: niedopuszczalne w żadnej konfiguracji, niezależnie od tego, że konto jest „anonimowe" po stronie Firebase.**

Rozróżnienie kluczowe dla tej opinii: „anonimowy" w sensie Firebase (`signInAnonymously()`, brak e-maila/hasła) **nie jest tym samym** co „anonimowy" w sensie RODO (dane nieodwracalnie niepowiązane z osobą, recital 26). Konto z Firebase UID jako trwałym identyfikatorem, do którego przypisywana jest treść refleksji, jest **danymi pseudonimizowanymi**, czyli nadal danymi osobowymi w rozumieniu RODO. Sam fakt braku e-maila nie zmienia tej kwalifikacji.

Treść refleksji/check-inu w aplikacji do zdrowia psychicznego kwalifikuje się jako dane dotyczące zdrowia (art. 4 pkt 15, art. 9 ust. 1 RODO) — to zresztą już dziś jest domyślne założenie architektury MindSync: checkbox `onboarding_gdprConsent` w obecnym legal gate wprost mówi „I consent to MindSync processing my **wellbeing and reflection data**" (`app_en.arb:89`), czyli traktuje treść refleksji jako kategorię wymagającą zgody, a nie zwykłe dane funkcjonalne.

Przetwarzanie danych art. 9 wymaga **łącznie**: (a) ważnej podstawy z art. 6 RODO, **i** (b) wyjątku z art. 9 ust. 2. Jedynym realistycznie stosowalnym wyjątkiem dla aplikacji wellness/mental-health jest **wyraźna zgoda (art. 9 ust. 2 lit. a)** — żaden inny wyjątek (zatrudnienie, żywotne interesy, dane oczywiście upublicznione, cele naukowe) nie pasuje do zwykłego zapisu refleksji przez nowego użytkownika. Bez uprzedniej zgody nie ma podstawy — i to jest niezależne od tego, czy konto ma e-mail, czy nie.

**Kiedy pokazać legal gate/consent w flow anonimowym.** Musi poprzedzać pierwszy zapis treści wrażliwej, nie musi poprzedzać samo `signInAnonymously()` ani przeglądanie ekranów bez zapisu. Praktyczna konsekwencja dla propozycji growth-analyst: „jeden zapis (quick capture albo jedna wiadomość Reflect) bez konta" nie może nastąpić przed zgodą — czyli między splashem a tym zapisem musi się zmieścić ekran zgody. Nie musi to być pełny 8-krokowy `TherapyOnboardingScreen` (patrz warunek MUST-3 niżej) — ale musi to być co najmniej odpowiednik dzisiejszego `OnboardingLegalGateView` (`mindsync-frontend/mindsync_app/lib/screens/therapy_onboarding/views/onboarding_legal_gate_view.dart`): disclaimer medyczny + checkbox zgody na przetwarzanie danych wellbeing/refleksji + checkbox wieku 16+ + link do polityki prywatności, z zapisem `ConsentRecord` po stronie backendu.

**Podstawa prawna PRZED zgodą — czy istnieje jakakolwiek?** Dla samego założenia konta anonimowego (Firebase UID + pusty wiersz `users`, bez treści) — tak, art. 6 ust. 1 lit. b (niezbędne do wykonania umowy/podjęcia kroków przed jej zawarciem) jest wystarczającą podstawą, analogicznie do dzisiejszego uzasadnienia w kodzie: *„Firebase account creation is kept pre-consent (lawful basis Art. 6(1)(b): necessary for contract) per the security audit decision"* (`sign_up_cubit.dart:142-143`). To już działa poprawnie dla ścieżki e-mail/OAuth i przenosi się 1:1 na ścieżkę anonimową — **utworzenie samego konta (bez treści) nie wymaga zgody**. Zgody wymaga dopiero zapis treści art. 9.

**Co z danymi, jeśli użytkownik nigdy nie założy konta.** To jest scenariusz **normalny, nie brzegowy**, dla trybu anonimowego z definicji (w przeciwieństwie do dzisiejszej ścieżki e-mail/OAuth, gdzie porzucenie przed dokończeniem rejestracji zostawia niekompletne dane, ale przynajmniej jest powiązany adres e-mail, przez który operator teoretycznie mógłby zareagować na żądanie). Tu nie ma żadnego kanału kontaktu z osobą, której dane dotyczą — right to erasure w klasycznym sensie („user zgłasza żądanie usunięcia") jest fizycznie niewykonalny, bo nikt nie jest w stanie zidentyfikować siebie jako właściciela konkretnego anonimowego UID po odinstalowaniu/reinstalacji aplikacji (Firebase anonymous auth jest lokalne dla instalacji — nowa instalacja = nowy UID, stary jest osierocony bezpowrotnie). Jedyna zgodna z zasadą minimalizacji/ograniczenia przechowywania (art. 5 ust. 1 lit. e) odpowiedź to **automatyczny, czasowy auto-purge** kont anonimowych, które nigdy nie zostały podniesione do pełnego konta — patrz warunek MUST-4.

---

## 2. Architektura obecna

### 2.1 Legal gate w kliencie — stan faktyczny (NIE to, co sugeruje pamięć projektu)

Zweryfikowałem bezpośrednio w kodzie (nie tylko z pamięci) trzy pliki: `mindsync-frontend/mindsync_app/lib/screens/sign_up/personalise_view.dart`, `mindsync-frontend/mindsync_app/lib/screens/sign_up/cubit/sign_up_cubit.dart`, `mindsync-frontend/mindsync_app/lib/screens/therapy_onboarding/views/onboarding_legal_gate_view.dart`, `mindsync-frontend/mindsync_app/lib/screens/therapy_onboarding/cubit/therapy_onboarding_cubit.dart`.

**Wniosek: problem opisany w pamięci projektu jako otwarty („PersonaliseView zbiera gender PRZED Legal Gate") jest już naprawiony w kodzie**, komentarzami datowanymi na ten sam audyt PostHog (2026-08-10, zadanie B6). Faktyczny przepływ dziś:

1. `PersonaliseView` zbiera `full_name`/`pronouns`/`gender`/`age_band` w UI (`personalise_view.dart:279-336`) i przekazuje do `SignUpCubit.register()`/`registerForGoogleAndApple()`.
2. `SignUpCubit.register()` (`sign_up_cubit.dart:144-224`) tworzy konto Firebase (e-mail/hasło) → tworzy wiersz `users` (tylko e-mail + UID, `_usersManager.createUser`) → **zapisuje profil (imię/płeć/wiek) lokalnie w `SharedPreferences` jako `pendingProfile`, NIE wysyła go do backendu** (`_savePendingProfile`, linia 117-132) → wysyła e-mail weryfikacyjny.
3. Dopiero `TherapyOnboardingCubit.acceptConsent()` (wywoływane po zaznaczeniu obu checkboxów na `OnboardingLegalGateView`) odblokowuje wysyłkę zapisanego profilu do backendu — komentarz w kodzie: *„createUserProfile deferred until GDPR consent (…) createUserProfile() is NOT called here — it is deferred until the user accepts GDPR consent in TherapyOnboardingCubit.acceptConsent()"* (`sign_up_cubit.dart:138-143`).

Czyli: **profil demograficzny (gender/pronouns/age_band) dziś już nie trafia do backendu przed zgodą** — jest tylko zbierany w UI i trzymany lokalnie do czasu zgody. To poprawny wzorzec i dokładnie ten sam wzorzec ([]„zbierz UI, wyślij po zgodzie") należy zastosować do treści refleksji/check-inu w wariancie anonimowym — z jedną różnicą: treść refleksji nie nadaje się do trzymania w `SharedPreferences` bez szyfrowania przez dłuższy czas (patrz 2.3), więc lepszym wzorcem jest **pokazać ekran zgody przed samym aktem zapisu**, a nie po nim.

Legal gate sam w sobie (`OnboardingLegalGateView`) jest solidny: brak przycisku „pomiń", Continue zablokowany dopóki oba checkboksy nie są zaznaczone (`therapy_onboarding_screen.dart` + `onboarding_legal_gate_view.dart:123,288`), telemetria porzuceń (`onboardingLegalGateAbandoned`), brak wymogu przewijania (świadoma decyzja udokumentowana w komentarzu jako zgodna z EDPB 05/2020 — nie weryfikowałem tej interpretacji, to obszar prawnika, nie mój).

### 2.2 Czy anonimowe konto Firebase (bez e-maila) przejdzie przez obecne modele — NIE, dziś jest zablokowane na poziomie kontraktu API

Model bazodanowy **jest gotowy**: `MindSync/app/models/models.py:97-98` — `User.email = Column(String(255), unique=True, index=True)`, **bez `nullable=False`**, czyli kolumna jest nullable, a unikalność w Postgresie toleruje wiele wartości `NULL` jednocześnie (NULL != NULL). Żadna migracja nie jest tu wymagana.

Ale **kontrakt Pydantic blokuje to dziś**: `MindSync/app/schemas/schemas.py:40-41` — `class UserBase(BaseModel): email: EmailStr`. `EmailStr` odrzuci `None`/pusty string na poziomie walidacji requestu, zanim żądanie w ogóle dotrze do warstwy CRUD. Klient dziś zawsze wysyła realny e-mail (`ms.User(email: email, id: user.uid, ...)` w obu ścieżkach `sign_up_cubit.dart:200`, `251`) — nie ma dziś ścieżki tworzenia użytkownika bez e-maila.

**To jest blokujący gap architektoniczny dla Wariantu A, niezależny od RODO** — `backend-api` musi zmienić `email` na `Optional[EmailStr] = None` (lub równoważne) w schemacie tworzenia użytkownika **zanim** klient może w ogóle wywołać `createUser` dla konta anonimowego. Zgodnie z zasadą „Change Safety & Impact Recon" z `CLAUDE.md` — to pole jest prawdopodobnie konsumowane przez więcej niż jeden endpoint/serwis (weryfikacja subskrypcji, receipty Apple/Google, integracja Loops do e-mail marketingu, generowanie PDF, powiadomienia) — **rekomenduję pełne grepowanie `email` w `app/services/` i `app/crud/` przez `backend-api` jako osobne zadanie recon przed dotknięciem tego pola**, nie tylko zmianę jednej klasy Pydantic. Nie robiłem tego greppingu sam (poza zakresem read-only audytu bezpieczeństwa skoncentrowanego na tym pytaniu), ale sygnalizuję to jako wymagany krok, nie fakultatywny.

### 2.3 `consent_records` — gotowe na UID bez e-maila, ale z jedną krytyczną luką egzekwowania

`MindSync/app/models/models.py:260-292` (`ConsentRecord`) i `MindSync/app/crud/consent.py` są **całkowicie agnostyczne wobec obecności e-maila** — kluczem jest `user_id` (String FK do `users.id`), więc zapis zgody dla anonimowego Firebase UID zadziała bez żadnej zmiany. `MindSync/app/api/v1/endpoints/consent.py` (endpointy `POST/DELETE/GET /users/consent/profiling` i `/users/consent/art9_health`) też nie odwołuje się do e-maila — wymaga tylko ważnego tokena Firebase, co anonimowy token spełnia (sekcja 3.1).

**Krytyczna luka, którą trzeba naprawić PRZED wdrożeniem trybu anonimowego (nie po):** dziś backend **nie egzekwuje** zgody na poziomie serwera dla treści konwersacji/refleksji. Sprawdziłem `MindSync/app/api/v1/endpoints/conversations.py` — zero odwołań do `consent`/`is_consent_active`. Jedyne miejsce, gdzie backend faktycznie blokuje zapis bez aktywnej zgody, to pole `currently_in_therapy` w `users.py:346,353,906,914` (`is_consent_active(db, current_user_id, "ARTICLE9_HEALTH")`) — wąski, pojedynczy przypadek. Cała reszta „zgoda przed treścią" działa dziś **wyłącznie jako kontrola przepływu UI** (klient nie pokazuje ekranu produktu, dopóki `TherapyOnboardingCompleted` się nie wyemituje) — nie jako kontrola serwera.

To jest akceptowalne ryzyko dziś, bo jedyna droga do uzyskania ważnego tokena to pełna rejestracja e-mail/OAuth, która zawsze prowadzi przez legal gate w kliencie — obejście wymagałoby zmodyfikowanego klienta lub bezpośredniego wywołania Firebase SDK z pominięciem apki. **W trybie anonimowym ten sam obchód staje się trywialny i bezkosztowy**: `signInAnonymously()` można wywołać z dowolnego skryptu bez żadnej bariery (bez e-maila, bez hasła, bez OAuth), uzyskać ważny token Firebase, i uderzyć bezpośrednio w `/conversations` czy dowolny endpoint zapisujący treść — z zerową ścieżką audytu (żadnego e-maila, żadnej tożsamości, żadnej zgody w `consent_records`), na koncie, które i tak nigdy nie zamierzano powiązać z realną osobą. To zamienia dzisiejsze „ryzyko teoretyczne, niskiego prawdopodobieństwa" w „trywialne do wykorzystania po wdrożeniu Wariantu A" — patrz warunek MUST-2.

---

## 3. Ryzyka techniczne

### 3.1 Uwierzytelnianie — brak nowego ryzyka bypassu

`MindSync/app/api/deps.py:23-35` (`get_current_user`) woła `firebase_admin.auth.verify_id_token(token)` i zwraca `decoded_token['uid']` — **identycznie dla tokenów kont anonimowych i pełnych**. Firebase Admin SDK poprawnie weryfikuje token anonimowego konta (ma `firebase.sign_in_provider: "anonymous"` w payloadzie, ale to nie jest dziś sprawdzane ani wymagane po stronie backendu). Nie ma tu luki uwierzytelniania — token jest token, weryfikacja kryptograficzna działa tak samo. **Ale to oznacza też, że backend dziś nie rozróżnia „konto anonimowe" od „konto pełne"** — co ma znaczenie dla warunku MUST-4 (auto-purge) i dla ryzyka nadużyć opisanego niżej.

### 3.2 `linkWithCredential` i scalanie danych — mniej ryzykowne niż sugeruje nazwa

Kluczowy fakt: **`linkWithCredential()` NIE zmienia Firebase UID** — podnosi istniejące konto anonimowe do pełnego przy zachowaniu tego samego `uid`. Ponieważ `users.id` w Postgresie to właśnie ten UID (`models.py:97`), **nie ma potrzeby żadnej logiki scalania rekordów po stronie backendu** — wiersz `users`, `consent_records`, `conversations` itd. zostają dokładnie tym samym wierszem, tylko z dopisanym `email` (wcześniej `NULL`). To jest architektonicznie czyste i dużo prostsze niż typowy problem „merge kont" w innych systemach.

**Jedyna rzecz do zweryfikowania przez `flutter-mobile`/`backend-api` przy implementacji:** klient nie może po prostu ponownie wywołać `createUser` (POST) po `linkWithCredential` z tym samym UID i teraz-obecnym e-mailem — trafi w istniejący wiersz i (zależnie od implementacji CRUD) albo zwróci błąd unikalności, albo zostanie po cichu zignorowane. Poprawny wzorzec to PATCH/PUT aktualizujący `email` na istniejącym wierszu, nie POST tworzący nowy. To drobna uwaga implementacyjna, nie blokada bezpieczeństwa — ale warto ją zapisać, żeby `flutter-mobile`/`backend-api` nie odkryły tego dopiero w produkcji.

### 3.3 Sieroty kont anonimowych — realne ryzyko, brak dziś mechanizmu czyszczenia

Sprawdziłem `MindSync/app/tasks/purge_deleted.py` (jedyny istniejący „purge job") — czyści wyłącznie **soft-deleted debriefy/notatki starsze niż 24h**, uruchamiane po **jawnym** usunięciu przez użytkownika. Nie istnieje żaden zadanie czyszczące **konta, które nigdy nie zostały aktywnie usunięte, ale też nigdy nie zostały podniesione z anonimowych do pełnych**. Usuwanie konta jest dziś w pełni user-initiated: `MindSync/app/api/v1/endpoints/users.py:79-96` (`firebase_delete_user`, idempotentne wywołanie `auth.delete_user(uid)`) uruchamiane z `rq_queue.enqueue(firebase_delete_user, current_user_id)` (linia 1440) — czyli tylko gdy zalogowany użytkownik sam zażąda usunięcia konta. Anonimowy użytkownik, który porzuci aplikację, nigdy nie trafi w tę ścieżkę.

Kaskada usuwania jest natomiast solidna, gdy już się uruchomi: `User` (`models.py:95-135`) ma `cascade="all, delete-orphan", passive_deletes=True` na każdej relacji (profile, konwersacje, streaks, session recordings, symptomy, notatki między sesjami itd.), z komentarzem w kodzie potwierdzającym świadomy audyt kaskad (2026-05-11). To znaczy: **gdy auto-purge zostanie zaimplementowany, nie trzeba projektować logiki kasowania per-tabela — wystarczy skasować wiersz `User`, reszta skasuje się kaskadowo poprawnie.** To jest dobra wiadomość — brakuje tylko wyzwalacza.

**Wniosek**: brak auto-purge to nie kwestia trudności technicznej (infrastruktura kaskad już istnieje i działa), tylko brakujący, prosty background job — patrz MUST-4.

### 3.4 PostHog `$identify` / person merge

Nie jest to nowy mechanizm — dokładnie ten sam mechanizm już działa dziś dla konwersji e-mail/OAuth i jest opisany w `analytics-reports/2026-08-10-anonymous-users-analysis.md` (F3): `AuthCubit` woła `Posthog().identify(distinctId: user.uid, ...)` przy logowaniu/rejestracji (`mindsync-frontend/mindsync_app/lib/screens/auth/cubit/auth_cubit.dart:64-72`, `126-130`), co scala wcześniejszy losowy `distinct_id` PostHoga (przypisany urządzeniu od pierwszego uruchomienia) z Firebase UID. Growth-analyst zmierzył ten artefakt jako mały (4,0% kohorty) i już dziś działający poprawnie. **Wprowadzenie trybu anonimowego nie zmienia tego mechanizmu** — jedyna różnica to to, że `identify()` z Firebase UID nastąpi wcześniej w cyklu życia użytkownika (przy `signInAnonymously`, nie dopiero przy pełnej rejestracji), co jest technicznie neutralne, ale rodzi jeden nowy wymóg: **żadne zdarzenie PostHog przed uzyskaniem zgody nie może nieść treści refleksji/wiadomości w properties** — dziś to prawda strukturalnie (zdarzenia analityczne w kodzie nie przenoszą treści wiadomości, tylko metadane typu `step_name`/`duration_seconds`), ale nowe zdarzenie „quick capture"/„pierwsza refleksja", jeśli powstanie dla tego wariantu, musi być zaprojektowane od początku bez treści w payloadzie — to do zweryfikowania przy code review implementacji, nie tylko w tej opinii.

### 3.5 `upload_chunks`/nagrania od anonimów

Sprawdziłem `MindSync/app/models/models.py:1820-1839` (`UploadChunk`) i `:836-856` (`SessionRecording`). Surowe audio jest szyfrowane Fernetem (`MESSAGE_ENCRYPTION_KEY`) i efemeryczne — kasowane w ciągu minut od `/complete`, najdalej 15 minut przez safety-net finalizer, z kaskadą `ON DELETE CASCADE` do `users`. To jest solidny wzorzec, ale **nagranie sesji terapeutycznej to zdecydowanie za ciężka treść na „pierwszą wartość przed kontem"** — poza tym, że wymagałoby zgody art. 9 tak samo jak tekst, dochodzi tu transkrypcja przez AssemblyAI (procesor trzeci-strony) danych wrażliwych od osoby, która formalnie nie wyraziła jeszcze żadnej zgody na przetwarzanie przez podmioty trzecie. **Rekomendacja: „pierwsza wartość" w wariancie anonimowym musi być ograniczona do lekkiego zapisu tekstowego (jedna refleksja/check-in), nigdy do nagrania audio sesji** — to zawęża powierzchnię ryzyka i jest zgodne z przykładem, który sam growth-analyst podał w R3 („quick capture albo jedna wiadomość Reflect").

### 3.6 Nowa powierzchnia nadużyć (poza RODO, ale istotna dla werdyktu całościowego)

Dziś każde konto wymaga e-maila lub tożsamości OAuth (Google/Apple) — to daje pewne, choć słabe, tarcie przeciw masowemu tworzeniu kont. Tryb anonimowy usuwa je całkowicie: `signInAnonymously()` nie wymaga niczego, można go wywołać programowo w pętli. Skoro anonimowe konto ma dokładnie taki sam dostęp do API jak konto pełne (sekcja 3.1), a produkt korzysta z płatnych modeli OpenAI, otwiera to wektor kosztowy/nadużyciowy (masowe tworzenie kont anonimowych do wyczerpania budżetu AI lub scrapingu) niezwiązany bezpośrednio z RODO, ale wystarczająco poważny, by wymagał mitygacji przed szerokim wdrożeniem — rekomendacja dla `integration-devops`: rate limiting per-UID/per-urządzenie i rozważenie device attestation (Play Integrity / App Attest) dla ścieżki anonimowej, analogicznie do tego, jak F1 raportu growth-analyst już pokazał, że MindSync ma dziś realny problem z ruchem niebędącym ludźmi uderzającym w istniejącą (trudniejszą) ścianę logowania.

---

## 4. Warunki MUST (wymagane przed jakąkolwiek implementacją Wariantu A)

1. **MUST — kolejność ekranów.** Ekran zgody (co najmniej: disclaimer + checkbox przetwarzania danych wellbeing/refleksji + checkbox wieku 16+, wzorem dzisiejszego `OnboardingLegalGateView`) musi zostać pokazany i zaakceptowany **przed** pierwszym zapisem jakiejkolwiek treści refleksyjnej/emocjonalnej — nie po. `signInAnonymously()` i przeglądanie ekranów bez zapisu może nastąpić bez zgody (art. 6 ust. 1 lit. b wystarcza na samo założenie pustego konta). Owner: `ui-ux-designer` (spec skróconej wersji, jeśli ma być krótsza niż dzisiejsza) → `flutter-mobile` (implementacja) → `security-guardian` (re-review przed wdrożeniem).
2. **MUST — egzekwowanie zgody po stronie serwera, nie tylko UI.** Przed wdrożeniem trybu anonimowego, endpoint(y) zapisujące treść refleksji/konwersacji/check-inu muszą sprawdzać `is_consent_active(db, user_id, "GDPR")` (lub odpowiedni typ zgody) analogicznie do istniejącego wzorca dla `ARTICLE9_HEALTH`/`currently_in_therapy` w `users.py:346,353,906,914`. Bez tego, anonimowe konto = trywialny, bezkosztowy sposób zapisania danych art. 9 z zerową ścieżką audytu przez ominięcie klienta. Owner: `backend-api`.
3. **MUST — zmiana kontraktu tworzenia użytkownika.** `UserBase.email` w `MindSync/app/schemas/schemas.py:40-41` musi przejść z `EmailStr` (wymagane) na `Optional[EmailStr] = None`, poprzedzone pełnym reconem wszystkich miejsc konsumujących `email` (subskrypcje, receipty, Loops, PDF, powiadomienia) zgodnie z zasadą „Change Safety & Impact Recon" z `CLAUDE.md` — to pole prawdopodobnie ma więcej konsumentów niż tylko tworzenie użytkownika. Model bazodanowy (`models.py:98`) już jest nullable — migracja niepotrzebna, tylko zmiana Pydantic + recon. Owner: `backend-api`.
4. **MUST — auto-purge kont anonimowych, które nigdy nie skonwertowały.** Nowy background job (wzorem `MindSync/app/tasks/purge_deleted.py`) usuwający konta z Firebase `sign_in_provider == "anonymous"` (wymaga dodania flagi/oznaczenia po stronie backendu przy tworzeniu użytkownika — dziś backend nie rozróżnia anonimowych od pełnych kont), które nie zostały podniesione do pełnego konta w oknie X dni (rekomendacja: krótkie okno, rzędu kilku-kilkunastu dni, do ustalenia z operatorem/prawnikiem — nie z tego audytu). Kaskada usuwania (`ON DELETE CASCADE` na wszystkich relacjach `User`) już działa poprawnie i nie wymaga zmian — trzeba tylko dodać wyzwalacz. To jest jedyna zgodna z zasadą minimalizacji odpowiedź na fakt, że osoba, której dane dotyczą, nie ma praktycznej możliwości samodzielnego zażądania usunięcia nigdy-nieskonwertowanego konta anonimowego. Owner: `backend-api`.
5. **MUST — zakres „pierwszej wartości" ograniczony do lekkiego tekstu.** Pierwszy zapis przed pełnym kontem nie może być nagraniem audio sesji terapeutycznej (transkrypcja przez AssemblyAI, procesor trzeciej strony, dodatkowa warstwa ryzyka) — tylko tekstowa refleksja/check-in, zgodnie z przykładem już podanym przez growth-analyst. Owner: `flutter-mobile`/`data-analytics` (decyzja produktowa), egzekwowane przez to, co MUST-1/MUST-2 i tak już wymuszają.
6. **MUST — brak treści w zdarzeniach PostHog przed zgodą.** Każde nowe zdarzenie analityczne wprowadzone dla tej ścieżki (np. „quick_capture_saved") musi przenosić wyłącznie metadane (długość tekstu, czas, ekran) — nigdy treść wiadomości — niezależnie od tego, czy zgoda już jest, czy jeszcze nie. To rozszerza istniejący wzorzec w kodzie (zdarzenia dziś nie niosą treści wiadomości) na nowy przypadek. Owner: `data-analytics`/`flutter-mobile`, weryfikacja: `security-guardian` przy code review.
7. **MUST — poprawny wzorzec „upgrade", nie „create" przy `linkWithCredential`.** Po podniesieniu konta anonimowego do pełnego, backend musi zaktualizować (PATCH/PUT) istniejący wiersz `users` (ten sam UID), nie próbować tworzyć nowego przez POST. Owner: `flutter-mobile` + `backend-api` (kontrakt).
8. **REKOMENDACJA (nie blokująca RODO, ale silnie zalecana przed szerokim wdrożeniem)**: rate limiting/attestation dla ścieżki `signInAnonymously`, żeby nie otworzyć nowego, taniego wektora nadużycia budżetu OpenAI/API. Owner: `integration-devops`.

### Alternatywa, jeśli warunki MUST 1-4 nie mogą zostać spełnione w rozsądnym terminie

„Ephemeral local-only" tryb próbny: pierwszy zapis (refleksja/check-in) trzymany **wyłącznie lokalnie na urządzeniu** (np. w zaszyfrowanym storage, bez żadnego wywołania backendu, bez Firebase UID, bez PostHog `identify`), z jasnym komunikatem w UI że nic nie jest wysłane ani zapisane po stronie serwera, dopóki użytkownik nie założy konta. W tym wariancie nie ma przetwarzania danych osobowych po stronie administratora (MindSync) w ogóle przed rejestracją — dane nigdy nie opuszczają urządzenia — więc art. 9 RODO nie ma zastosowania (nie ma administratora przetwarzającego). To słabszy z punktu widzenia produktu (treść ginie, jeśli user odinstaluje przed rejestracją; brak kontynuacji na innym urządzeniu), ale nie wymaga żadnego z warunków MUST-2/3/4 i może być wdrożony szybciej, jako krok pośredni przed pełnym Wariantem A.

---

## GDPR Compliance Status (dot. tej konkretnej propozycji)

| Wymóg | Status dziś (bez zmian) | Status po spełnieniu MUST 1-7 |
|---|---|---|
| Podstawa prawna dla treści art. 9 przed zgodą | Nie dotyczy (funkcja nie istnieje) | ✅ Spełniony (zgoda przed zapisem) |
| Egzekwowanie zgody po stronie serwera | ❌ Nie istnieje nawet dla dzisiejszego flow | ✅ Wymagane jako MUST-2 |
| Prawo do bycia zapomnianym dla kont niekonwertowanych | ❌ Brak mechanizmu | ✅ Auto-purge (MUST-4) |
| Kaskada usuwania danych | ✅ Już działa poprawnie (`ON DELETE CASCADE`, audyt 2026-05-11) | ✅ bez zmian |
| Minimalizacja danych (audio vs tekst) | Nie dotyczy | ✅ Ograniczone do tekstu (MUST-5) |
| Zgodność `consent_records` z kontem bez e-maila | ✅ Już gotowe, brak zmian potrzebnych | ✅ |

---

## Ścieżka raportu

`C:\Users\mikol\Notebooks\MindSync\Heroku\security-reports\2026-08-10-anonymous-auth-gdpr-opinion.md`
