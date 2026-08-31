"use client";

import type { JSX } from "react";
import type { DocHeading } from "@/lib/docs-content.generated";

interface DocsTocProps {
  readonly headings: ReadonlyArray<DocHeading>;
  readonly activeHeadingId: string;
}

export function DocsToc({ headings, activeHeadingId }: DocsTocProps): JSX.Element {
  const items = headings.filter((h) => h.level === 2 || h.level === 3);
  if (items.length === 0) return <aside className="docs-toc" aria-hidden="true" />;

  return (
    <aside className="docs-toc" aria-label="On this section">
      <p className="docs-toc-heading">On this section</p>
      <ul className="docs-toc-list">
        {items.map((h) => (
          <li
            key={h.id}
            className={`docs-toc-item ${h.level === 3 ? "indent" : ""}`}
          >
            <a
              href={`#${h.id}`}
              className={`docs-toc-link ${activeHeadingId === h.id ? "active" : ""}`}
              aria-current={activeHeadingId === h.id ? "location" : undefined}
            >
              {h.text}
            </a>
          </li>
        ))}
      </ul>
    </aside>
  );
}
