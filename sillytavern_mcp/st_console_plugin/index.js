import fs from 'node:fs';
import path from 'node:path';

const logPath = path.resolve(globalThis.DATA_ROOT, 'st_console.log');
const stream = fs.createWriteStream(logPath, { flags: 'a' });

const originalMethods = {};
const levels = ['log', 'warn', 'error', 'info', 'debug'];

for (const method of levels) {
    originalMethods[method] = console[method];
    console[method] = function (...args) {
        const timestamp = new Date().toISOString();
        const text = args.map(a =>
            typeof a === 'object' ? (a instanceof Error ? a.stack || a.message : JSON.stringify(a))
                : String(a)
        ).join(' ');
        const line = `[${timestamp}] [${method.toUpperCase()}] ${text}`;
        stream.write(line + '\n');
        originalMethods[method].apply(console, args);
    };
}

process.on('exit', () => {
    stream.end();
});

export const info = {
    id: 'st-console-logger',
    name: 'ST Console Logger',
    description: 'Logs all console output to st_console.log for MCP diagnostics',
};

export async function init(router) {
    router.post('/status', (_req, res) => res.json({ ok: true }));
}
