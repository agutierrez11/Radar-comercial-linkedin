import type { Metadata } from "next";
import { DocsHero } from "@/components/design-system/docs-hero";
import { SkipLink } from "@/components/design-system/layout";
import { DocsShell, type SectionView } from "@/components/docs/docs-shell";
import { SiteFooter } from "@/components/site/site-footer";
import { SiteHeader } from "@/components/site/site-header";
import { DOC_SECTIONS, neighborSections } from "@/lib/docs-sections";
import { loadDocSource, loadDocToc } from "@/lib/docs-source";
import { SITE_CONFIG } from "@/lib/site-config";
import "@/app/styles/docs.css";

export const metadata: Metadata = {
  title: "Documentation",
  description:
    "LazyCodex documentation for the OmO agent harness: install, getting started, commands, concepts, skills, and reference.",
  alternates: {
    canonical: "/docs",
  },
};

export default function DocsPage() {
  const sections: SectionView[] = DOC_SECTIONS.map((s) => {
    const { prev, next } = neighborSections(s.id);
    return {
      id: s.id,
      title: s.title,
      group: s.group,
      html: loadDocSource(s.file),
      toc: loadDocToc(s.file),
      prev,
      next,
    };
  });

  return (
    <>
      <SkipLink />
      <SiteHeader />
      <main id="content" className="docs-page">
        <DocsHero badge={SITE_CONFIG.version} title="Documentation">
          Install and run the OmO harness inside Codex for complex codebases —
          project memory, planning, execution, and verified completion.
        </DocsHero>
        <DocsShell sections={sections} />
      </main>
      <SiteFooter />
    </>
  );
}
