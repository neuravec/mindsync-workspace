// Shared components for MindSync login designs.

const { useState, useEffect, useRef } = React;

// ── Icon (Material Symbols Rounded wrapper) ────────────────────────
function Icon({ name, size = 24, fill = 0, weight = 400, color = "inherit", style = {} }) {
  return (
    <span
      className="material-symbols-rounded"
      style={{
        fontSize: size,
        color,
        fontVariationSettings: `"FILL" ${fill}, "wght" ${weight}, "GRAD" 0, "opsz" ${Math.min(48, Math.max(20, size))}`,
        userSelect: "none",
        lineHeight: 1,
        display: "inline-block",
        ...style
      }}>
      
      {name}
    </span>);

}

// ── Android phone shell (transparent status bar; no top app bar) ─────
function PhoneShell({ children, label, statusColor = "auto", time = "08:48" }) {
  const dark = statusColor === "dark";
  return (
    <div data-screen-label={label} style={{
      width: 412, height: 892, borderRadius: 38,
      background: "#0a0d0e",
      padding: 8, boxSizing: "border-box",
      boxShadow: "0 30px 60px rgba(14,29,31,0.30), 0 0 0 1px rgba(255,255,255,0.04) inset",
      fontFamily: 'Figtree, system-ui, sans-serif',
      flexShrink: 0,
      position: "relative"
    }}>
      <div style={{
        width: "100%", height: "100%", overflow: "hidden",
        borderRadius: 30, position: "relative",
        background: "var(--ms-page)",
        display: "flex", flexDirection: "column"
      }}>
        {children}
        {/* Status bar overlay — sits on top of whatever the screen drew */}
        <StatusBar time={time} dark={dark} />
        {/* Home gesture bar */}
        <HomeGesture dark={dark} />
      </div>
    </div>);

}

function StatusBar({ time = "08:48", dark = false }) {
  const ink = dark ? "#fff" : "#1F3D38";
  return (
    <div style={{
      position: "absolute", top: 0, left: 0, right: 0,
      height: 32, padding: "0 22px",
      display: "flex", alignItems: "center", justifyContent: "space-between",
      color: ink, fontSize: 14, fontWeight: 600, letterSpacing: -0.2,
      zIndex: 50, pointerEvents: "none"
    }}>
      <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
        <span>{time}</span>
        <Icon name="play_arrow" size={12} fill={1} color={ink} style={{ transform: "rotate(0deg)" }} />
      </div>
      <div style={{ display: "flex", gap: 6, alignItems: "center" }}>
        <Icon name="notifications_off" size={13} color={ink} />
        <Icon name="bluetooth" size={13} color={ink} />
        <Icon name="signal_cellular_alt" size={13} color={ink} />
        <Icon name="wifi" size={13} color={ink} />
        <span style={{ fontSize: 11 }}>96</span>
        <span style={{
          display: "inline-block", width: 16, height: 9, borderRadius: 2,
          border: `1px solid ${ink}`, position: "relative"
        }}>
          <span style={{
            position: "absolute", inset: 1, background: ink, borderRadius: 1
          }} />
        </span>
      </div>
    </div>);

}

function HomeGesture({ dark = false }) {
  return (
    <div style={{
      position: "absolute", left: 0, right: 0, bottom: 0,
      height: 22, display: "flex", alignItems: "center", justifyContent: "center",
      zIndex: 50, pointerEvents: "none"
    }}>
      <div style={{
        width: 130, height: 4, borderRadius: 4,
        background: dark ? "rgba(255,255,255,0.65)" : "rgba(17,50,55,0.55)"
      }} />
    </div>);

}

