"use client";

import type { JSX } from "react";
import { DOC_GROUPS } from "@/lib/docs-sections";

export type NavSection = {
  readonly id: string;
  readonly title: string;
  readonly group: string;
};

interface DocsSidebarProps {
  readonly sections: ReadonlyArray<NavSection>;
  readonly activeId: string;
  readonly searchQuery: string;
  readonly onSearchChange: (value: string) => void;
  readonly searchRef: React.RefObject<HTMLInputElement | null>;
  readonly onNavigate: () => void;
}

export function DocsSidebar({
  sections,
  activeId,
  searchQuery,
  onSearchChange,
  searchRef,
  onNavigate,
}: DocsSidebarProps): JSX.Element {
  const query = searchQuery.trim().toLowerCase();

  return (
    <div className="docs-sidebar-inner">
      <div className="docs-search">
        <label htmlFor="docs-search-input" className="sr-only">
          Search documentation
        </label>
        <div className="docs-search-field">
          <SearchGlyph />
          <input
            id="docs-search-input"
            ref={searchRef}
            type="search"
            placeholder="Search docs..."
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            className="docs-search-input"
          />
          <kbd className="docs-search-kbd" aria-hidden="true">⌘K</kbd>
        </div>
      </div>

      <nav aria-label="Documentation" className="docs-nav">
        {DOC_GROUPS.map((group) => {
          const groupSections = sections.filter((s) => s.group === group);
          const visible = groupSections.filter((s) =>
            query ? s.title.toLowerCase().includes(query) : true,
          );
          if (visible.length === 0) return null;
          return (
            <div key={group} className="docs-nav-group">
              <p className="docs-nav-heading">{group}</p>
              <ul className="docs-nav-list">
                {visible.map((s) => (
                  <li key={s.id} className="docs-nav-item">
                    <a
                      href={`#${s.id}`}
                      className={`docs-nav-link ${activeId === s.id ? "active" : ""}`}
                      aria-current={activeId === s.id ? "location" : undefined}
                      onClick={onNavigate}
                    >
                      {s.title}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          );
        })}
        {query && sections.every((s) => !s.title.toLowerCase().includes(query)) && (
          <p className="docs-nav-empty">No matches.</p>
        )}
      </nav>
    </div>
  );
}

function SearchGlyph(): JSX.Element {
  return (
    <svg
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      className="docs-search-glyph"
    >
      <circle cx="11" cy="11" r="8" />
      <path d="m21 21-4.3-4.3" />
    </svg>
  );
}
