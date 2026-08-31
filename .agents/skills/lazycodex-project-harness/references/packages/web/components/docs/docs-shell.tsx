"use client";

import type { JSX } from "react";
import { useEffect, useRef, useState } from "react";
import type { DocHeading } from "@/lib/docs-content.generated";
import type { DocSection } from "@/lib/docs-sections";
import { DocsSidebar } from "./docs-sidebar";
import { DocsToc } from "./docs-toc";
import { DocsPrevNext } from "./docs-prev-next";

export type SectionView = {
  readonly id: string;
  readonly title: string;
  readonly group: string;
  readonly html: string;
  readonly toc: ReadonlyArray<DocHeading>;
  readonly prev: DocSection | undefined;
  readonly next: DocSection | undefined;
};

interface DocsShellProps {
  readonly sections: ReadonlyArray<SectionView>;
}

export function DocsShell({ sections }: DocsShellProps): JSX.Element {
  const [searchQuery, setSearchQuery] = useState("");
  const [activeId, setActiveId] = useState<string>(sections[0]?.id ?? "");
  const [activeHeadingId, setActiveHeadingId] = useState<string>("");
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const searchRef = useRef<HTMLInputElement | null>(null);
  const sectionObserverRef = useRef<IntersectionObserver | null>(null);
  const headingObserverRef = useRef<IntersectionObserver | null>(null);

  // ⌘K / Ctrl-K focuses the search field from anywhere on the page.
  useEffect(() => {
    function onKeyDown(event: KeyboardEvent): void {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        searchRef.current?.focus();
        searchRef.current?.select();
      }
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  useEffect(() => {
    function handleHashChange(): void {
      const hash = window.location.hash.slice(1);
      if (hash) setActiveId(hash);
    }
    window.addEventListener("hashchange", handleHashChange);
    handleHashChange();
    return () => window.removeEventListener("hashchange", handleHashChange);
  }, []);

  // Scroll-spy: which section is currently in view (drives sidebar + right ToC).
  useEffect(() => {
    sectionObserverRef.current = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) setActiveId(entry.target.id);
        }
      },
      { rootMargin: "-15% 0px -75% 0px" },
    );
    for (const el of document.querySelectorAll<HTMLElement>(".docs-section[id]")) {
      sectionObserverRef.current.observe(el);
    }
    return () => sectionObserverRef.current?.disconnect();
  }, [sections]);

  // Scroll-spy: which heading is currently in view (drives right ToC highlight).
  useEffect(() => {
    headingObserverRef.current = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) setActiveHeadingId(entry.target.id);
        }
      },
      { rootMargin: "-15% 0px -80% 0px" },
    );
    for (const el of document.querySelectorAll<HTMLElement>(".docs-content h2[id], .docs-content h3[id]")) {
      headingObserverRef.current.observe(el);
    }
    return () => headingObserverRef.current?.disconnect();
  }, [sections]);

  const navSections = sections.map((s) => ({
    id: s.id,
    title: s.title,
    group: s.group,
  }));

  const activeSection = sections.find((s) => s.id === activeId) ?? sections[0];

  return (
    <div className="docs-layout">
      <button
        type="button"
        className="docs-mobile-toggle"
        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
        aria-expanded={isMobileMenuOpen}
        aria-controls="docs-sidebar"
      >
        {isMobileMenuOpen ? "Close Menu" : "Menu"}
      </button>

      <aside
        id="docs-sidebar"
        className={`docs-sidebar ${isMobileMenuOpen ? "open" : ""}`}
      >
        <DocsSidebar
          sections={navSections}
          activeId={activeId}
          searchQuery={searchQuery}
          onSearchChange={setSearchQuery}
          searchRef={searchRef}
          onNavigate={() => setIsMobileMenuOpen(false)}
        />
      </aside>

      <div className="docs-main-content">
        {sections.map((s) => (
          <section key={s.id} id={s.id} className="docs-section" aria-labelledby={`${s.id}-title`}>
            <h2 id={`${s.id}-title`} className="docs-section-title">
              {s.title}
            </h2>
            <article
              className="docs-content"
              dangerouslySetInnerHTML={{ __html: s.html }}
            />
            <DocsPrevNext prev={s.prev} next={s.next} />
          </section>
        ))}
      </div>

      <DocsToc
        headings={activeSection?.toc ?? []}
        activeHeadingId={activeHeadingId}
      />
    </div>
  );
}
