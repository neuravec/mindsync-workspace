// MindSync — Login form screen (M3 redesign per product spec).
//
// Minimal top app bar, no logo, no illustrations, no wave pattern.
// Surface fill #F6FFFD. Coral Pink #FF9F8A is reserved for active focus only.

const M3 = {
  surface:      "#F6FFFD", // Ocean Mist (page)
  fieldFill:    "#F0F8F5", // Surface Container Low (input fill)
  primary:      "#113237", // Deep Ocean
  onPrimary:    "#F6FFFD",
  tertiary:     "#FF9F8A", // Coral Pink — focus accent ONLY
  outlineVar:   "#C5D5D2",
  outlineMuted: "#6B8783",
  onSurface:    "#0E1D1F",
};

// ── M3 Outlined Text Field with floating label ────────────────────────
function M3Field({
  type = "text", value, onChange, label,
  trailingIcon, onTrailingClick, trailingAriaLabel,
  autoComplete, name, inputMode,
}) {
  const [focused, setFocused] = React.useState(false);
  const hasValue = (value ?? "").length > 0;
  const floating = focused || hasValue;
  const borderColor = focused ? M3.tertiary : M3.outlineVar;
  const labelColor = focused ? M3.tertiary : "rgba(14,29,31,0.65)";

  return (
    <div style={{ position: "relative", width: "100%" }}>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        autoComplete={autoComplete}
        name={name}
        inputMode={inputMode}
        aria-label={label}
        style={{
          width: "100%",
          height: 56,
          boxSizing: "border-box",
          padding: "20px 52px 6px 16px",
          fontFamily: "Figtree",
          fontSize: 15,
          fontWeight: 500,
          color: M3.onSurface,
          background: M3.fieldFill,
          border: `${focused ? 2 : 1}px solid ${borderColor}`,
          borderRadius: 12,
          outline: "none",
          // Compensate the 1↔2px border swap so input position is stable
          margin: focused ? 0 : 1,
          transition: "border-color 200ms var(--ease-out), border-width 0ms",
          appearance: "none",
          WebkitAppearance: "none",
        }}
      />
      <label
        style={{
          position: "absolute",
          left: floating ? 12 : 16,
          top: floating ? -8 : "50%",
          transform: floating ? "none" : "translateY(-50%)",
          padding: floating ? "0 4px" : 0,
          background: floating ? M3.surface : "transparent",
          fontFamily: "Figtree",
          fontSize: floating ? 12 : 15,
          fontWeight: 500,
          color: labelColor,
          letterSpacing: 0.1,
          pointerEvents: "none",
          transition: "all 200ms var(--ease-out)",
        }}
      >
        {label}
      </label>
      {trailingIcon && (
        <button
          type="button"
          onClick={onTrailingClick}
          aria-label={trailingAriaLabel}
          style={{
            position: "absolute",
            right: 4, top: "50%",
            transform: "translateY(-50%)",
            width: 48, height: 48,
            border: "none",
            background: "transparent",
            display: "flex", alignItems: "center", justifyContent: "center",
            cursor: onTrailingClick ? "pointer" : "default",
            borderRadius: 24,
          }}
        >
          <Icon name={trailingIcon} size={20} color={focused ? M3.primary : M3.outlineMuted} />
        </button>
      )}
    </div>
  );
}

// ── M3 Checkbox (18dp inside 48dp touch target) ──────────────────────
function M3Checkbox({ checked, onChange, label, id = "remember" }) {
  return (
    <label
      htmlFor={id}
      style={{
        display: "inline-flex", alignItems: "center", gap: 4,
        cursor: "pointer", userSelect: "none",
        marginLeft: -15, // align 48dp tap padding to grid edge
      }}
    >
      <span style={{
        width: 48, height: 48, borderRadius: 24,
        display: "flex", alignItems: "center", justifyContent: "center",
        flexShrink: 0,
      }}>
        <input
          id={id}
          type="checkbox"
          checked={checked}
          onChange={(e) => onChange(e.target.checked)}
          style={{ position: "absolute", opacity: 0, pointerEvents: "none" }}
        />
        <span
          aria-hidden="true"
          style={{
            width: 18, height: 18, borderRadius: 4,
            border: `2px solid ${checked ? M3.primary : M3.outlineMuted}`,
            background: checked ? M3.primary : "transparent",
            display: "inline-flex", alignItems: "center", justifyContent: "center",
            transition: "all 180ms var(--ease-out)",
          }}
        >
          {checked && <Icon name="check" size={14} weight={700} color="#fff" />}
        </span>
      </span>
      <span style={{
        fontSize: 14, fontWeight: 500,
        color: M3.onSurface,
      }}>{label}</span>
    </label>
  );
}

