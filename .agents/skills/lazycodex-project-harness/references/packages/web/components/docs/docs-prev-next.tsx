import type { JSX } from "react";
import type { DocSection } from "@/lib/docs-sections";

interface DocsPrevNextProps {
  readonly prev: DocSection | undefined;
  readonly next: DocSection | undefined;
}

export function DocsPrevNext({ prev, next }: DocsPrevNextProps): JSX.Element {
  if (!prev && !next) return <></>;

  return (
    <nav className="docs-prev-next" aria-label="Section navigation">
      {prev ? (
        <a className="docs-prev-next-card prev" href={`#${prev.id}`}>
          <span className="docs-prev-next-label" aria-hidden="true">← Previous</span>
          <span className="docs-prev-next-title">{prev.title}</span>
        </a>
      ) : (
        <span className="docs-prev-next-card placeholder" aria-hidden="true" />
      )}
      {next ? (
        <a className="docs-prev-next-card next" href={`#${next.id}`}>
          <span className="docs-prev-next-label" aria-hidden="true">Next →</span>
          <span className="docs-prev-next-title">{next.title}</span>
        </a>
      ) : (
        <span className="docs-prev-next-card placeholder" aria-hidden="true" />
      )}
    </nav>
  );
}
