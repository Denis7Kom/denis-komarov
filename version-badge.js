const projectVersion = "2.0.1";
const badge = document.createElement("small");
badge.className = "project-version";
badge.textContent = "ver. " + projectVersion;
Object.assign(badge.style, {
  display: "block",
  marginTop: "6px",
  fontFamily: "inherit",
  fontSize: "11px",
  fontWeight: "400",
  lineHeight: "1.4",
  fontVariantNumeric: "tabular-nums",
  color: "inherit",
  opacity: ".76",
});

const normalize = (value) => value.trim().replace(/[’‘]/g, "'").replace(/\s+/g, " ");
const invitations = new Set([
  "Let's build something together!",
  "Costruiamo qualcosa insieme!",
  "Давайте создадим что-нибудь вместе!",
]);

function placeVersion() {
  const matches = [...document.body.querySelectorAll("p, span, div, h2, h3, h4, small, a")]
    .filter((element) => invitations.has(normalize(element.textContent)))
    .filter((element) => ![...element.children].some(
      (child) => invitations.has(normalize(child.textContent)),
    ));
  const invitation = matches.find((element) => element.getClientRects().length) ?? matches[0];
  if (!invitation) return;
  const style = getComputedStyle(invitation);
  const parentDisplay = getComputedStyle(invitation.parentElement).display;
  badge.style.color = style.color;
  badge.style.textAlign = style.textAlign;
  const rowLayout = parentDisplay.includes("grid") ||
    (parentDisplay.includes("flex") && getComputedStyle(invitation.parentElement).flexDirection.startsWith("row"));
  if (rowLayout) {
    const stack = document.createElement("div");
    invitation.before(stack);
    stack.append(invitation, badge);
  } else {
    invitation.after(badge);
  }
  observer.disconnect();
}

const observer = new MutationObserver(placeVersion);
observer.observe(document.body, { childList: true, subtree: true, characterData: true });
placeVersion();