// ── Wave pattern (brand DNA) — single layer drifting horizontally ───
function WavePattern({ color = "var(--ms-forest-500)", opacity = 0.18, height = 160, amp = 14, animate = true }) {
  // Two copies stitched, animated leftward so the loop is seamless.
  const lines = 10;
  const w = 800;
  const path = (yOffset, freq) => {
    let d = `M 0 ${yOffset}`;
    for (let x = 0; x <= w; x += 4) {
      const y = yOffset + Math.sin(x / w * Math.PI * freq) * amp;
      d += ` L ${x} ${y.toFixed(2)}`;
    }
    return d;
  };
  return (
    <div style={{
      position: "absolute", left: 0, right: 0, bottom: 0,
      height, overflow: "hidden", pointerEvents: "none",
      maskImage: "linear-gradient(180deg, transparent 0%, #000 35%, #000 100%)",
      WebkitMaskImage: "linear-gradient(180deg, transparent 0%, #000 35%, #000 100%)"
    }}>
      <svg
        width={w * 2} height={height} viewBox={`0 0 ${w * 2} ${height}`}
        style={{
          display: "block",
          animation: animate ? "waveDrift 22s linear infinite" : "none"
        }}>
        
        <g>
          {Array.from({ length: lines }).map((_, i) => {
            const y = height * 0.42 + i * (height * 0.06);
            const op = opacity * (1 - i * 0.06);
            return (
              <g key={i}>
                <path d={path(y, 4 + i % 3 * 0.5)} fill="none" stroke={color} strokeWidth="1.1" strokeOpacity={op} />
                <path d={path(y, 4 + i % 3 * 0.5)} fill="none" stroke={color} strokeWidth="1.1" strokeOpacity={op} transform={`translate(${w} 0)`} />
              </g>);

          })}
        </g>
      </svg>
    </div>);

}

// ── Logo mark (raster PNG from brand assets) ────────────────────────
function LogoMark({ size = 88 }) {
  return (
    <img
      src="assets/logo-mark.png"
      alt="MindSync"
      width={size}
      height={size}
      style={{ display: "block", objectFit: "contain" }} />);


}

// ── Pill button (primary forest / ghost outline / white-google) ─────
function Pill({ kind = "primary", onClick, children, leading, fullWidth = true, style = {} }) {
  const [pressed, setPressed] = useState(false);

  const base = {
    width: fullWidth ? "100%" : "auto",
    minHeight: 56,
    borderRadius: 9999,
    padding: "0 22px",
    display: "inline-flex", alignItems: "center", justifyContent: "center", gap: 10,
    fontFamily: "Figtree", fontSize: 16, fontWeight: 600, letterSpacing: 0.1,
    cursor: "pointer",
    transition: "transform 180ms var(--ease-out), background 180ms var(--ease-out), border-color 180ms var(--ease-out)",
    transform: pressed ? "scale(0.985)" : "scale(1)",
    border: "1px solid transparent"
  };

  const kinds = {
    primary: {
      background: pressed ? "rgb(20, 56, 60)" : "rgb(31, 76, 80)",
      color: "#fff",
      boxShadow: pressed ? "none" : "0 6px 14px rgba(31, 61, 56, 0.18)"
    },
    ghost: {
      background: pressed ? "rgba(17,50,55,0.04)" : "transparent",
      color: "var(--ms-ink-title)",
      border: "1.5px solid var(--ms-forest-deep)"
    },
    google: {
      background: pressed ? "#f6f6f6" : "#ffffff",
      color: "var(--ms-ink-title)",
      border: "1px solid var(--ms-border-mint)",
      fontWeight: 500
    }
  };

  return (
    <button
      type="button"
      onClick={onClick}
      onMouseDown={() => setPressed(true)}
      onMouseUp={() => setPressed(false)}
      onMouseLeave={() => setPressed(false)}
      onTouchStart={() => setPressed(true)}
      onTouchEnd={() => setPressed(false)}
      style={{ ...base, ...kinds[kind], ...style }}>
      
      {leading}
      <span>{children}</span>
    </button>);

}

