import fs from 'fs/promises';
import path from 'path';

async function writeBeacon() {
  const outPath = path.resolve('public', 'sig.beacon.json');
  const payload = {
    ts: new Date().toISOString(),
    agent: 'Agents-Gen-0',
  };

  await fs.mkdir(path.dirname(outPath), { recursive: true });
  await fs.writeFile(outPath, JSON.stringify(payload, null, 2));
  console.log(`Wrote ${outPath}`);
}

writeBeacon().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
