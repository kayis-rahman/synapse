import type { Metadata } from "next";
import { DocsLayout } from "fumadocs-ui/layouts/docs";
import { source, pageTree } from "@/lib/source";

export const metadata: Metadata = {
  title: 'Documentation',
  description: 'Complete SYNAPSE documentation',
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <DocsLayout tree={pageTree}>
      {children}
    </DocsLayout>
  );
}