// ── Text input (mint hairline pill with leading/trailing icon) ──────
function TextField({
  type = "text", value, onChange, placeholder,
  trailingIcon, onTrailingClick, autoComplete, name
}) {
  const [focused, setFocused] = useState(false);
  return (
    <label style={{
      display: "flex", alignItems: "center", gap: 10,
      background: "#fff",
      border: `1.5px solid ${focused ? "var(--ms-p-900)" : "var(--ms-border-mint)"}`,
      borderRadius: 9999,
      height: 56,
      padding: "0 18px",
      transition: "border-color 200ms var(--ease-out), box-shadow 200ms var(--ease-out)",
      boxShadow: focused ? "var(--shadow-input-focus)" : "none",
      cursor: "text"
    }}>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        placeholder={placeholder}
        autoComplete={autoComplete}
        name={name}
        style={{
          flex: 1, border: "none", outline: "none", background: "transparent",
          fontFamily: "Figtree", fontSize: 15, fontWeight: 500,
          color: "var(--ms-ink-title)", padding: 0, minWidth: 0
        }} />
      
      {trailingIcon &&
      <button
        type="button"
        onClick={onTrailingClick}
        style={{
          border: "none", background: "transparent", padding: 6, margin: -6,
          cursor: onTrailingClick ? "pointer" : "default",
          display: "flex", alignItems: "center", justifyContent: "center",
          color: "var(--ms-forest-500)"
        }}>
        
          <Icon name={trailingIcon} size={20} color="var(--ms-forest-500)" />
        </button>
      }
    </label>);

}

// ── Checkbox (rounded square, mint hairline) ────────────────────────
function Checkbox({ checked, onChange, label }) {
  return (
    <label style={{
      display: "inline-flex", alignItems: "center", gap: 10,
      cursor: "pointer", userSelect: "none"
    }}>
      <span
        role="checkbox"
        aria-checked={checked}
        onClick={() => onChange(!checked)}
        style={{
          width: 20, height: 20, borderRadius: 6,
          border: `1.5px solid ${checked ? "var(--ms-forest-deep)" : "var(--ms-border-divider)"}`,
          background: checked ? "var(--ms-forest-deep)" : "#fff",
          display: "inline-flex", alignItems: "center", justifyContent: "center",
          transition: "all 180ms var(--ease-out)",
          flexShrink: 0
        }}>
        
        {checked && <Icon name="check" size={14} weight={700} color="#fff" />}
      </span>
      <span style={{ fontSize: 13.5, fontWeight: 500, color: "var(--ms-ink-title)" }}>
        {label}
      </span>
    </label>);

}

// ── Or-divider with hair lines ──────────────────────────────────────
function OrDivider({ label = "lub" }) {
  return (
    <div style={{
      display: "flex", alignItems: "center", gap: 12,
      padding: "4px 8px"
    }}>
      <span style={{ flex: 1, height: 1, background: "var(--ms-border-divider)" }} />
      <span style={{
        fontSize: 12, fontWeight: 500, letterSpacing: 0.4,
        textTransform: "uppercase", color: "var(--ms-ink-tertiary)"
      }}>{label}</span>
      <span style={{ flex: 1, height: 1, background: "var(--ms-border-divider)" }} />
    </div>);

}

// ── Google "G" mark ─────────────────────────────────────────────────
function GoogleG({ size = 20 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 48 48" aria-hidden="true">
      <path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3c-1.6 4.7-6 8-11.3 8a12 12 0 1 1 7.9-21l5.7-5.7C33.6 6.1 29 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z" />
      <path fill="#FF3D00" d="m6.3 14.7 6.6 4.8C14.7 16 19 13 24 13c3 0 5.8 1.1 7.9 3l5.7-5.7C33.6 6.1 29 4 24 4 16.3 4 9.7 8.3 6.3 14.7z" />
      <path fill="#4CAF50" d="M24 44c5 0 9.5-1.9 12.9-5l-6-5.1A11.9 11.9 0 0 1 24 36c-5.3 0-9.7-3.3-11.3-8l-6.6 5.1C9.6 39.7 16.3 44 24 44z" />
      <path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.3-2.3 4.3-4.3 5.8l6 5.1c-.4.4 6.4-4.7 6.4-14.9 0-1.3-.1-2.4-.4-3.5z" />
    </svg>);

}

// ── Footer link row ─────────────────────────────────────────────────
function FooterLinks({ children }) {
  return (
    <div style={{
      display: "flex", justifyContent: "center", alignItems: "center",
      gap: 20, padding: "0 8px",
      fontSize: 13, fontWeight: 500,
      color: "var(--ms-ink-secondary)"
    }}>{children}</div>);

}

Object.assign(window, {
  Icon, PhoneShell, StatusBar, HomeGesture,
  WavePattern, LogoMark,
  Pill, TextField, Checkbox, OrDivider, GoogleG, FooterLinks
});