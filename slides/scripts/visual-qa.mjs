#!/usr/bin/env node
// Slidev 덱 시각 QA: 라이트/다크 두 스킴으로 슬라이드별 캡처 + overflow 감사
import fs from 'node:fs/promises'
import path from 'node:path'
import net from 'node:net'
import { spawn } from 'node:child_process'
import { chromium } from 'playwright-chromium'

const root = path.resolve(new URL('..', import.meta.url).pathname)
const outDir = path.join(root, '.omx', 'qa')

async function getFreePort() {
  return new Promise((resolve, reject) => {
    const srv = net.createServer()
    srv.unref()
    srv.on('error', reject)
    srv.listen(0, '127.0.0.1', () => {
      const p = srv.address().port
      srv.close(() => resolve(p))
    })
  })
}

const port = await getFreePort()
const base = `http://localhost:${port}`

const server = spawn('pnpm', ['exec', 'slidev', 'slides.md', '--port', String(port), '--log', 'warn'], {
  cwd: root, stdio: ['ignore', 'pipe', 'pipe'],
})
server.stderr.on('data', (c) => process.stderr.write(c))

async function up() {
  for (let i = 0; i < 120; i++) {
    try { const r = await fetch(base + '/1'); if (r.ok) return true } catch {}
    await new Promise((r) => setTimeout(r, 500))
  }
  return false
}
if (!(await up())) { server.kill(); console.error('server failed'); process.exit(1) }

await fs.rm(outDir, { recursive: true, force: true })
await fs.mkdir(outDir, { recursive: true })

const audit = () => {
  const layouts = [...document.querySelectorAll('.slidev-layout')].filter((el) => {
    const r = el.getBoundingClientRect(); return r.width > 10 && r.height > 10
  })
  const layout = layouts.at(-1)
  if (!layout) return { error: 'no layout' }
  const lr = layout.getBoundingClientRect()
  const issues = []
  for (const el of layout.querySelectorAll('*')) {
    if (['PATH', 'DEFS', 'SYMBOL'].includes(el.tagName.toUpperCase())) continue
    const r = el.getBoundingClientRect()
    if (r.width < 2 || r.height < 2) continue
    const outBottom = r.bottom - lr.bottom
    const outRight = r.right - lr.right
    if (outBottom > 2 || outRight > 2) {
      issues.push({
        tag: el.tagName.toLowerCase(),
        cls: String(el.className).slice(0, 60),
        text: (el.innerText || '').slice(0, 40),
        outBottom: Math.round(outBottom),
        outRight: Math.round(outRight),
      })
    }
  }
  return { htmlClass: document.documentElement.className, issues: issues.slice(0, 8) }
}

const browser = await chromium.launch()
const report = {}
for (const scheme of ['light', 'dark']) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, colorScheme: scheme })
  await page.goto(base + '/1', { waitUntil: 'networkidle' })
  const total = await page.evaluate(() => window.__slidev__.nav.total)
  report.total = total
  report[scheme] = {}
  for (let n = 1; n <= total; n++) {
    await page.goto(`${base}/${n}`, { waitUntil: 'domcontentloaded' })
    await page.waitForFunction((x) => window.__slidev__?.nav?.currentPage === x, n, { timeout: 8000 })
    await page.waitForTimeout(450)
    await page.screenshot({ path: path.join(outDir, `${scheme}-${String(n).padStart(2, '0')}.png`) })
    report[scheme][n] = await page.evaluate(audit)
  }
  await page.close()
}
await browser.close()
server.kill()

await fs.writeFile(path.join(outDir, 'report.json'), JSON.stringify(report, null, 2))
let bad = 0
for (const scheme of ['light', 'dark']) {
  for (const [n, r] of Object.entries(report[scheme])) {
    if (r.issues?.length) { bad++; console.log(`[${scheme} ${n}] html=${r.htmlClass}`, JSON.stringify(r.issues)) }
  }
}
console.log(`done: ${report.total} slides, htmlClass(dark emulation)=${report.dark?.[1]?.htmlClass}, slides with overflow: ${bad}`)
