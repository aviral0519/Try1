import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Will you be my Valentine?", page_icon="💖", layout="centered")

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>Valentine</title>

<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>

<style>
  :root {
    --bg1: #ffd6e7;
    --bg2: #ffeef6;
    --bg3: #fff0f5;
    --card: rgba(255, 255, 255, 0.95);
    --yes: #ff3b7a;
    --yesHover: #ff1f68;
  }

  * { box-sizing: border-box; }

  body {
    margin: 0;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(120deg, #ff9a9e, #fad0c4, #fbc2eb, #ffd1ff);
    background-size: 300% 300%;
    animation: bgShift 12s ease infinite;
    font-family: 'Segoe UI', system-ui, sans-serif;
    overflow: hidden;
    padding: 16px;
    position: relative;
  }

  @keyframes bgShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
  }

  /* Glowing blobs */
  body::before,
  body::after {
    content: "";
    position: fixed;
    width: 420px;
    height: 420px;
    border-radius: 50%;
    filter: blur(120px);
    opacity: 0.45;
    z-index: 0;
    pointer-events: none;
  }

  body::before {
    background: #ff5f9e;
    top: -100px;
    left: -100px;
    animation: blob1 18s ease-in-out infinite;
  }

  body::after {
    background: #ffc3e6;
    bottom: -120px;
    right: -120px;
    animation: blob2 20s ease-in-out infinite;
  }

  @keyframes blob1 {
    0%, 100% { transform: translate(0, 0); }
    50% { transform: translate(120px, 80px); }
  }

  @keyframes blob2 {
    0%, 100% { transform: translate(0, 0); }
    50% { transform: translate(-120px, -100px); }
  }

  /* Floating hearts & sparkles */
  .particle {
    position: fixed;
    font-size: 18px;
    opacity: 0.7;
    animation: floatUp linear infinite;
    z-index: 0;
    pointer-events: none;
  }

  @keyframes floatUp {
    from {
      transform: translateY(110vh) scale(0.8);
      opacity: 0;
    }
    10% { opacity: 0.8; }
    to {
      transform: translateY(-10vh) scale(1.2);
      opacity: 0;
    }
  }

  #confettiCanvas {
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    z-index: 5;
  }

  .card {
    width: min(480px, 92vw);
    max-width: 100%;
    padding: 32px 24px;
    background: var(--card);
    backdrop-filter: blur(10px);
    border-radius: 22px;
    text-align: center;
    box-shadow: 0 18px 60px rgba(0,0,0,.15);
    position: relative;
    z-index: 10;
  }

  h1 {
    font-size: clamp(26px, 4vw, 44px);
    margin: 12px 0 18px;
    color: #333;
  }

  .button-zone {
    position: relative;
    width: 100%;
    max-width: 320px;
    height: 120px;
    margin: 20px auto;
    touch-action: none;
  }

  button {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    padding: 14px 28px;
    font-size: 16px;
    font-weight: 700;
    border-radius: 999px;
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0,0,0,.15);
    user-select: none;
    -webkit-tap-highlight-color: transparent;
    transition: transform .12s ease, background .12s ease;
  }

  #yesBtn {
    left: 10%;
    background: var(--yes);
    color: #fff;
  }
  #yesBtn:hover { background: var(--yesHover); }

  #noBtn {
    right: 10%;
    left: auto;
    background: #e5e7eb;
    color: #111827;
  }

  .hint {
    margin-top: 10px;
    font-size: 13px;
    opacity: 0;
    transform: translateY(5px);
    transition: opacity 0.3s ease, transform 0.3s ease;
    color: #666;
  }

  .hint.visible {
    opacity: 1;
    transform: translateY(0);
  }

  .result {
    display: none;
    margin-top: 18px;
    animation: pop .35s ease;
  }

  .result h2 {
    font-size: clamp(30px, 4.5vw, 46px);
    margin: 10px 0;
  }

  .fireworks {
    width: min(380px, 90vw);
    margin: 0 auto;
    display: block;
  }

  @keyframes pop {
    from { transform: scale(.96); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
  }
</style>
</head>

<body>
<canvas id="confettiCanvas"></canvas>

<main class="card">
  <h1>Wagisha will you be my valentine? 💖</h1>

  <section class="button-zone" id="zone">
    <button id="yesBtn">Yes</button>
    <button id="noBtn">No</button>
  </section>

  <div class="hint" id="hint">"No" seems a bit shy 😈</div>

  <section class="result" id="result">
    <h2>YAY! 🎉</h2>
    <img
      class="fireworks"
      src="https://media.giphy.com/media/26ufdipQqU2lhNA4g/giphy.gif"
      alt="Fireworks"
    />
  </section>
</main>

<script>
  // Create floating hearts & sparkles
  const symbols = ["💖","💗","💘","✨","💞","💕"];
  function createParticle() {
    const p = document.createElement("div");
    p.className = "particle";
    p.innerText = symbols[Math.floor(Math.random() * symbols.length)];
    p.style.left = Math.random() * 100 + "vw";
    p.style.animationDuration = (6 + Math.random() * 6) + "s";
    p.style.fontSize = (14 + Math.random() * 16) + "px";
    document.body.appendChild(p);

    setTimeout(() => {
      p.remove();
    }, 12000);
  }

  setInterval(createParticle, 600);

  const zone = document.getElementById("zone");
  const yesBtn = document.getElementById("yesBtn");
  const noBtn = document.getElementById("noBtn");
  const result = document.getElementById("result");
  const hint = document.getElementById("hint");

  const confettiCanvas = document.getElementById("confettiCanvas");

  function resizeConfettiCanvas() {
    const dpr = Math.max(1, window.devicePixelRatio || 1);
    confettiCanvas.width = Math.floor(window.innerWidth * dpr);
    confettiCanvas.height = Math.floor(window.innerHeight * dpr);
    confettiCanvas.style.width = "100vw";
    confettiCanvas.style.height = "100vh";
  }

  resizeConfettiCanvas();
  window.addEventListener("resize", resizeConfettiCanvas);

  const confettiInstance = confetti.create(confettiCanvas, {
    resize: false,
    useWorker: true
  });

  function fullScreenConfetti() {
    const end = Date.now() + 1600;
    (function frame() {
      confettiInstance({
        particleCount: 12,
        spread: 90,
        startVelocity: 45,
        ticks: 180,
        origin: { x: Math.random(), y: Math.random() * 0.3 }
      });
      if (Date.now() < end) requestAnimationFrame(frame);
    })();

    setTimeout(() => {
      confettiInstance({
        particleCount: 300,
        spread: 140,
        startVelocity: 60,
        ticks: 220,
        origin: { x: 0.5, y: 0.55 }
      });
    }, 300);
  }

  let yesScale = 1;
  function growYes() {
    yesScale = Math.min(2.2, yesScale + 0.1);
    yesBtn.style.transform = `translateY(-50%) scale(${yesScale})`;
  }

  function clamp(n, min, max) {
    return Math.max(min, Math.min(max, n));
  }

  function moveNo(px, py) {
    const z = zone.getBoundingClientRect();
    const b = noBtn.getBoundingClientRect();

    let dx = (b.left + b.width / 2) - px;
    let dy = (b.top + b.height / 2) - py;
    let mag = Math.hypot(dx, dy) || 1;
    dx /= mag;
    dy /= mag;

    let newLeft = (b.left - z.left) + dx * 150;
    let newTop  = (b.top - z.top) + dy * 150;

    newLeft = clamp(newLeft, 0, z.width - b.width);
    newTop  = clamp(newTop, 0, z.height - b.height);

    noBtn.style.right = "auto";
    noBtn.style.left = newLeft + "px";
    noBtn.style.top = newTop + "px";
    noBtn.style.transform = "none";

    growYes();
  }

  zone.addEventListener("pointermove", e => {
    const b = noBtn.getBoundingClientRect();
    const d = Math.hypot(
      (b.left + b.width / 2) - e.clientX,
      (b.top + b.height / 2) - e.clientY
    );
    if (d < 140) moveNo(e.clientX, e.clientY);
  });

  noBtn.addEventListener("mouseenter", () => {
    hint.classList.add("visible");
  });

  noBtn.addEventListener("mouseleave", () => {
    hint.classList.remove("visible");
  });

  noBtn.addEventListener("click", e => e.preventDefault());

  yesBtn.addEventListener("click", () => {
    zone.style.display = "none";
    hint.style.display = "none";
    result.style.display = "block";
    resizeConfettiCanvas();
    fullScreenConfetti();
  });
</script>
</body>
</html>
"""

components.html(html_code, height=750, scrolling=False)
