import { readFile } from 'fs/promises';
import ts from 'typescript';

export async function load(url, context, nextLoad) {
  if (url.endsWith('.ts')) {
    const source = await readFile(new URL(url));
    const transpiled = ts.transpileModule(source.toString(), {
      compilerOptions: { module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2019 }
    });
    return {
      format: 'module',
      source: transpiled.outputText,
      shortCircuit: true
    };
  }
  return nextLoad(url, context);
}
