import { DOC_SOURCES, DOC_TOC, type DocHeading } from "./docs-content.generated";

export function loadDocSource(file: string): string {
  const source = DOC_SOURCES[file];
  if (source === undefined) {
    throw new Error(
      `Unknown doc file: ${file}. Run \`node ./scripts/generate-docs-content.mjs\` to regenerate docs content.`,
    );
  }
  return source;
}

export function loadDocToc(file: string): DocHeading[] {
  const toc = DOC_TOC[file];
  if (toc === undefined) {
    throw new Error(
      `Unknown doc file: ${file}. Run \`node ./scripts/generate-docs-content.mjs\` to regenerate docs content.`,
    );
  }
  return toc;
}
