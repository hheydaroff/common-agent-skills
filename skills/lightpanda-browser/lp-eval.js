#!/usr/bin/env node

import { connectAndNavigate } from "./cdp.js";

const args = process.argv.slice(2);
if (args.length < 2) {
	console.log("Usage: lp-eval.js <url> 'code'");
	console.log("\nNavigates to URL then evaluates JavaScript and returns the result.");
	console.log("\nExamples:");
	console.log('  lp-eval.js https://example.com "document.title"');
	console.log('  lp-eval.js https://example.com "document.querySelectorAll(\'a\').length"');
	console.log('  lp-eval.js https://example.com "(function(){ return Array.from(document.querySelectorAll(\'a\')).map(a => ({text: a.textContent.trim(), href: a.href})); })()"');
	process.exit(1);
}

const url = args[0];
const code = args.slice(1).join(" ");

const { browser, page } = await connectAndNavigate(url);

const result = await page.evaluate((c) => {
	const AsyncFunction = (async () => {}).constructor;
	return new AsyncFunction(`return (${c})`)();
}, code);

if (Array.isArray(result)) {
	for (let i = 0; i < result.length; i++) {
		if (i > 0) console.log("");
		for (const [key, value] of Object.entries(result[i])) {
			console.log(`${key}: ${value}`);
		}
	}
} else if (typeof result === "object" && result !== null) {
	for (const [key, value] of Object.entries(result)) {
		console.log(`${key}: ${value}`);
	}
} else {
	console.log(result);
}

await browser.disconnect();
