// MindSync — Welcome / landing screen (the screen the user sees before logging in).
// Brand moment: aqua-breeze wash, big logo, wave-pattern footer.

function WelcomeScreen({ tagline = "Zanurz się w swoim umyśle", bgStyle = "aqua", showWave = true, onLogin, onRegister }) {
  // Brand washes
  const bg = bgStyle === "mist"
    ? "var(--ms-ocean-mist)"
    : bgStyle === "aqua"
      ? "var(--ms-aqua-breeze)"
      : "var(--ms-lagoon-blue)";

  return (
    <div style={{
      flex: 1, position: "relative", overflow: "hidden",
      background: bg,
      display: "flex", flexDirection: "column",
      padding: "44px 24px 38px",
    }}>
      {/* Subtle brand wave at the very bottom */}
      {showWave && (
        <WavePattern color="var(--ms-forest-deep)" opacity={0.10} height={220} amp={12} />
      )}

      {/* Top spacer — pushes brand block into the optical center */}
      <div style={{ flex: "1 1 0%" }} />

      {/* Brand block */}
      <div style={{
        display: "flex", flexDirection: "column", alignItems: "center", gap: 28,
        animation: "fadeUp 600ms var(--ease-out) both",
      }}>
        <LogoMark size={110} />
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 10 }}>
          <h1 style={{
            margin: 0,
            fontSize: 40, fontWeight: 700, letterSpacing: -0.6,
            color: "var(--ms-forest-deep)", lineHeight: 1.05,
            whiteSpace: "nowrap",
          }}>MindSync</h1>
          <p style={{
            margin: 0,
            fontSize: 16, fontWeight: 500, letterSpacing: 0,
            color: "var(--ms-ink-title)",
            textAlign: "center", maxWidth: 300,
            opacity: 0.85,
          }}>{tagline}</p>
        </div>
      </div>

      {/* Spacer — between brand and CTAs */}
      <div style={{ flex: "1 1 0%", minHeight: 32 }} />

      {/* CTAs */}
      <div style={{
        display: "flex", flexDirection: "column", gap: 12,
        animation: "fadeUp 700ms 120ms var(--ease-out) both",
        position: "relative", zIndex: 2,
      }}>
        <Pill kind="primary" onClick={onLogin}>Zaloguj się</Pill>
        <Pill kind="ghost" onClick={onRegister}>Zarejestruj się</Pill>
      </div>

      {/* Footer */}
      <div style={{
        marginTop: 28, paddingTop: 4,
        position: "relative", zIndex: 2,
      }}>
        <FooterLinks>
          <a href="#" style={{ color: "var(--ms-ink-secondary)" }}>Regulamin</a>
          <span style={{ width: 3, height: 3, borderRadius: "50%", background: "var(--ms-ink-tertiary)", opacity: 0.6 }} />
          <a href="#" style={{ color: "var(--ms-ink-secondary)" }}>Polityka prywatności</a>
        </FooterLinks>
      </div>
    </div>
  );
}

Object.assign(window, { WelcomeScreen });
