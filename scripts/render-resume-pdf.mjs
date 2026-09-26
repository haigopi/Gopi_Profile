// Render a designed HTML resume (Letter pages, sized in CSS) to PDF.
// Usage: CHROME_PATH=... node scripts/render-resume-pdf.mjs <input.html> <output.pdf>
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import puppeteer from "puppeteer-core";

const [inputArg, outputArg] = process.argv.slice(2);
if (!inputArg || !outputArg) {
  console.error("Usage: node scripts/render-resume-pdf.mjs <input.html> <output.pdf>");
  process.exit(1);
}
const inputHtml = path.resolve(inputArg);
const outputPdf = path.resolve(outputArg);

const executablePath = process.env.CHROME_PATH || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
if (!fs.existsSync(executablePath)) {
  console.error(`Chrome executable not found. Set CHROME_PATH. Tried: ${executablePath}`);
  process.exit(1);
}

const browser = await puppeteer.launch({ headless: "new", executablePath, args: ["--no-sandbox"] });
try {
  const page = await browser.newPage();
  await page.goto(new URL(`file://${inputHtml}`).toString(), { waitUntil: "networkidle0" });
  await page.evaluate(async () => {
    if (document.fonts && document.fonts.ready) await document.fonts.ready;
  });
  // Page size and margins come from the document's @page rule.
  await page.pdf({ path: outputPdf, printBackground: true, preferCSSPageSize: true });
  console.log(`Wrote: ${outputPdf}`);
} finally {
  await browser.close();
}