// ── M3 Filled Primary CTA ────────────────────────────────────────────
function M3PrimaryCTA({ children, onClick, disabled }) {
  const [pressed, setPressed] = React.useState(false);
  return (
    <button
      type="submit"
      disabled={disabled}
      onClick={onClick}
      onMouseDown={() => setPressed(true)}
      onMouseUp={() => setPressed(false)}
      onMouseLeave={() => setPressed(false)}
      onTouchStart={() => setPressed(true)}
      onTouchEnd={() => setPressed(false)}
      style={{
        width: "100%", height: 56, borderRadius: 28,
        border: "none",
        background: disabled ? "rgba(14,29,31,0.12)" : M3.primary,
        color: disabled ? "rgba(14,29,31,0.38)" : M3.onPrimary,
        fontFamily: "Figtree",
        fontSize: 15, fontWeight: 600, letterSpacing: 0.1,
        cursor: disabled ? "default" : "pointer",
        position: "relative",
        overflow: "hidden",
        transition: "background 100ms var(--ease-out)",
      }}
    >
      {/* State layer */}
      <span
        aria-hidden="true"
        style={{
          position: "absolute", inset: 0,
          background: M3.onPrimary,
          opacity: pressed && !disabled ? 0.12 : 0,
          transition: "opacity 100ms var(--ease-out)",
          pointerEvents: "none",
        }}
      />
      <span style={{ position: "relative" }}>{children}</span>
    </button>
  );
}

// ── M3 Outlined Button (Google) ──────────────────────────────────────
function M3OutlinedButton({ children, onClick, leading, ariaLabel }) {
  const [pressed, setPressed] = React.useState(false);
  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={ariaLabel}
      onMouseDown={() => setPressed(true)}
      onMouseUp={() => setPressed(false)}
      onMouseLeave={() => setPressed(false)}
      onTouchStart={() => setPressed(true)}
      onTouchEnd={() => setPressed(false)}
      style={{
        width: "100%", height: 56, borderRadius: 28,
        background: M3.surface,
        border: `1px solid ${M3.outlineVar}`,
        color: M3.onSurface,
        fontFamily: "Figtree",
        fontSize: 15, fontWeight: 500, letterSpacing: 0.1,
        display: "inline-flex", alignItems: "center", justifyContent: "center", gap: 12,
        cursor: "pointer",
        position: "relative", overflow: "hidden",
        transition: "background 100ms var(--ease-out)",
      }}
    >
      <span
        aria-hidden="true"
        style={{
          position: "absolute", inset: 0,
          background: M3.primary,
          opacity: pressed ? 0.08 : 0,
          transition: "opacity 100ms var(--ease-out)",
          pointerEvents: "none",
        }}
      />
      {leading}
      <span style={{ position: "relative" }}>{children}</span>
    </button>
  );
}

// ── M3 Divider with centered label ───────────────────────────────────
function M3Divider({ label = "LUB" }) {
  return (
    <div style={{
      display: "flex", alignItems: "center", gap: 16,
      padding: "0 0",
    }}>
      <span style={{ flex: 1, height: 1, background: M3.outlineVar }} />
      <span style={{
        fontSize: 12, fontWeight: 500, letterSpacing: 0.6,
        color: "rgba(14,29,31,0.6)",
      }}>{label}</span>
      <span style={{ flex: 1, height: 1, background: M3.outlineVar }} />
    </div>
  );
}

