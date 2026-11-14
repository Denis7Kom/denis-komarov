const projectVersion = "2.0.1";
const badge = document.createElement("span");
badge.className = "project-version";
badge.textContent = "ver. " + projectVersion;
Object.assign(badge.style, {
  position: "fixed",
  right: "calc(12px + env(safe-area-inset-right, 0px))",
  bottom: "calc(12px + env(safe-area-inset-bottom, 0px))",
  zIndex: "100",
  padding: "5px 10px",
  border: "1px solid color-mix(in srgb, currentColor 20%, transparent)",
  borderRadius: "999px",
  background: "light-dark(rgba(255,255,255,.93), rgba(20,24,35,.94))",
  color: "light-dark(#293552, #e6ebfa)",
  fontFamily: "inherit",
  fontSize: "11px",
  fontWeight: "600",
  lineHeight: "1.4",
  fontVariantNumeric: "tabular-nums",
  whiteSpace: "nowrap",
  pointerEvents: "none",
  colorScheme: getComputedStyle(document.documentElement).colorScheme === "normal" ? "light dark" : "inherit",
  boxShadow: "0 2px 12px #0002",
});
document.body.append(badge);
