import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

if (!process.argv[2]) throw new Error('请通过 build-diagrams.ps1 指定 Mermaid CLI。');
const moduleUrl = new URL('./index.js', pathToFileURL(path.resolve(process.argv[2])));
const { run } = await import(moduleUrl.href);
const config = JSON.parse(await readFile('assets/mermaid-config.json', 'utf8'));
const browser = JSON.parse((await readFile('.work/puppeteer.json', 'utf8')).replace(/^\uFEFF/, ''));
await run('assets/figures/pipeline.mmd', process.argv[3] || 'assets/figures/pipeline.pdf', {
  puppeteerConfig: browser,
  parseMMDOptions: {
    backgroundColor: '#F7F9FB',
    mermaidConfig: config,
    customFontCSS: [{
      cssUrl: pathToFileURL(path.resolve('.work/diagram-fonts.css')),
      allowParentDirectoryLevel: 0,
    }],
  },
});
