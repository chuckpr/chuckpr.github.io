// Animated Braille DNA double helix
// Two sine-wave strands offset by π, connected by base-pair rungs,
// rendered into Unicode Braille characters (U+2800–U+28FF).

(function () {
  "use strict";

  var canvas = document.getElementById("dna-canvas");
  if (!canvas) return;

  // ── Braille encoding ──────────────────────────────────────────────
  // Each Braille character is a 2-wide × 4-tall dot grid.
  // Dot positions map to bit offsets in (codepoint - 0x2800):
  //   col 0: rows 0-3 → bits 0,1,2,6
  //   col 1: rows 0-3 → bits 3,4,5,7
  var DOT_BIT = [
    [1 << 0, 1 << 1, 1 << 2, 1 << 6], // column 0, rows 0–3
    [1 << 3, 1 << 4, 1 << 5, 1 << 7], // column 1, rows 0–3
  ];

  // ── Configuration ─────────────────────────────────────────────────
  var ROWS = 4; // Braille-character rows (× 4 = 16 logical pixels high)
  var FPS = 8;
  var FRAME_MS = 1000 / FPS;
  var TWO_PI = Math.PI * 2;

  // Helix parameters (in logical-pixel space)
  var LOGICAL_H = ROWS * 4; // 16 logical pixels tall
  var CENTER_Y = (LOGICAL_H - 1) / 2;
  var AMPLITUDE = (LOGICAL_H - 2) / 2; // leave 1px margin top/bottom
  var PERIOD_PX = 48; // logical pixels per full helix turn
  var K = TWO_PI / PERIOD_PX;
  var PHASE_SPEED = -0.05; // radians per frame (negative = right-handed helix)

  // Base-pair rungs drawn every N logical pixels along x
  var RUNG_SPACING = 4;

  // ── State ─────────────────────────────────────────────────────────
  var cols = 0; // Braille-character columns (recomputed on resize)
  var logicalW = 0;
  var phase = 0;
  var lastFrame = 0;
  var rafId = null;
  var isStatic = false;

  // ── Reduced-motion check ──────────────────────────────────────────
  var motionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
  isStatic = motionQuery.matches;
  motionQuery.addEventListener("change", function (e) {
    isStatic = e.matches;
    if (isStatic && rafId) {
      cancelAnimationFrame(rafId);
      rafId = null;
    } else if (!isStatic && !rafId) {
      rafId = requestAnimationFrame(tick);
    }
  });

  // ── Sizing ────────────────────────────────────────────────────────
  function measure() {
    var container = canvas.parentElement;
    if (!container) return;
    var width = container.clientWidth;

    // Estimate character width: Fira Code at 0.85rem ≈ 0.51rem per char.
    // Use a measurement element for accuracy.
    var probe = document.createElement("span");
    probe.style.cssText =
      "position:absolute;visibility:hidden;white-space:pre;font:inherit;";
    probe.textContent = "\u2800"; // Braille blank
    canvas.appendChild(probe);
    var charW = probe.getBoundingClientRect().width || 8;
    canvas.removeChild(probe);

    cols = Math.floor(width / charW);
    logicalW = cols * 2; // 2 logical pixels per Braille column
  }

  // ── Render one frame ──────────────────────────────────────────────
  function render() {
    // pixel buffer: logicalW × LOGICAL_H
    // values: 0 = off, 1 = strand 1, 2 = strand 2, 3 = rung
    var buf = new Uint8Array(logicalW * LOGICAL_H);

    function setPixel(x, y, val) {
      x = Math.round(x);
      y = Math.round(y);
      if (x >= 0 && x < logicalW && y >= 0 && y < LOGICAL_H) {
        buf[y * logicalW + x] = val;
      }
    }

    for (var x = 0; x < logicalW; x++) {
      var angle = K * x + phase;
      var sinVal = Math.sin(angle);

      var y1 = CENTER_Y + AMPLITUDE * sinVal;
      var y2 = CENTER_Y - AMPLITUDE * sinVal; // π offset = negation

      // Determine which strand is "in front" (closer to viewer).
      // cos >= 0 → strand 1 in front; cos < 0 → strand 2 in front
      var cosVal = Math.cos(angle);
      var frontY = cosVal >= 0 ? y1 : y2;
      var backY = cosVal >= 0 ? y2 : y1;
      var frontId = cosVal >= 0 ? 1 : 2;
      var backId = cosVal >= 0 ? 2 : 1;

      // Always draw front strand
      setPixel(x, frontY, frontId);

      // Draw back strand only when strands are separated enough (≥2px)
      if (Math.abs(y1 - y2) >= 2) {
        setPixel(x, backY, backId);
      }

      // Rungs: draw vertical lines between strands at intervals
      if (x % RUNG_SPACING === 0 && Math.abs(y1 - y2) >= 3) {
        var top = Math.round(Math.min(y1, y2)) + 1;
        var bot = Math.round(Math.max(y1, y2)) - 1;
        for (var ry = top; ry <= bot; ry++) {
          setPixel(x, ry, 3);
        }
      }
    }

    // Encode to Braille characters with per-character color classes
    var TYPE_CLASS = ["", "s1", "s2", "rg"]; // indexed by pixel type
    var lines = [];
    for (var row = 0; row < ROWS; row++) {
      var line = "";
      for (var col = 0; col < cols; col++) {
        var code = 0;
        var dominant = 0; // track dominant pixel type in this 2×4 block
        for (var dc = 0; dc < 2; dc++) {
          for (var dr = 0; dr < 4; dr++) {
            var px = col * 2 + dc;
            var py = row * 4 + dr;
            if (px < logicalW) {
              var val = buf[py * logicalW + px];
              if (val) {
                code |= DOT_BIT[dc][dr];
                // priority: strand (1 or 2) > rung (3) > empty (0)
                if (val <= 2 && (dominant === 0 || dominant === 3)) {
                  dominant = val; // strand beats rung or empty
                } else if (dominant === 0) {
                  dominant = val; // rung beats empty
                }
              }
            }
          }
        }
        var ch = String.fromCharCode(0x2800 + code);
        if (code === 0) {
          line += ch;
        } else {
          line += '<span class="' + TYPE_CLASS[dominant] + '">' + ch + "</span>";
        }
      }
      lines.push(line);
    }

    canvas.innerHTML = lines.join("\n");
  }

  // ── Animation loop ────────────────────────────────────────────────
  function tick(timestamp) {
    if (timestamp - lastFrame >= FRAME_MS) {
      lastFrame = timestamp;
      phase += PHASE_SPEED;
      if (phase > TWO_PI) phase -= TWO_PI;
      if (phase < -TWO_PI) phase += TWO_PI;
      render();
    }
    if (!isStatic) {
      rafId = requestAnimationFrame(tick);
    }
  }

  // ── Responsive resize ─────────────────────────────────────────────
  var resizeTimer;
  window.addEventListener("resize", function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () {
      measure();
      render();
    }, 100);
  });

  // ── Boot ──────────────────────────────────────────────────────────
  measure();
  render(); // always show one static frame immediately

  if (!isStatic) {
    rafId = requestAnimationFrame(tick);
  }
})();
