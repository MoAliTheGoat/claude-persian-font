// Opens a page in a fresh headless Edge and reports which installed font
// Chromium actually used for each test paragraph (CDP getPlatformFontsForNode).
// usage: node fonts.mjs <url> <label>
import { spawn } from 'node:child_process'
import { mkdtempSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'

const [url, label] = process.argv.slice(2)
const EDGE = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
const port = 9300 + Math.floor(Math.random() * 500)
const edge = spawn(EDGE, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${mkdtempSync(join(tmpdir(), 'e'))}`, '--window-size=700,400', 'about:blank'])
const sleep = ms => new Promise(r => setTimeout(r, ms))

let target
for (let i = 0; i < 40 && !target; i++) {
  await sleep(500)
  try { target = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find(t => t.type === 'page') } catch {}
}
const ws = new WebSocket(target.webSocketDebuggerUrl)
await new Promise(r => (ws.onopen = r))
let id = 0
const pending = new Map()
ws.onmessage = m => { const d = JSON.parse(m.data); if (pending.has(d.id)) { pending.get(d.id)(d.result ?? d); pending.delete(d.id) } }
const send = (method, params = {}) => new Promise(r => { pending.set(++id, r); ws.send(JSON.stringify({ id, method, params })) })

await send('Page.enable'); await send('DOM.enable'); await send('CSS.enable')
await send('Page.navigate', { url })
await sleep(4000)
const out = { label }
const { root } = await send('DOM.getDocument', { depth: -1 })
for (const sel of ['#serif', '#sans', '#latin']) {
  const { nodeId } = await send('DOM.querySelector', { nodeId: root.nodeId, selector: sel })
  if (!nodeId) { out[sel] = 'missing'; continue }
  const r = await send('CSS.getPlatformFontsForNode', { nodeId })
  out[sel] = (r.fonts || []).map(f => `${f.familyName} (${f.glyphCount})`)
}
const shot = await send('Page.captureScreenshot', { format: 'png' })
writeFileSync(`shot-${label}.png`, Buffer.from(shot.data, 'base64'))
console.log(JSON.stringify(out))
ws.close(); edge.kill()
process.exit(0)
