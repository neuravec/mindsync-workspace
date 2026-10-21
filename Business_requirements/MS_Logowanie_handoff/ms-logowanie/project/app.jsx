// MindSync — Logowanie — design canvas root.
// Lays out Welcome + Login phone frames side-by-side, plus a focused interactive
// flow artboard. Tweaks panel toggles copy / background / wave.

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "bgStyle": "aqua",
  "showWave": true,
  "tagline": "Zanurz się w swoim umyśle",
  "greeting": "Dobrze, że wracasz."
}/*EDITMODE-END*/;

const TAGLINES = [
  "Zanurz się w swoim umyśle",
  "Codziennie po sesji, codziennie po pracy.",
  "Twoja terapia w kieszeni — łagodnie."
];

const GREETINGS = [
  "Dobrze, że wracasz.",
  "Witaj ponownie.",
  "Cieszę się, że jesteś tu znów."
];

function App() {
  const [tweaks, setTweak] = useTweaks(TWEAK_DEFAULTS);
  // Interactive (focusable) flow state
  const [step, setStep] = React.useState("welcome"); // welcome | login

  return (
    <>
      <DesignCanvas>
        <DCSection id="entry" title="Wejście do aplikacji" subtitle="Powitanie · Logowanie · Klikalny przepływ">

          <DCArtboard id="ab-welcome" label="01 · Powitanie" width={428} height={908}>
            <PhoneShell label="01 Welcome" time="08:48">
              <WelcomeScreen
                tagline={tweaks.tagline}
                bgStyle={tweaks.bgStyle}
                showWave={tweaks.showWave}
              />
            </PhoneShell>
          </DCArtboard>

          <DCArtboard id="ab-login" label="02 · Logowanie" width={428} height={908}>
            <PhoneShell label="02 Login" time="08:49">
              <LoginScreen greetingCopy={tweaks.greeting} />
            </PhoneShell>
          </DCArtboard>

          <DCArtboard id="ab-flow" label="03 · Klikalny przepływ" width={428} height={908}>
            <PhoneShell label="03 Flow" time="08:48">
              {step === "welcome" ? (
                <WelcomeScreen
                  tagline={tweaks.tagline}
                  bgStyle={tweaks.bgStyle}
                  showWave={tweaks.showWave}
                  onLogin={() => setStep("login")}
                  onRegister={() => setStep("login")}
                />
              ) : (
                <LoginScreen
                  greetingCopy={tweaks.greeting}
                  onBack={() => setStep("welcome")}
                  onLogin={() => alert("Zalogowano (mock)")}
                  onRegister={() => setStep("welcome")}
                  onForgot={() => alert("Reset hasła — link wysłany (mock)")}
                  onGoogle={() => alert("Kontynuuj z Google (mock)")}
                />
              )}
            </PhoneShell>
          </DCArtboard>

        </DCSection>
      </DesignCanvas>

      <TweaksPanel title="Tweaks">
        <TweakSection label="Powitanie (01)">
          <TweakRadio
            label="Wariant tła"
            value={tweaks.bgStyle}
            onChange={(v) => setTweak("bgStyle", v)}
            options={[
              { value: "mist", label: "Mglisty" },
              { value: "aqua", label: "Brand" },
              { value: "lagoon", label: "Mocny" },
            ]}
          />
          <TweakToggle
            label="Fala marki"
            value={tweaks.showWave}
            onChange={(v) => setTweak("showWave", v)}
          />
        </TweakSection>

        <TweakSection label="Copy">
          <TweakSelect
            label="Hasło na powitalnym"
            value={tweaks.tagline}
            onChange={(v) => setTweak("tagline", v)}
            options={TAGLINES.map(t => ({ value: t, label: t }))}
          />
          <TweakSelect
            label="Powitanie w logowaniu"
            value={tweaks.greeting}
            onChange={(v) => setTweak("greeting", v)}
            options={GREETINGS.map(t => ({ value: t, label: t }))}
          />
        </TweakSection>
      </TweaksPanel>
    </>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