// ── The screen ──────────────────────────────────────────────────────
function LoginScreen({
  greetingCopy = "Dobrze, że wracasz.",
  onLogin, onRegister, onForgot, onGoogle, onBack,
}) {
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [showPw, setShowPw] = React.useState(false);
  const [remember, setRemember] = React.useState(false);

  const canSubmit = email.trim().length > 3 && password.length >= 4;

  return (
    <div style={{
      flex: 1, position: "relative", overflow: "hidden",
      background: M3.surface,
      display: "flex", flexDirection: "column",
    }}>
      <div style={{
        flex: 1, overflow: "auto",
        display: "flex", flexDirection: "column",
        paddingTop: 32, /* status-bar overlay clearance */
      }}>
        {/* Top app bar — 64dp, transparent, back-arrow only */}
        <header style={{
          height: 64, padding: "0 8px",
          display: "flex", alignItems: "center",
          flexShrink: 0,
        }}>
          <button
            type="button"
            onClick={onBack}
            aria-label="Powrót"
            style={{
              width: 48, height: 48, borderRadius: 24,
              background: "transparent", border: "none",
              display: "flex", alignItems: "center", justifyContent: "center",
              cursor: "pointer",
            }}
          >
            <Icon name="arrow_back" size={24} color={M3.onSurface} />
          </button>
        </header>

        {/* Title block */}
        <div style={{
          padding: "24px 24px 0",
          display: "flex", flexDirection: "column", gap: 4,
        }}>
          <h1 style={{
            margin: 0,
            fontFamily: "Figtree",
            fontSize: 28, fontWeight: 600, lineHeight: 1.15,
            letterSpacing: -0.2,
            color: M3.onSurface,
          }}>Zaloguj się</h1>
          <p style={{
            margin: 0,
            fontFamily: "Figtree",
            fontSize: 14, fontWeight: 400, lineHeight: 1.4,
            color: "rgba(14,29,31,0.7)",
          }}>{greetingCopy}</p>
        </div>

        {/* Form */}
        <form
          onSubmit={(e) => { e.preventDefault(); if (canSubmit) onLogin?.({ email, password, remember }); }}
          style={{
            padding: "32px 24px 0",
            display: "flex", flexDirection: "column",
          }}
        >
          {/* Field stack */}
          <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            <M3Field
              type="email"
              value={email}
              onChange={setEmail}
              label="Adres e-mail"
              autoComplete="email"
              name="email"
              inputMode="email"
              trailingIcon="mail"
              trailingAriaLabel="E-mail"
            />
            <M3Field
              type={showPw ? "text" : "password"}
              value={password}
              onChange={setPassword}
              label="Hasło"
              autoComplete="current-password"
              name="password"
              trailingIcon={showPw ? "visibility_off" : "visibility"}
              onTrailingClick={() => setShowPw(s => !s)}
              trailingAriaLabel={showPw ? "Ukryj hasło" : "Pokaż hasło"}
            />
          </div>

          {/* Remember-me — its own row */}
          <div style={{ marginTop: 12 }}>
            <M3Checkbox checked={remember} onChange={setRemember} label="Zapamiętaj mnie" />
          </div>

          {/* Forgot-password — its own row, right-aligned */}
          <div style={{
            marginTop: 8,
            display: "flex", justifyContent: "flex-end",
            marginRight: -8,
          }}>
            <button
              type="button"
              onClick={onForgot}
              style={{
                minHeight: 48,
                padding: "0 12px",
                background: "transparent",
                border: "none",
                fontFamily: "Figtree",
                fontSize: 14, fontWeight: 600, letterSpacing: 0.1,
                color: M3.primary,
                cursor: "pointer",
                borderRadius: 24,
              }}
            >Nie pamiętasz hasła?</button>
          </div>

          {/* Primary CTA */}
          <div style={{ marginTop: 32 }}>
            <M3PrimaryCTA disabled={!canSubmit}>Zaloguj się</M3PrimaryCTA>
          </div>

          {/* Divider */}
          <div style={{ marginTop: 24 }}>
            <M3Divider label="LUB" />
          </div>

          {/* Google */}
          <div style={{ marginTop: 24 }}>
            <M3OutlinedButton
              onClick={onGoogle}
              leading={<GoogleG size={20} />}
              ariaLabel="Zaloguj się przez Google"
            >Kontynuuj z Google</M3OutlinedButton>
          </div>
        </form>

        {/* Pushes footer to the bottom */}
        <div style={{ flex: "1 1 0%", minHeight: 24 }} />

        {/* Footer */}
        <div style={{
          padding: "16px 24px 46px",
          display: "flex", justifyContent: "center", alignItems: "center", gap: 4,
          fontFamily: "Figtree",
          fontSize: 14, fontWeight: 400,
          color: M3.onSurface,
        }}>
          <span style={{ opacity: 0.7 }}>Nie masz konta?</span>
          <button
            type="button"
            onClick={onRegister}
            style={{
              minHeight: 48,
              padding: "0 8px",
              background: "transparent",
              border: "none",
              fontFamily: "Figtree",
              fontSize: 14, fontWeight: 600,
              color: M3.primary,
              cursor: "pointer",
              borderRadius: 24,
            }}
          >Zarejestruj się.</button>
        </div>
      </div>
    </div>
  );
}

Object.assign(window, {
  LoginScreen,
  M3Field, M3Checkbox, M3PrimaryCTA, M3OutlinedButton, M3Divider,
});
