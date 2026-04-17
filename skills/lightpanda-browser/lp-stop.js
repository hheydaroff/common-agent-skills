#!/usr/bin/env node

import { readFileSync, unlinkSync } from "node:fs";

const pidFile = `${process.env.HOME}/.cache/lightpanda.pid`;

try {
	const pid = parseInt(readFileSync(pidFile, "utf8").trim());
	process.kill(pid, "SIGTERM");
	unlinkSync(pidFile);
	console.log(`✓ Lightpanda stopped (PID: ${pid})`);
} catch (e) {
	if (e.code === "ENOENT") {
		console.log("✓ No Lightpanda server running (no PID file)");
	} else if (e.code === "ESRCH") {
		try { unlinkSync(pidFile); } catch {}
		console.log("✓ Lightpanda process already gone, cleaned up PID file");
	} else {
		console.error("✗ Error stopping Lightpanda:", e.message);
		process.exit(1);
	}
}
