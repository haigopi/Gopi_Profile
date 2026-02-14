import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import puppeteer from "puppeteer-core";

const workspaceDir = process.cwd();
const inputHtml = path.resolve(workspaceDir, "gopi_profile.html");
const outputPdf = path.resolve(workspaceDir, "gopi_profile.pdf");

if (!fs.existsSync(inputHtml)) {
  console.error(`Input HTML not found: ${inputHtml}`);
  process.exit(1);
}

const defaultChromePath = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const executablePath = process.env.CHROME_PATH || defaultChromePath;

if (!fs.existsSync(executablePath)) {
  console.error("Chrome executable not found.");
  console.error(`Set CHROME_PATH or install Chrome. Tried: ${executablePath}`);
  process.exit(1);
}

const fileUrl = new URL(`file://${inputHtml}`);

const browser = await puppeteer.launch({
  headless: "new",
  executablePath,
  args: ["--no-sandbox", "--disable-setuid-sandbox"],
});

try {
  const page = await browser.newPage();

  // Ensure consistent viewport for layout.
  await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 1 });

  await page.goto(fileUrl.toString(), { waitUntil: "networkidle0" });

  // Give fonts a brief moment to settle (esp. Google Fonts).
  await page.evaluate(async () => {
    // @ts-ignore
    if (document.fonts && document.fonts.ready) await document.fonts.ready;
  });

  await page.pdf({
    path: outputPdf,
    format: "A4",
    printBackground: true,
    margin: {
      top: "12mm",
      right: "12mm",
      bottom: "12mm",
      left: "12mm",
    },
  });

  console.log(`Wrote: ${outputPdf}`);
} finally {
  await browser.close();
}
