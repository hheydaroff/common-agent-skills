// smart-deck-kit.js — reusable pptxgenjs build kit for the smart corporate LIGHT theme.
// Usage:
//   const kit = require("./smart-deck-kit");
//   const pres = kit.newDeck();
//   const h = kit.helpers(pres);
//   const s = pres.addSlide(); s.background = { color: kit.T.bg };
//   h.title(s, "Title", "optional subtitle");
//   h.card(s, 0.5, 2, 6, 4);  h.badge(s, 0.7, 2.2, 1);  h.accent(s, 0.5, 2, 4);
//   h.footer(s, 2);
//   pres.writeFile({ fileName: "output/deck.pptx" });
// Run with the GLOBAL pptxgenjs:  NODE_PATH=/opt/homebrew/lib/node_modules node compile.js

const pptxgen = require("pptxgenjs");

// --- smart brand tokens (light theme) ---
const T = {
  bg: "FFFFFF", primary: "141414", body: "595959", muted: "969DA3",
  card: "F1F0EE", lime: "D7E600", border: "DFE2E5",
  // extra brand accents (use sparingly, normally not needed):
  mint: "ACE6B7", sky: "7DCFE3", coral: "EA9C98", amber: "F7BF31",
};
const HEAD = "Montserrat";  // brand: FOR smart Next  → Montserrat fallback
const BODY = "Inter";       // brand: FOR smart Sans  → Inter fallback
const R = 0.08;             // standard corner radius
const W = 13.33, H = 7.5;   // LAYOUT_WIDE matches the smart master exactly

function newDeck() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  return pres;
}

// `>` brand bullet for plain string arrays
const NL = (arr) => arr.map(t => ({ text: t, options: { bullet: { characterCode: "003E" }, indentLevel: 0 } }));

function helpers(pres) {
  function footer(slide, n) {
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: 7.02, w: 12.33, h: 0.24, fill: { color: T.card }, line: { type: "none" }, rectRadius: 0.08 });
    slide.addText("smart.AI", { x: 0.6, y: 6.98, w: 3, h: 0.32, fontFace: HEAD, fontSize: 9, bold: true, color: T.muted, align: "left", valign: "middle" });
    if (n) slide.addText(String(n).padStart(2, "0"), { x: 11.9, y: 6.98, w: 0.93, h: 0.32, fontFace: HEAD, fontSize: 9, bold: true, color: T.muted, align: "right", valign: "middle" });
  }
  function title(slide, text, sub) {
    slide.addText(text, { x: 0.5, y: 0.42, w: 12.33, h: 0.7, fontFace: HEAD, fontSize: 30, bold: true, color: T.primary, align: "left", valign: "middle" });
    slide.addShape(pres.shapes.RECTANGLE, { x: 0.52, y: 1.18, w: 1.1, h: 0.06, fill: { color: T.lime }, line: { type: "none" } }); // the ONE standing lime accent
    if (sub) slide.addText(sub, { x: 0.5, y: 1.28, w: 12.33, h: 0.4, fontFace: BODY, fontSize: 12, color: T.muted, align: "left", valign: "middle" });
  }
  function card(slide, x, y, w, h) {
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: T.card }, line: { type: "none" }, rectRadius: R });
  }
  function badge(slide, x, y, n) {
    slide.addShape(pres.shapes.OVAL, { x, y, w: 0.42, h: 0.42, fill: { color: T.muted }, line: { type: "none" } });
    slide.addText(String(n), { x, y, w: 0.42, h: 0.42, fontFace: HEAD, fontSize: 13, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
  }
  // thin lime left-edge bar — the ONE permitted highlight per content slide
  function accent(slide, x, y, h) {
    slide.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.07, h, fill: { color: T.lime }, line: { type: "none" } });
  }
  return { footer, title, card, badge, accent, NL };
}

module.exports = { T, HEAD, BODY, R, W, H, newDeck, helpers, NL };
