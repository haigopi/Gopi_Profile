// Render scripts/og-image.html to og-image.png (1200x630) for link previews.
// Usage: CHROME_PATH=... node scripts/render-og.mjs
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import puppeteer from "puppeteer-core";

const root = process.cwd();
const inputHtml = path.resolve(root, "scripts/og-image.html");
const outputPng = path.resolve(root, "og-image.png");

const executablePath = process.env.CHROME_PATH || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
if (!fs.existsSync(executablePath)) {
  console.error(`Chrome executable not found. Set CHROME_PATH. Tried: ${executablePath}`);
  process.exit(1);
}

const browser = await puppeteer.launch({ headless: "new", executablePath, args: ["--no-sandbox"] });
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1200, height: 630, deviceScaleFactor: 1 });
  await page.goto(new URL(`file://${inputHtml}`).toString(), { waitUntil: "networkidle0" });
  await page.evaluate(async () => {
    if (document.fonts && document.fonts.ready) await document.fonts.ready;
  });
  await page.screenshot({ path: outputPng });
  console.log(`Wrote: ${outputPng}`);
} finally {
  await browser.close();
}
